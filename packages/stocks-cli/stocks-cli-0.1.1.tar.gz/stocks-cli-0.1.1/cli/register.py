# -*- coding: utf-8 -*-
"""
The 'register' module of the CLI
"""
import fnmatch
import logging
import os.path
import sys
import traceback
from typing import Tuple

import typer
from time import gmtime, strftime
from cli import get_default_config_file_path, get_sniffer_plugin_dir_list
from stocks.assaysniffer.sniffers import *
from stocks.assaysniffer.registry import registry
from stocks.models import InstrumentModel, Instrument, InstrumentRun
from stocksapi.client import StocksClient
from stocksapi.exceptions import HTTPException, MultipleObjectMatchedError
from stocksapi.manager import StocksManager
from cli.config import get_config
from stocksapi.models import PyDatasetListPost
from cli.utils import ExtendedEnum, is_uuid, ModelType

logger = logging.getLogger(__name__)

# name of this module (as appearing on the command line) is the last part of the __name__ eg cli.config -> config
_MODULE_NAME = __name__.rsplit(".", 1)[-1]
# list of command names offered in this module
_CMD_LOAD_ASSAY = "assays"
_CMD_LOAD_DATASET_COLLECTION = "collection"

# enums for fixed choices
class SidecarMetadataFormats(ExtendedEnum):
    KeyValue = "KeyValue"

# create the CLI app
app = typer.Typer()

# init the sniffer registry with potential plugins
for p in get_sniffer_plugin_dir_list():
    registry.load_custom_plugins_from_plugin_base_dir(p)

for snif_name in registry.get_registered_sniffer_names():
    logger.info(f"Registered sniffer: {snif_name}")

#TODO: support loading on behald of other users as a super user
@app.command(_CMD_LOAD_ASSAY,
             short_help="Register one or more assays and associated raw data to an existing study.",
             help="""
     All assays must be of the same type/technology (e.g. 'sequencing') and platform (e.g. Illumina or Nanopore)
     and produced by a unique instrument run. It is recommended to first execute the command as a dry run to spot 
     potential issues. 
     The assay(s) information is extracted from a run directory obeying a structure recognized by a 'sniffer'. 
     You can either specify the sniffer to use (always preferred) or let the  tool iterate over all the sniffers 
     available for the technology at hand. 
     The optional and mutually exclusive run_id, instrument or instrument model can be provided when the sniffer 
     is not able to extract this information from the run directory.
     Finally, you may decide to only transfer the files/folders identified as dataset or to transfer the whole run 
     folder (--indir). The latter option allows to keep additional information that may be later registered as 
     datasets if need be.     
    """
             )
