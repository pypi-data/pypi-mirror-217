import glob
import json
import os
from datetime import datetime
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

from jsonschema import validate
from stocks.models import InstrumentRun, User, Instrument, SequencingLibrary, NanoporeAssay, Dataset, \
    DatasetCollection, DatasetFile, FastqFile, Fast5File, FastqDir, Fast5Dir, DataProducer, SequencingAssay, UserGroup
from stocks import AssayStructureError
from cli.utils import Technology, SequencingReadType, SequencingRunType, NanoporeLiveBaseCallingType
from stocks.assaysniffer import JSONAssaySniffer, AssaySniffer, check_valid_directory
from stocks.assaysniffer.registry import registry
import pandas as pd

logger = logging.getLogger(__name__)

@registry.install
class NanoporeAssaySniffer(AssaySniffer):
    # see https://github.com/nanoporetech/minknow_api for some concept definition (in the README)

    # currently, 12 but announced to be 96 in near future
    MAX_BARCODE_NUMBER: int = 12

    @classmethod
    def is_multi_run_sniffer(cls) -> bool:
        return False

    @classmethod
    def get_supported_technology(cls) -> Technology:
        """
        :return: the technology this sniffer supports ie 'Technology.SEQUENCING'
        """
        return Technology.SEQUENCING

    @classmethod
    def get_supported_platforms(cls) -> List[str]:
        """
        :return: platforms: the list of Platform this sniffer supports
        """
        return ["NANOPORE"]

    @classmethod
    def get_sniffer_description(cls) -> str:
        help_txt = f"""
        This sniffer looks into a directory expecting the native project_id structure created by nanopore sequencer:
            - PROJECT_FOLDER => an option project_id folder regrouping multiple samples & runs
                - LIBRARY/SAMPLE_FOLDER(s) => an optional library (potentially multiplexed) folder containing 
                                            results from 1 or more runs (tech replicates)
                    - RUN_FOLDER(s)
                        - barcode_alignment_* file: contains a single line when the sample is not a multiplexed library.
                                                    MANDATORY
                        - final_summary_* file: key=value summary of main parameters. 
                                                MANDATORY
                        - report_*.md file: a multi-section file with an initial JSON session holding all but more 
                                            params than final_summary_* file
                                            MANDATORY
                        - duty_time_* file: we will assume this optional (as we dont use it)
                        - throughput_* file: we will assume this optional (as we dont use it)
                        - other_reports/*csv: additional files generate during run. We wont assume anything here   
                        
                        If base calling was OFF:
                        - fast5 : a directory containing the raw fast5 signal. MANDATORY
                        
                        If base calling was ON:
                        - sequencing_summary_* file: a big file listing all the reads sequenced and in which fastQ/fast5
                                                    file(s) they are in, this file is multi Gb big.
                                                    MANDATORY when base calling is true

                        - fast5_fail & fast5_pass: directories containing the fast5 files for failed and passed reads.
                                                    A sub-directory layer 'barcode01-12' and 'unclassified' is present 
                                                    if the library is multiplexed. 
                                                    one of the two is MANDATORY
                        - fastq_fail & fastq_pass: optional directories (present if base calling was done) containing 
                                                    the fast5 files for failed and passed reads. 
         
        The run folder detection occurs by looking for the presence of files matching the pattern
        'final_summary_*.txt' and/or 'report_*.md' (both must be found). 
        Each directory containing such a file will be parsed into a nanopore assay. 
        
        When the fast5 (and fastq) directories contain more than one file, the directories are registered as 
        'multi-fast5'/'multi-fastq' dataset directories. When unique files are found per dir_path, there are registered 
        as fast5/fastq dataset files. Each 'fast5', 'fast5_pass'/'fast5_fail', 'fastq_pass' and 'fastq_fail'
         will end up as a different dataset collection when found. 
        
        The 'sequencing_summary_* file' and verbose other metadata files are also registered as a dataset
        
        An Assay is created for each *run*.
         """
        return help_txt

    def looks_like_nanopore_project_dir(self, dir_path: Path) -> int:
        """
        inspects the given directory for being a Nanopore top project_id dir_path.

        :param dir_path: the path to Nanopore project_id dir_path
        :return int: the run number found (or raises exception)
        :raises: AssayStructureError if expected content is not found
        """
        # we grab all the final_summary_* files. One per run should be found
        run_num = 0
        for path in dir_path.rglob('final_summary_*.txt'):
            run_num += 1
            run_dir: Path = path.parent

            # each run folder must contain a number of files/dir_path
            fast5_pass: bool = Path(run_dir, "fast5_pass").exists()
            fast5_fail: bool = Path(run_dir, "fast5_fail").exists()
            fast5: bool = Path(run_dir, "fast5").exists()

            if not any([fast5, fast5_fail, fast5_pass]):
                raise AssayStructureError(f"Expected fast5* dir_path not found in Nanopore run dir_path {str(run_dir)}")

            for expected in ['barcode_alignment_*.tsv', 'report_*.md']:
                if not self.nanopore_file_exists(run_dir, expected):
                    raise AssayStructureError(
                        f"File matching {expected} pattern not found in Nanopore run folder {str(run_dir)}")

            if Path(run_dir, "fastq_pass").exists():
                if not self.nanopore_file_exists(run_dir, 'sequencing_summary_*.txt'):
                    raise AssayStructureError(
                        "sequencing_summary_*.txt not found while base calling is on (fasq_pass dir_path present) " +
                        f"in Nanopore run folder {str(run_dir)}")

        return run_num

    @staticmethod
    def nanopore_file_exists(a_dir: Path, filename_pattern: str):
        for x in a_dir.glob(pattern=filename_pattern):
            return x.exists()
        return False

    def sniff_instrument_run_assays(self, dir_path: Path, group: str, username: Optional[str] = None) \
            -> List[InstrumentRun]:
        owner: User
        if username:
            owner = User(username=username, groups=[UserGroup(name=group)])

        if not check_valid_directory(dir_path):
            mess = f"The dir_path {str(dir_path)} is either empty or does not point to a valid directory."
            raise AssayStructureError(mess)

        runs: List[InstrumentRun] = list()
        # validate directory
        try:
            if self.looks_like_nanopore_project_dir(dir_path) == 0:
                return runs
        except AssayStructureError as err:
            mess = f"""The dir_path {str(dir_path)} does not fit the expected Nanopore data structure:
                    {self.get_sniffer_description()}
    
                    Error is : {str(err)}
                    """
            raise AssayStructureError(mess)

        for path in dir_path.rglob('report_*.md'):
            params: Dict[str, str] = self.get_param_dict_from_nanopore_report(path)
            final_params: Dict[str, str] = self.get_param_dict_from_nanopore_final_summary(path.parent)

            sample_id = params['sample_id']

            # instrument details
            instrument_serial = params['host_product_serial_number']
            instrument_name = params['hostname']
            model = params['device_type']
            model_code = params['host_product_code']
            instrument = Instrument(name=f"{model} {instrument_name}", model=model_code,
                                    serial_number=instrument_serial)
            # run details
            run_name = path.parent.name
            run_id = params['run_id']
            run = InstrumentRun(name=f"{instrument.name} run {run_id}", managed=False, technology=Technology.SEQUENCING,
                                platform="NANOPORE", instrument=instrument)
            if owner:
                run.set_owner(owner=owner, also_set_group=True)
            else:
                run.group = group

            run.add_annotation(annot_key="position", annot_value=params['device_id'])

            flowcell = params['flow_cell_id']
            flowcell_version = params['flow_cell_product_code']
            protocol = final_params['protocol']
            # protocol=sequencing/sequencing_MIN106_DNA:FLO-MIN106:SQK-LSK110
            # here 2 pieces of info seems avail => 'DNA' (as the run_mode) and 'SQK-LSK110' (as the chemistry)
            protocol_splits = protocol.split(":")
            chemistry: str = protocol_splits.pop()
            run_mode: str = protocol_splits.pop()
            # run times
            start_time = datetime.fromisoformat(final_params['started']).replace(microsecond=0)
            end_time = datetime.fromisoformat(final_params['processing_stopped']).replace(microsecond=0)
            run.start_datetime = start_time
            run.end_datetime = end_time
            # td = end_time - start_time
            # run_duration: str = str(td)  ## not used

            # is this sample multiplexed ?
            barcode_df = self.sniff_multiplexing_info(run_dir=path.parent)
            multiplexed = len(barcode_df) > 1
            # if we have fastq files, base calling was on
            with_base_calling = bool(final_params['basecalling_enabled'])
            datasets: List[Dataset] = []
            samples: List[SequencingLibrary] = []

            if multiplexed:
                # we need to find how many multiplexed samples we had
                # create the different dataset
                if Path(path.parent, "fast5").exists():
                    datasets.extend(self.get_nanopore_demultiplexed_datasets(
                        run_dir=path.parent, dir_name="fast5", sample_base_name=sample_id, file_type="fast5",
                        barcode_number=self.MAX_BARCODE_NUMBER))

                if Path(path.parent, "fast5_pass").exists():
                    datasets.extend(self.get_nanopore_demultiplexed_datasets(
                        run_dir=path.parent, dir_name="fast5_pass", sample_base_name=sample_id, file_type="fast5",
                        barcode_number=self.MAX_BARCODE_NUMBER))

                if Path(path.parent, "fast5_fail").exists():
                    datasets.extend(self.get_nanopore_demultiplexed_datasets(
                        run_dir=path.parent, dir_name="fast5_fail", sample_base_name=sample_id, file_type="fast5",
                        barcode_number=self.MAX_BARCODE_NUMBER))

                if Path(path.parent, "fastq_pass").exists():
                    datasets.extend(self.get_nanopore_demultiplexed_datasets(
                        run_dir=path.parent, dir_name="fastq_pass", sample_base_name=sample_id, file_type="fastq",
                        barcode_number=self.MAX_BARCODE_NUMBER))

                if Path(path.parent, "fastq_fail").exists():
                    datasets.extend(self.get_nanopore_demultiplexed_datasets(
                        run_dir=path.parent, dir_name="fastq_fail", sample_base_name=sample_id, file_type="fastq",
                        barcode_number=self.MAX_BARCODE_NUMBER))

                # get unique list of samples
                name2lib = dict()
                for d in datasets:
                    if d.sample.name not in name2lib:
                        name2lib[d.sample.name] = d.sample
                samples = list(name2lib.values())

            else:
                # we have a single assay, a single sample
                sample = SequencingLibrary(name=sample_id, barcode=None)
                samples.append(sample)
                # create the different dataset
                if Path(path.parent, "fast5").exists():
                    datasets.append(self.get_nanopore_dataset(run_dir=path.parent, dir_name="fast5", sample=sample,
                                                              file_type="fast5"))

                if Path(path.parent, "fast5_pass").exists():
                    datasets.append(self.get_nanopore_dataset(run_dir=path.parent, dir_name="fast5_pass", sample=sample,
                                                              file_type="fast5"))

                if Path(path.parent, "fast5_fail").exists():
                    datasets.append(self.get_nanopore_dataset(run_dir=path.parent, dir_name="fast5_fail", sample=sample,
                                                              file_type="fast5"))

                if Path(path.parent, "fastq_pass").exists():
                    datasets.append(self.get_nanopore_dataset(run_dir=path.parent, dir_name="fastq_pass", sample=sample,
                                                              file_type="fastq"))

                if Path(path.parent, "fastq_fail").exists():
                    datasets.append(self.get_nanopore_dataset(run_dir=path.parent, dir_name="fastq_fail", sample=sample,
                                                              file_type="fastq"))

            datasets.extend(self.get_all_metadata_file_as_datasets(run_dir=path.parent))
            # create the assay for this run dir_path
            assay = NanoporeAssay(name=run_name, flowcell=flowcell, flowcell_version=flowcell_version,
                                  datasets=datasets, samples=samples, instrumentrun=run,
                                  chemistry=chemistry, run_mode=run_mode,
                                  multiplexed=False, demultiplexed=False)
            if owner:
                assay.set_owner(owner=owner, also_set_group=True)
            else:
                assay.group = group

            assay.live_base_calling = NanoporeLiveBaseCallingType.OTHER if with_base_calling \
                else NanoporeLiveBaseCallingType.NONE
            run.add_assay(assay)
            # add run in result list
            runs.append(run)

        return runs

    def get_nanopore_demultiplexed_datasets(self, run_dir: Path, dir_name: str, sample_base_name: str, file_type: str,
                                            barcode_number: int) -> List[Dataset]:
        """
        :param run_dir: the base dir_path
        :param dir_name: the dir_path name to inspect (this dir_path is in run_dir)
        :param sample_base_name: the multiplexed library name
        :param file_type: either fast5 or fastq
        :param barcode_number : the number of barcode to expect (12 or 96 as announced)
        :return:
        """
        if file_type not in ['fastq', 'fast5']:
            raise ValueError(f"file_type must be one of 'fastq', 'fast5' but was {file_type}")

        col = DatasetCollection(name=dir_name)
        base_dir = Path(run_dir, dir_name)
        single_file: bool = self.just_one_file_in_dir(Path(base_dir, "barcode01"), file_type)
        datasets: List[Dataset] = []
        barcode_names: List[str] = [f"barcode{n:02d}" for n in range(1, barcode_number + 1)]
        barcode_names.append('unclassified')
        for barcode in barcode_names:
            the_dir = Path(base_dir, barcode)
            if not the_dir.exists():
                raise AssayStructureError(f"Multiplexed result directory missing : {str(the_dir)}")
            lib: SequencingLibrary = SequencingLibrary(name=f"{sample_base_name}_{barcode}", barcode=barcode)
            data_file: DatasetFile
            if single_file:
                the_file = Path(the_dir, self.list_files_in_dir(the_dir, file_type)[0])
                if file_type == 'fastq':
                    data_file = FastqFile(name=f"{dir_name} file", read_type=SequencingReadType.READ1,
                                          byte=os.path.getsize(str(the_file)), mime_type="application/gzip",
                                          uri=str(the_file))
                else:
                    data_file = Fast5File(name=f"{dir_name} file", byte=os.path.getsize(str(the_file)),
                                          uri=str(the_file))
            else:
                if file_type == 'fastq':
                    data_file = FastqDir(name=f"{dir_name} directory", read_type=SequencingReadType.READ1,
                                         mime_type="application/gzip", uri=str(the_dir))
                else:
                    data_file = Fast5Dir(name=f"{dir_name} directory", uri=str(the_dir))
            datasets.append(Dataset(name=data_file.name, is_raw=True,
                                    datafiles=[data_file], samples=[lib], collection=col))

        return datasets

    @staticmethod
    def get_all_metadata_file_as_datasets(run_dir: Path) -> List[Dataset]:
        """
        registers all file found in the indicated run_dir as datasets without link to samples. If present, the
        sub dir_path 'other_reports' is also scanned.
        Skips hidden files (name starting with a dot '.').

        :param run_dir:
        :return: a list of Datasets groups into a DatasetCollection; or an empty list
        """
        datasets: List[Dataset] = list()
        col: DatasetCollection = DatasetCollection(name="metadata files")
        for f in [p for p in run_dir.iterdir() if p.is_file() and not p.name.startswith(".")]:
            df: DatasetFile = DatasetFile(name=f.name, mime_type="", byte=os.path.getsize(str(f)),
                                          filetype=f.suffix[1:],
                                          uri=str(f))
            datasets.append(Dataset(name=f.name, is_raw=False, datafiles=[df], collection=col))

        # other_reports subdir
        for f in [p for p in Path(run_dir, 'other_reports').iterdir() if p.is_file()]:
            df: DatasetFile = DatasetFile(name=f"other_reports/{f.name}", mime_type="", byte=os.path.getsize(str(f)),
                                          filetype=f.suffix[1:], uri=str(f))
            datasets.append(Dataset(name=f.name, is_raw=False, datafiles=[df], collection=col))

        return datasets

    def get_nanopore_dataset(self, run_dir: Path, dir_name: str, sample: SequencingLibrary, file_type: str) -> Dataset:
        """

        :param run_dir: the base dir_path
        :param dir_name: the dir_path name to inspect (this dir_path is in run_dir)
        :param sample: the sample name
        :param file_type: either fast5 or fastq
        :return:
        """
        if file_type not in ['fastq', 'fast5']:
            raise ValueError(f"file_type must be one of 'fastq', 'fast5' but was {file_type}")

        col = DatasetCollection(name=dir_name)
        the_dir = Path(run_dir, dir_name)
        data_file: DatasetFile
        single_file: bool = self.just_one_file_in_dir(the_dir, file_type)

        if single_file:
            the_file = Path(the_dir, self.list_files_in_dir(the_dir, file_type)[0])
            if file_type == 'fastq':
                data_file = FastqFile(name=f"{dir_name} file", read_type=SequencingReadType.READ1,
                                      byte=os.path.getsize(str(the_file)), mime_type="application/gzip",
                                      uri=str(the_file))
            else:
                data_file = Fast5File(name=f"{dir_name} file", byte=os.path.getsize(str(the_file)), uri=str(the_file))
        else:
            if file_type == 'fastq':
                data_file = FastqDir(name=f"{dir_name} directory", read_type=SequencingReadType.READ1,
                                     mime_type="application/gzip", uri=str(the_dir))
            else:
                data_file = Fast5Dir(name=f"{dir_name} directory", uri=str(the_dir))

        return Dataset(name=data_file.name, is_raw=True, datafiles=[data_file], samples=[sample],
                       collection=col)

    @staticmethod
    def get_param_dict_from_nanopore_report(report_path: Path) -> Dict[str, str]:
        """
        Loads the json params from the Tracking ID section of the given report

        :param report_path:
        :return:
        """

        json_str = ""
        keep = False
        with open(report_path) as sum_file:
            for line in sum_file:
                if keep or line.startswith('{'):
                    keep = True
                    json_str += line
                if keep and line.startswith('}'):
                    break
        params = json.loads(json_str)
        return params

    @staticmethod
    def get_param_dict_from_nanopore_final_summary(run_dir: Path) -> Dict[str, str]:
        """
        Load the key/value params from the final_summary_*.txt file

        :param run_dir:
        :return:
        """
        params: Dict[str, str] = dict()
        found_it: bool = False
        for sum_file_path in run_dir.glob('final_summary_*.txt'):
            if found_it:
                raise AssayStructureError(f"Found more than one final_summary_*.txt file in run dir_path {run_dir}")
            with open(str(sum_file_path)) as sum_file:
                for line in sum_file:
                    name, var = line.partition("=")[::2]
                    params[name.strip()] = var.strip()

        return params

    @staticmethod
    def list_files_in_dir(dir_path: Path, ext: str, gz_tolerant: bool = True) -> List[Path]:
        """
        util method to list files matching given extension (optionally tolerating extra '.gz') in the given dir_path

        :param dir_path:
        :param ext:
        :param gz_tolerant:
        :return:
        """
        file_paths: List[Path] = []
        for path in dir_path.iterdir():
            if path.is_file() and (path.name.endswith(ext) or (gz_tolerant and path.name.endswith(ext + ".gz"))):
                file_paths.append(path)
        return file_paths

    @staticmethod
    def just_one_file_in_dir(dir_path: Path, ext: str, gz_tolerant: bool = True) -> bool:
        """
        util method to check if the given dir_path contains a unique file matching given extension (optionally
        tolerating extra '.gz')

        :param dir_path:
        :param ext:
        :param gz_tolerant:
        :return: True if a single file matching the parameters is found in the dir_path ; else False (0 or >1 file
        found)
        """
        num: int = 0
        for path in dir_path.iterdir():
            if path.is_file() and (path.name.endswith(ext) or (gz_tolerant and path.name.endswith(ext + ".gz"))):
                num += 1
            if num > 1:
                return False

        return num == 1

    @staticmethod
    def sniff_multiplexing_info(run_dir: Path) -> Any:
        """
        returns the barcode file (barcode_alignment_*.tsv) content as a panda dataframe
        :param run_dir:
        :return:
        """
        # finds the barcode file
        bc_file: Optional[Path] = None
        for x in run_dir.glob(pattern='barcode_alignment_*.tsv'):
            bc_file = x
        if not bc_file or not bc_file.exists():
            raise FileNotFoundError("Barcode file not found (pattern 'barcode_alignment_*.tsv')")
        return pd.read_csv(str(bc_file), sep='\t')