def sniff_assays_from_instrument_run(
        indir: Path = typer.Option(
            ...,
            "--indir",
            "-i",
            help="Path to the run directory containing the data to be parsed/sniffed. "
        ),
        technology: Technology = typer.Option(
            ...,
            "--technology",
            "-t",
            case_sensitive=False,
            help=f"The technology that produced this run directory; one of {Technology.list()}"
        ),
        platform: str = typer.Option(
            None,
            "--platform",
            "-p",
            case_sensitive=False,
            help=f"The platform that produced this run directory e.g. NANOPORE, ILLUMINA, ZEISS ..."
        ),
        study_id: str = typer.Option(
            ...,
            "--study",
            "-s",
            help="The UUID of the study to link the datasets to"
        ),
        instrument_key: Optional[str] = typer.Option(
            None,
            "--instrument",
            help="Name, code or UUID of the actual instrument (e.g. sequencer, microscope...) used to generate the "
                 "assay(s). This is ignored when --instrument-session is provided. This must exist in STOCKS."
        ),
        instrument_model_key: Optional[str] = typer.Option(
            None,
            "--instrument-model",
            help="Name or UUID of the instrument model (e.g. sequencer, microscope...) used to generate the assay(s). "
                 "This is ignored when --instrument or --instrument-session is provided. This must exist in STOCKS."
        ),
        instrument_session_id: Optional[str] = typer.Option(
            None,
            "--instrument-session",
            help="UUID of an existing instrument session (aka instrument run) to use, "
        ),
        dry_run: bool = typer.Option(
            False,
            "--dry",
            "-d",
            help="Do not perform real request. Only checks if the dir_path can be sniffed"),
        allow_pooled_samples: bool = typer.Option(
            True,
            "--allow-pooled/--reject-pooled",
            help="When pooled is allowed, the same sample can be the input of multiple datasets (within the same "
                 "dataset collection)"),
        transfer_whole_input_dir: bool = typer.Option(
            True,
            "--whole-dir_path/--dataset-only",
            help="Transfer the whole run dir_path. If false (--dataset-only), only dataset files are imported i.e. any other"
                 " file will be ignored"),
        sniffer_name: Optional[str] = typer.Option(
            None,
            "--name",
            "-n",
            help="Name of the sniffer to use, optional. If not given, a sniffer matching the given Technology/Platform"
                 " are used and the first returning a valid result is used"
        ),
        stocks_group_name: Optional[str] = typer.Option(
            None,
            "--group_name",
            "-g",
            help="Group name to use to load the data. By default, your primary group is used."
                 "Warning: the group name must match one of the groups listed by calling 'stocks-cli config show'. "
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path")
) -> None:
    """
    Register one or more assay and associated raw data to STOCKS. All assays must be of the same type i.e. same
    technology (e.g. 'sequencing') and platform (e.g. Illumina or Nanopore) and produced by a unique instrument run.
    The assay(s) are parsed from a run directory obeying a structure recognized by a 'sniffer'.
    """
    _config = get_config(Path(conf_file_path))
    #_default_unix_group = _config[_config["default"]]["unix_group"]
    client: StocksClient = StocksClient(_config)
    stocks_manager: StocksManager = StocksManager(client)
    logged_in_user: User = stocks_manager.logged_in_user
    if not stocks_group_name:
        stocks_group_name =  logged_in_user.get_primary_group().name
    elif stocks_group_name not in stocks_manager.logged_in_user.groups:
        raise typer.BadParameter(f"Invalid group name for user '{logged_in_user.username}' : "
                                 f"'{stocks_group_name}'. The group must be one of "
                                 f"{list(logged_in_user.groups)}")

    logger.debug(indir)
    if not check_valid_directory(indir):
        raise typer.BadParameter(f"Invalid directory path: {str(indir)}")
    if not os.access(str(indir), os.R_OK):
        raise typer.BadParameter(f"Directory cannot be read: {str(indir)}")

    # Check given id is really a study
    invalid_study = False
    try:
        if not is_uuid(study_id):
            try:
                # try fetch by name
                o: dict | None = stocks_manager.fetch_item_by_name(name=study_id, model=ModelType.STUDY)
                if o and 'id' in o:
                    logging.debug(f"Fetched study {o} for name {study_id}")
                    study_id = o['id']
                else:
                    raise typer.BadParameter(f"No studies returned for --study {study_id} ; please use UUID")
            except MultipleObjectMatchedError as e:
                raise typer.BadParameter(f"{ len(e.results)} studies returned for --study {study_id}")

        study = stocks_manager.fetch_study(study_id)

        if not study:
            invalid_study = True
    except HTTPException as e:
        logger.error(f"Error while fetching study with id {study_id}: {e.detail}")
        invalid_study = True

    if invalid_study:
        raise typer.BadParameter(f"No study returned for --study {study_id}")

    # Check if session, instrument or model is provided, with session superseeding instrument superseeding model
    session: InstrumentRun = None
    instrument: Instrument = None
    instrument_model: InstrumentModel = None
    if instrument_session_id:
        if not is_uuid(instrument_session_id):
            raise typer.BadParameter(f"Provided run/session UUID {instrument_session_id} is not a valid UUID",
                                     param_hint="--instrument-session")
        try:
            session = stocks_manager.fetch_instrument_run(instrument_session_id)
        except Exception:
            logger.error(f"Error:\n {traceback.format_exc()}")
            raise typer.BadParameter(f"No valid session found with run/session UUID {instrument_session_id}",
                                     param_hint="--instrument-session")
    elif instrument_key:
        instrument = _lookup_instrument_by_uuid_code_or_name(
            stocks_manager=stocks_manager, instrument_key=instrument_key)
    elif instrument_model_key:
        instrument_model = _lookup_instrument_model_by_uuid_or_name(
            stocks_manager=stocks_manager, instrument_model_key=instrument_model_key, technology=technology
        )
    # end of --instrument-session --instrument and --instrument-model checks


    ####################
    # one sniffer name was given
    ####################
    runs: List[InstrumentRun] = None
    if sniffer_name:
        sniffer: AssaySniffer = registry.get_sniffer_instance(sniffer_name)
        if not sniffer:
            raise typer.BadParameter(f"Unknown sniffer name: {sniffer_name}. "
                                     f"Registered sniffers: {registry.get_registered_sniffer_names()}")

        if not sniffer.is_sniffer_valid_for(technology=technology, platform=platform):
            raise typer.BadParameter(f"Sniffer '{sniffer_name}' is not valid for technology/platform:"
                                     f" {technology}/{platform}.")
        # looks good, snif the dir_path
        try:
            runs = sniffer.sniff_instrument_run_assays(
                dir_path=indir, username=logged_in_user.username, group=stocks_group_name)
        except AssayStructureError as err:
            logger.error(str(err))
            print(f"The data in {str(indir)} does not comply to the sniffer {sniffer_name} expectations!")
            sys.exit(1)

        if not runs or len(runs) == 0:
            raise typer.BadParameter(f"Sniffer '{sniffer_name}' could not detect any assay i.e. data in {str(indir)} "
                                     f"is not recognized by this sniffer.")
        if len(runs) > 1:
            raise typer.BadParameter(f"Sniffer '{sniffer_name}' detected {len(runs)} instrument runs in the directory"
                                     f" {str(indir)}. Loading mutliple runs at once is not supported; please call"
                                     f" the {_CMD_LOAD_ASSAY} command on a folder containing results for a unique run")

    else:
        ####################
        # loop over sniffers and try !
        ####################
        for sniffer_cls in registry.get_sniffers():
            # get instance
            sniffer = sniffer_cls()
            logger.debug(sniffer)
            if sniffer.is_sniffer_valid_for(technology=technology, platform=platform):
                # looks good, snif the dir_path
                try:
                    runs: List[InstrumentRun] = sniffer.sniff_instrument_run_assays(dir_path=indir,
                                                                                    username=logged_in_user.username,
                                                                                    group=stocks_group_name)
                except AssayStructureError as err:
                    logger.debug(str(err))
                    logger.debug(f"Sniffer {sniffer.__class__.__name__} raised an error while sniffing {str(indir)}."
                                 f" Trying next sniffer.")
                    continue

                if not runs or len(runs) == 0:
                    logger.debug(
                        f"Sniffer {sniffer.__class__.__name__} did not find run in {str(indir)}. Trying next sniffer.")
                    continue

                if len(runs) > 1:
                    logger.error(
                        f"Sniffer {sniffer.__class__.__name__} detected {len(runs)} instrument runs in directory"
                        f" {str(indir)}. Loading multiple runs at once is not supported; please call"
                        f" the {_CMD_LOAD_ASSAY} command on a folder containing results for a unique run")
                    continue

                # we have a unique run, good!post this and let the server complains if something wrong !
                logger.info(
                    f"Sniffer {sniffer.__class__.__name__} found a run in {str(indir)}, submitting to STOCKS...")
                break


        submitted: bool = False
        try:
            if runs and len(runs) == 1:
                # we have a unique run in 'runs', good!post this and let the server complains if something wrong !

                # we first need to register the assays and for this, we need to have a run or a model
                the_run: InstrumentRun = runs[0]
                # do we need to look up for instrument (ie user did not pass this as option) ?
                if not session and not instrument and not instrument_model:
                    instrument, instrument_model = _fetch_instrument_or_model_info_from_sniffed_data(
                        stocks_manager=stocks_manager, run=the_run, technology=technology)
                # at this point we must have a session, an instrument or a model
                existing_run: SimpleInstrumentRun = None
                if session:
                    existing_run = session
                elif instrument:
                    the_run.instrument = instrument
                elif instrument_model:
                    # we force the instrument model and there is no proper instrument_run for assays
                    the_run.instrument = None
                    for assay in the_run.assays:
                        assay.instrumentrun = None
                        assay.instrumentmodel = instrument_model

                if not dry_run:
                    # let s create a run to use for all assays if needed (if instrument...)
                    if not existing_run and instrument:
                        # check if we have this run already. This could happen if eg (1) assays are loaded separately while
                        # from the same run or (2) when re-running code after failure (with run created before).
                        existing_runs: List[InstrumentRun] = stocks_manager.list_instrument_runs(
                            name=the_run.name, instrument_name=instrument.name, owner=logged_in_user.username)
                        if existing_runs and len(existing_runs) > 0:
                            existing_run = existing_runs[0]
                        else:
                            existing_run = stocks_manager.save_instrument_run(
                                name=the_run.name, instrument=instrument, description=the_run.description,
                                start_datetime=the_run.start_datetime, end_datetime=the_run.end_datetime,
                                producer=the_run.producer
                            )
                    # now we save all assays to the run
                    for assay in the_run.assays:
                        # when needed:
                        # assay.owner = logged_in_user
                        # assay.owned_by = ..
                        assay.id = stocks_manager.save_assay(assay=assay, instrument_run=existing_run)

                    res = stocks_manager.register_raw_assay_datasets(
                        instrument_run=runs[0], run_dir=indir, username=logged_in_user.username, unixgroup=stocks_group_name,
                        allow_pooled_samples=allow_pooled_samples, transfer_whole_input_dir=transfer_whole_input_dir,
                        study=study)
                    logger.debug(res)

                    submitted = True
                else:
                    o: PyDatasetListPost = stocks_manager._create_instrument_run_post(
                        instrument_run=runs[0], run_dir=indir, owner=logged_in_user.username, owned_by_group=stocks_group_name,
                        allow_pooled_samples=allow_pooled_samples, transfer_whole_input_dir=transfer_whole_input_dir,
                        study_id=study_id)
                    logger.warning("Dry-run: would submit payload (JSON):")
                    logger.warning("\n" + o.json(exclude_none=True, exclude_unset=True))
                    submitted = True
        except Exception:
            logger.error(f"Error:\n {traceback.format_exc()}")
            logger.error(f"An unexcepted error occurred, please check error logs.")
            exit(1)


    if not submitted:
        logger.warning(f"Could not find a suitable sniffer for {str(indir)}. Sorry. You are welcome to contribute one.")
    elif dry_run:
        logger.warning("Dry-run: looking good!")


def _fetch_instrument_or_model_info_from_sniffed_data(
        stocks_manager: StocksManager, run: InstrumentRun, technology: Technology, platform: str = None
) -> Tuple[Instrument, InstrumentModel]:
    """
    looks in the server to try to identify the instrument or instrument model matching info in the sniffed run
    returns a Tuple (Instrument, InstrumentModel) of which only one is not None
    """
    instrument: Instrument = None
    instrument_model: InstrumentModel = None
    # the user did not provided this info, let's see if we can look this up with sniffed info
    unknown_instrument = run.instrument
    instrument = _lookup_instrument_by_code(stocks_manager, code=unknown_instrument.serial_number)
    if not instrument:
        instrument = _lookup_instrument_by_name(stocks_manager, unknown_instrument.name, technology)

    # if still no instrument, we fall back on model
    if not instrument:
        logging.warn(f"No instrument registered for {unknown_instrument.as_simple_json()}.{os.linesep}"
                     f"We warmly recommend to register this instrument using the Web UI")
        instrument_model = _lookup_instrument_model_by_name(stocks_manager, unknown_instrument.model,
                                                            technology)
    if not instrument_model:
        logging.warn(f"No instrument model registered for {run.instrument.model} and technology "
                     f"{str(technology)}.{os.linesep}"
                     f"We warmly recommend to register this instrument model using the Web UI")
        # we use default model
        try:
            instrument_model = stocks_manager.list_instrument_models(technology=technology,
                                                                     platform="UNKNOWN")[0]
            logging.info(f"Will default to model: {os.linesep} {instrument_model.as_simple_json()}")
        except IndexError as e:
            # no model was returned!
            logging.fatal(f"No instrument model defined in server for technology={technology.value} and the"
                          f" platform=UNKNOWN. Such 'UNKNOWN' instrument models are expected for each "
                          f"technology. Please report this message to admin.")
            sys.exit(1)

    return (instrument, instrument_model)

def _lookup_instrument_model_by_uuid_or_name(stocks_manager: StocksManager, instrument_model_key: str,
                                             technology: Technology, platform: str = None) \
        -> InstrumentModel | None:
    """
    try to find an instrument by UUID, code or name (in this order) using provided key
    :param stocks_manager
    :param instrument_model_key a uuid, code or name. If None the method return None

    """
    if not instrument_model_key:
        return None

    instrument_model: InstrumentModel = None
    if is_uuid(instrument_model_key):
        data = stocks_manager.resolve(uuid=instrument_model_key)
        if not data:
            raise typer.BadParameter(f"UUID provided as --instrument-model is not valid for this server:"
                                     f" {instrument_model_key}")
        resolved_type: str = data['model_name']
        if resolved_type != "instrumentmodel":
            raise typer.BadParameter(f"UUID provided as --instrument-model '{instrument_model_key}' does not point "
                                     f"to a valid equipment model but to {resolved_type}")
        instrument_model = stocks_manager.fetch_instrument_model(data['id'])
        return instrument_model

    # look up by name
    results: List[InstrumentModel] = \
        stocks_manager.list_instrument_models(name=instrument_model_key, technology=technology, platform=platform)
    if results and len(results) == 1:
        instrument_model = results[0]
    elif results and len(results) > 1:
        raise typer.BadParameter(f"key provided as --instrument-model '{instrument_model_key}' matches"
                                 f" {len(results)} instrument models, please use UUID to disambiguate")
    else:
        raise typer.BadParameter(f"key provided as --instrument-model '{instrument_model_key}' did not match "
                                 f"any instrument, please use UUID to disambiguate")

    if instrument_model:
        logger.debug(f"Will use instrument model: {instrument_model.as_simple_json()}")
    return instrument_model

def _lookup_instrument_model_by_name(stocks_manager: StocksManager, name: str, technology: Technology
                                     ) -> Instrument | None:
    """
    only return an InstrumentModel if a unique instrument model matches this name for the given technology
    """
    if not name:
        return None

    results: List[InstrumentModel] = stocks_manager.list_instrument_models(name=name, technology=technology)
    if results and len(results) == 1:
        return results[0]

    return None

def _lookup_instrument_by_uuid_code_or_name(stocks_manager: StocksManager, instrument_key: str) -> Instrument | None:
    """
    try to find an instrument by UUID, code or name (in this order) using provided key
    :param stocks_manager
    :param instrument_key a uuid, code or name. If None the method return None

    """
    if not instrument_key:
        return None

    instrument: Instrument = None
    if is_uuid(instrument_key):
        data = stocks_manager.resolve(uuid=instrument_key)
        if not data:
            raise typer.BadParameter(f"UUID provided as --instrument is not valid for this server:"
                                     f" {instrument_key}")
        resolved_type: str = data['model_name']
        if resolved_type != "equipment":
            raise typer.BadParameter(f"UUID provided as --instrument '{instrument_key}' does not point "
                                     f"to an equipment item but to {resolved_type}")
        instrument = stocks_manager.fetch_equipment(data['id'])
        return instrument

    # look up by code
    results: List[Instrument] = stocks_manager.list_instruments(code=instrument_key)
    if not results:
        # look up by name
        results = stocks_manager.list_instruments(name=instrument_key)

    if results and len(results) == 1:
        instrument = results[0]
    elif results and len(results) > 1:
        raise typer.BadParameter(f"key provided as --instrument '{instrument_key}' matches {len(results)} "
                                 f"instruments, please use UUID to disambiguate")
    else:
        raise typer.BadParameter(f"key provided as --instrument '{instrument_key}' did not match any instrument"
                                 f", please use UUID to disambiguate")

    if instrument:
        logger.debug(f"Will use instrument: {instrument.as_simple_json()}")
    return instrument


def _lookup_instrument_by_code(stocks_manager: StocksManager, code: str) -> Instrument | None:
    """
    only return an Instrument if a unique instrument matches this code
    """
    if not code:
        return None

    results: List[Instrument] = stocks_manager.list_instruments(code=code)

    if results and len(results) == 1:
        return results[0]

    return None


def _lookup_instrument_by_name(stocks_manager: StocksManager, name: str, technology: Technology) -> Instrument | None:
    """
    only return an Instrument if a unique instrument matches this name for the given technology
    """
    if not name:
        return None

    results: List[Instrument] = stocks_manager.list_instruments(technology=technology, name=name)
    if results and len(results) == 1:
        return results[0]

    return None

@app.command(_CMD_LOAD_DATASET_COLLECTION,
             help="Ingest a collection of 'derived' datasets from a folder located in the user's dropbox (or from "
                  "whitelisted paths for trusted submission sources like facilities). All "
                  "datasets are associated to a unique dataset collection and should be of the same type."
                  " A typical use case is to load all the datasets generated by a unique workflow step i.e. all datasets"
                  " having the same type and sharing the workflow step parameters metadata. "
                  # "Optionally, sidecar files describe dataset specific annotations; these are parsed and also "
                  # "registered with a separate 'sidecar' collection. Optional metadata pattern "
                  # "may be provided to register metadata files (these are associated to a separate "
                  # "metadata collection)."
             )
def load_dataset_collection(
        in_dir: Path = typer.Option(
            ...,
            "--indir",
            "-i",
            help="Full path to the run directory containing the data to be registered. For security issues, this"
                 " directory must be in one of your dropboxes or a whitelisted pathes for trusted services (in which "
                 "case you must also be using a trusted account); else STOCKS will refused data ingestion."
        ),
        collection_name: str = typer.Option(
            ...,
            "--collection-name",
            "-c",
            help="The name of the dataset collection e.g. 'Aligned reads with STAR (bam)'"
        ),
        study_id: str = typer.Option(
            ...,
            "--study",
            "-s",
            help="The UUID of the study to link the datasets to"
        ),
        pattern: str = typer.Option(
            "*",
            "--pattern",
            "-p",
            help="Name pattern e.g. '*.bam', DO NOT forget the simple quotes! "
                 "Every file/folder matching the pattern will be loaded as a new dataset."
        ),
        # meta_pattern: List[str] = typer.Option(
        #     None,
        #     "--meta-pattern",
        #     "-m",
        #     help="Pattern(s) to identify metadata files e.g. '*.log', DO NOT forget the simple quotes! "
        #          "Every file matching this pattern will be registered as a metadata dataset."
        # ),
        recursive: bool = typer.Option(
            False,
            "--recursive",
            "-r",
            help="Whether input dir should be recursively inspected (i.e. looking in sub-folders)."
        ),
        search_files: bool = typer.Option(
            False,
            "--search-files/--ignore-files",
            help="Are we looking for files?"
        ),
        search_folders: bool = typer.Option(
            False,
            "--search-folders/--ignore-folders",
            help="Are we looking for folders?"
        ),
        dataset_type: str = typer.Option(
            "generic",
            "--type",
            "-t",
            help="Associates all found datasets (files or folders) to this dataset type."
                 " Note that the dataset type is not the same as the dataset file format. For example a dataset of "
                 "type 'paired-end fastq' is composed of two files which format are 'fastq' "

        ),
        datafile_format: str = typer.Option(
            None,
            "--format",
            "-f",
            help="Associates all found dataset files to this format i.e. no matter their extension."
                 " For files, data file format defaults to the file extension e.g. 'bam' unless this option is given."
                 " This option is mandatory if --search-folders is used. "
                 " Note that the dataset type is not the same as the dataset file format. For example a dataset of "
                 "type 'paired-end fastq' is composed of two files which format are 'fastq' "
        ),
        dry_run: bool = typer.Option(
            True,
            "--dry/--no-dry",
            help="Dry run i.e. only tell what would be done."),
        transfer_whole_input_dir: bool = typer.Option(
            True,
            "--whole-dir_path/--dataset-only",
            help="Transfer the whole input dir_path. If false (--dataset-only), only datasets are imported i.e. other"
                 " files & folders will be ignored. Note that relative path to the input dir is always preserved unless"
                 "--flatten is passed."),
        # sidecar_annotation_extension: str= typer.Option(
        #     None,
        #     "--sidecar-extension",
        #     help="extension of the dataset's sidecar metadata file e.g. 'info' would identify either "
        #          "'dataset1.bam.info' or 'dataset1.info' as a sidecar metadata file for dataset1.bam"),
        # sidecar_annotation_format: SidecarMetadataFormats = typer.Option(
        #     None,
        #     "--sidecar-format",
        #     help= f"the format of the sidecar metadata files. One of { SidecarMetadataFormats.list() } "),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path")
) -> None:
    """
    Register one or more non-raw datasets to STOCKS.
    """

    if not search_files and not search_folders:
        raise typer.BadParameter("Provide one of --search-files or --search-folders")

    if search_files and search_folders:
        raise typer.BadParameter(f"Cannot look for file and folder at the same time! "
                                 f"Give only one of --search-files or --search-folders")

    if search_folders and not datafile_format:
        raise typer.BadParameter(f"--datafile_format is mandatory with --search-folders option")

    _config = get_config(Path(conf_file_path))
    _username: str = _config[_config["default"]]["username"]

    client: StocksClient = StocksClient(_config)
    stocks_manager: StocksManager = StocksManager(client)

    logger.debug(in_dir)
    if not check_valid_directory(in_dir):
        raise typer.BadParameter(f"Invalid directory path: {str(in_dir)}")
    if not os.access(str(in_dir), os.R_OK):
        raise typer.BadParameter(f"Directory cannot be read: {str(in_dir)}")

    # Check given id is really a study
    invalid_study = False
    try:
        study = stocks_manager.fetch_study(study_id)
        if not study:
            invalid_study = True
    except HTTPException as e:
        logger.error(f"Error while fetching study with id {study_id}: {e.detail}")
        invalid_study = True

    if invalid_study:
        raise typer.BadParameter(f"No study returned for --study {study_id}")

    # validate dropbox and group
    # get dropboxes for user and that in_dir is in one of the user's dropbox
    dropboxes: dict[str, str] = stocks_manager.list_dropboxes(for_username=_username)

    # check in_dir is in a user's dropbox (also validating the user belong to the group)
    the_groupname = None
    for g_name, box_path in dropboxes.items():
        if str(in_dir).startswith(os.path.abspath(box_path) + os.sep):
            the_groupname = g_name

    if not the_groupname:
        dropboxes_multiline = ""
        for k, v in dropboxes.items():
            dropboxes_multiline = dropboxes_multiline + f"{k} -> {v}" + os.linesep
        raise typer.BadParameter(f"You are trying to load data that is not in any of your Dropbox. "
                                 f"This is not supported, please move the data in one of your dropbox first : {os.linesep}"
                                 f"{dropboxes_multiline}")

    now = strftime("%Y-%m-%d_%Hh%Mm", gmtime())
    collection: DatasetCollection = DatasetCollection(
        name=f"{collection_name}", description=f"Datasets batch loaded from {in_dir}")
    datasets : List[Dataset] = []
    for datafile_path in find_files(directory=in_dir, pattern=pattern, recursive=recursive,
                        search_files=search_files, search_directories=search_folders):
        p: Path = Path(datafile_path)
        size = 0
        if search_files:
            size = os.path.getsize(datafile_path)
        ds_name, stripped_ext = remove_extension(p.name)
        stripped_ext = stripped_ext.lstrip(".")
        now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        descr = f"Imported from {datafile_path} on {now}"
        dataset_file: DatasetFile = DatasetFile(name=p.name, uri=datafile_path, is_dir=search_folders,
                                                mime_type=stripped_ext, byte=size,
                                                filetype=datafile_format if datafile_format else stripped_ext)
        dataset: Dataset = Dataset(name=ds_name, is_raw=False, description=descr, datafiles=[dataset_file],
                                   collection=collection,
                                   dataset_type=dataset_type)
        datasets.append(dataset)

    collection.datasets = datasets

    if not datasets or not len(datasets):
        raise typer.BadParameter(f"Could not find a single datasets. Please check your input!")

    stocks_manager.register_derived_datasets(
        collections=[collection],
        run_dir = in_dir,
        username=_username,
        transfer_whole_input_dir=transfer_whole_input_dir,
        study=study,
        group=the_groupname
    )

def find_files(directory, pattern, recursive=True, search_files=True, search_directories=False):
    """
    Recursively finds files or directories that match a specified pattern in a specified directory.

    Args:
        directory (str): The directory to search in.
        pattern (str): The pattern to match file or directory names against.
        recursive (bool, optional): Whether to search recursively or not. Defaults to True.
        search_files (bool, optional): Whether to search for files or not. Defaults to True.
        search_directories (bool, optional): Whether to search for directories or not. Defaults to False.

    Yields:
        str: The full path of each file or directory that matches the pattern.
    """
    if recursive:
        walker = os.walk(directory)
    else:
        walker = [(directory, [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))],
                   [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])]
    for root, dirs, files in walker:
        if search_files and not search_directories:
            for file_name in files:
                if fnmatch.fnmatch(file_name, pattern):
                    yield os.path.join(root, file_name)
        elif search_directories and not search_files:
            for dir_name in dirs:
                if fnmatch.fnmatch(dir_name, pattern):
                    yield os.path.join(root, dir_name)
        elif search_directories and search_files:
            for dir_name in files + dirs:
                if fnmatch.fnmatch(dir_name, pattern):
                    yield os.path.join(root, dir_name)

def remove_extension(path) -> Tuple:
    """Remove the extension(s) from a file path.

    If the file name has one of the following compressed file extensions, both extensions will be removed:
    .zip, .gz, .bz2, .xz, .tar, .tar.gz, .tar.bz2, .tar.xz

    Args:
        path (str): The file path to remove the extension(s) from.

    Returns:
        tuple: A tuple containing the file path without any extensions and the stripped extension.
    """
    root, ext = os.path.splitext(path)
    stripped_ext = ""
    if ext in [".zip", ".gz", ".bz2", ".xz", ".tar", ".tar.gz", ".tar.bz2", ".tar.xz"]:
        root, stripped_ext = os.path.splitext(root)
        ext = stripped_ext + ext
    return root, ext