@registry.install
class GeneCoreAssaySniffer(JSONAssaySniffer):
    JSON_NAME_PATTERN: str = '*_lane[0-9].json'
    JSON_SPECS_URL: str = 'https://git.embl.de/grp-gbcs/stocks-server/-/issues/558'

    def __init__(self, **kwargs):
        super(GeneCoreAssaySniffer, self).__init__(**kwargs)

    @classmethod
    def get_sniffer_description(cls) -> str:
        help_txt = f"""
         This sniffer looks for a json file matching {GeneCoreAssaySniffer.JSON_NAME_PATTERN} describing:
           - a unique Illumina assay and its details
           - the input samples  
           - the different FastQ files to be imported and their relationship with samples 
          The described FastQ files must exist in the same directory.
          The complete JSON description can be found at {GeneCoreAssaySniffer.JSON_SPECS_URL}
         """
        return help_txt

    @classmethod
    def is_multi_run_sniffer(cls) -> bool:
        return False

    @classmethod
    def get_supported_technology(cls) -> Technology:
        """
        :return: the technology this sniffer supports ie 'Technology.SEQUENCING'
        """
        return Technology.SEQUENCING

    @classmethod
    def get_supported_platforms(cls) -> List[str]:
        """
        :return: platforms: the list of Platform this sniffer supports
        """
        return ["ILLUMINA"]

    def get_json_schema(self, technology: Technology, platform: str) -> Any:

        if not self.is_sniffer_valid_for(technology, platform):
            raise ValueError(f"Unsupported technology/platform combination: {technology}/{platform}")

        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "http://www.embl.org/stocks/schemas/genecore-illumina.json",
            "title": "GeneCore Sequencing Data",
            "description": "This is a schema that describes the sequencing data released by EMBL GeneCore.",
            "type": "object",
            "properties": {
                "managed": {"type": "string"},
                "data": {
                    "description": "the different instrument runs",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "flowcell": {"type": "string"},
                            "runid": {"type": "string"},
                            "sequencer": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "model": {"type": "string"},
                                    "serialnumber": {"type": "string"},
                                    "runid": {"type": "string"}
                                },
                                "required": ["name", "model", "serialnumber"]
                            },
                            "producer": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"}
                                },
                                "required": ["name"]
                            },
                            "lanes": {
                                "description": "the different lanes of the flowcell",
                                "type": "array",
                                "items": {
                                    "description": "each item is a lane that will become an Assay in STOCKS",
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "lane": {"type": "integer"},
                                        "user": {"type": "string"},
                                        "email": {"type": "string", "format": "email"},
                                        "type": {"enum": ["single-end", "paired-end", "multi-end"]},
                                        "multiplexed": {"enum": ["true", "false"]},
                                        "readlength": {"type": "string"},
                                        "runmode": {"type": "string"},
                                        "demultiplexed": {"enum": ["true", "false"]},
                                        "samples": {
                                            "type": "object",
                                            "patternProperties": {
                                                "^.+$": {
                                                    "type": "object",
                                                    "properties": {
                                                        "barcode": {"type": "string"},
                                                        "genecoreid": {"type": "string"},
                                                        "genecorereaction": {"type": "string"},
                                                        "sampletype": {"type": "string"},
                                                        "applicationname": {"type": "string"}
                                                    },
                                                    "required": ["barcode"]
                                                }
                                            }
                                        },
                                        "filelist": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "name": {"type": "string"},
                                                    "format": {"type": "string"},
                                                    "sample": {"type": "string"},
                                                    "readtype": {
                                                        "enum": ["read_1", "read_2", "read_3", "read_4", "index_1",
                                                                 "index_2"]},
                                                    "mimetype": {"type": "string"},
                                                    "bytes": {"type": "integer"}
                                                },
                                                "required": ["name", "format", "sample", "readtype"]
                                            },
                                            "minItems": 1
                                        }
                                    },
                                    "required": ["user", "type", "multiplexed", "demultiplexed", "samples", "filelist"]
                                },
                                "minItems": 1,
                                "maxItems": 1
                            }
                        },
                        "required": ["flowcell", "runid", "sequencer", "producer", "lanes"]
                    },
                    "minItems": 1,
                    "maxItems": 1
                }
            },
            "required": ["managed", "data"]
        }

    @staticmethod
    def __decode_samples(sample_dict: dict) -> Dict[str, SequencingLibrary]:
        """
        converts the JSON representation in a list of SequencingLibrary

        :param sample_dict:
        :return:
        """
        samples: Dict[str, SequencingLibrary] = {}
        for key, value in sample_dict.items():
            lib: SequencingLibrary = SequencingLibrary(key, value['barcode'])
            if 'sampletype' in value:
                lib.sample_type = value['sampletype']
            if 'genecoreid' in value:
                lib.provider_sample_name = value['genecoreid']
            if 'genecorereaction' in value:
                lib.provider_sample_id = value['genecorereaction']
            if 'applicationname' in value:
                lib.application = value['applicationname']
            samples[key.replace("'", "")] = lib
        return samples

    @staticmethod
    def __decode_datasets(file_list: [], samples: Dict[str, SequencingLibrary], run_type: SequencingRunType,
                          data_dir: Path) -> List[Dataset]:
        datasets: Dict[str, Dataset] = {}  # map sample name to dataset
        collections: Dict[str, DatasetCollection] = {}  # map name to collection
        for values in file_list:
            file_format: str = values['format']
            mime_type = ""
            if 'mimetype' in values:
                mime_type = values['mimetype']
            byte = 0
            if 'bytes' in values:
                byte = values['bytes']
            if file_format == "fastq":
                df: DatasetFile = FastqFile(name=values['name'],
                                            uri=str(Path(data_dir, values['name'])),
                                            read_type=values['readtype'],
                                            mime_type=mime_type,
                                            byte=byte)
            else:
                df: DatasetFile = DatasetFile(name=values['name'],
                                              uri=str(Path(data_dir, values['name'])),
                                              mime_type=mime_type,
                                              byte=byte,
                                              filetype=file_format)

            sample = samples[values['sample']]
            collection_name: str = file_format + ' files'
            if collection_name not in collections:
                collections[collection_name] = DatasetCollection(name=collection_name)
            collection = collections[collection_name]
            # get or create a dataset
            if sample.name not in datasets:
                datasets[sample.name] = Dataset(name=f"{sample.name} {str(run_type)} {file_format} dataset",
                                                is_raw=(file_format == "fastq"),
                                                samples=[sample],
                                                collection=collection)

            dataset: Dataset = datasets[sample.name]
            dataset.add_datafile(df)
            datasets[sample.name] = dataset

        return list(datasets.values())

    def sniff_instrument_run_assays(self, dir_path: Path, group: str, username: Optional[str] = None) \
            -> List[InstrumentRun]:
        logger.debug(f"looking in {str(dir_path)}")
        # we expect JSON files like <flowcell>_lane<x>.json
        json_filenames_list = glob.glob(str(Path(dir_path, GeneCoreAssaySniffer.JSON_NAME_PATTERN)))
        logger.debug(json_filenames_list)
        if not len(json_filenames_list):
            raise AssayStructureError(
                f"Sniffer {self.get_sniffer_name()}: No JSON file found in directory {str(dir_path)}.")

        runs: List[InstrumentRun] = []
        for json_path in json_filenames_list:
            try:
                runs.append(self.load_run_from_json_file(Path(json_path), group, username=username))
            except ValueError:
                mess = f"AssaySniffer {self.get_sniffer_name()}: Parsing JSON file {json_path} failed."
                logger.exception(mess)
                raise AssayStructureError(mess)

        return runs

    def load_run_from_json_file(self, json_path: Path, group: str, username: str | None = None) -> InstrumentRun:
        owner: Optional[User] = None
        if username:
            owner = User(username=username, groups=[UserGroup(name=group)])
        # first load the file as a dict
        with open(json_path) as json_file:
            data = json.load(json_file)
            # validate JSON with json schema
            validate(data, schema=self.get_json_schema(Technology.SEQUENCING, "ILLUMINA"))

            managed = bool(data['managed'])
            payload = data['data']
            # the payload potentially holds many runs
            for run_data in payload:
                flowcell: str = run_data['flowcell']
                run_id: str = run_data['runid']
                instrument: Instrument = Instrument(name=run_data['sequencer']['name'],
                                                    model=run_data['sequencer']['model'],
                                                    serial_number=run_data['sequencer']['serialnumber'])
                run = InstrumentRun(name=run_id,
                                    managed=managed,
                                    technology=Technology.SEQUENCING,
                                    platform="ILLUMINA",
                                    instrument=instrument,
                                    producer=DataProducer(run_data['producer']['name']))
                if owner:
                    run.set_owner(owner=owner, also_set_group=True)
                else:
                    run.group = group

                for assay_dict in run_data['lanes']:
                    assay_lane: int = assay_dict['lane'] if 'lane' in assay_dict else 1
                    assay_name: str = assay_dict['name'] if 'name' in assay_dict else f"{flowcell}_lane{assay_lane}"
                    user: str = assay_dict['user']
                    email: str = assay_dict['email'] if 'email' in assay_dict else ""
                    if not owner:
                        owner = User(username=user, groups=[UserGroup(name=group)])
                    owner.email = email

                    run_type: SequencingRunType = SequencingRunType(assay_dict['type'])
                    multiplexed: bool = bool(assay_dict['multiplexed'])
                    demultiplexed: bool = bool(assay_dict['demultiplexed'])
                    read_length: str = assay_dict['readlength'] if 'readlength' in assay_dict else ""
                    run_mode: str = assay_dict['runmode'] if 'runmode' in assay_dict else ""
                    samples: Dict[str, SequencingLibrary] = self.__decode_samples(assay_dict['samples'])
                    datasets: List[Dataset] = self.__decode_datasets(assay_dict['filelist'],
                                                                     samples, run_type, json_path.parent)
                    # create an SequencingAssay
                    assay: SequencingAssay = SequencingAssay(name=assay_name,
                                                             flowcell=flowcell,
                                                             platform=run.platform,
                                                             datasets=datasets,
                                                             samples=list(samples.values()),
                                                             chemistry="",
                                                             instrumentrun=run,
                                                             lane=assay_lane,
                                                             multiplexed=multiplexed,
                                                             demultiplexed=demultiplexed,
                                                             runtype=run_type,
                                                             runmode=run_mode,
                                                             readlength=read_length
                                                             )
                    if owner:
                        assay.set_owner(owner=owner, also_set_group=True)
                    else:
                        assay.group = group

                    run.add_assay(assay)

        return run
