import csv
import logging
import io
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Type
from collections import OrderedDict
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
import yaml
from dateutil.relativedelta import relativedelta
from enum import Enum

import cli
from stocks.models import Assay, Study, User, UserMember, Instrument, InstrumentRun, AnnotationType, Protocol, \
    SequencingAssay, StocksCVTerm, OntologyTerm, Ontology, OwnableMixin
from stocksapi.exceptions import HTTPException, SubProcessError
from stocksapi.manager import StocksManager
from cli.utils import Technology, UserRole, HTMLFilter, SequencingRunType, ModelType

logger = logging.getLogger(__name__)

ENA_CREDENTIALS_FILE = 'ena_credentials.yml'
COMMENT_STOCKS_UUID = 'Comment[stocks_uuid]'
MAGETAB_RELEASE_DATE = (datetime.today() + relativedelta(years=1)).strftime('%d-%m-%Y')
MAGETAB_HEADER_IDF_PROTOCOL = ["Protocol Name", "Protocole Type", "Protocol Description", "Protocol Hardware",
                               "Protocol Term Source REF", "Protocol Term Accession Number",
                               'Protocol Comment[stocks_uuid]']

MAGETAB_HEADER_IDF_DESIGN = ["Experimental Design", "Experimental Design Term Source REF",
                             "Experimental Design Term Accession Number"]

MAGETAB_HEADER_IDF_EXPERIMENTAL_FACTORS = ["Experimental Factor Name", "Experimental Factor Type",
                                           "Experimental Factor Term Source REF",
                                           "Experimental Factor Term Accession Number"]

MAGETAB_HEADER_IDF_USER_ROLES = ["Person Last Name", "Person First Name", "Person Middle Name",
                                 "Person Email", "Person Affiliation", "Person Roles"]

MAGETAB_HEADER_SINGLE_CELL_ANNOTARE = ['Single Cell Isolation', 'End Bias', 'Input Molecule', 'Primer', 'Spike In',
                                       'Spike in dilution', 'umi barcode read', 'umi barcode offset',
                                       'umi barcode size',
                                       'cdna read', 'cdna read offset', 'cdna read size', 'cell barcode read',
                                       'cell barcode offset', 'cell barcode size', 'sample barcode read',
                                       'sample barcode offset', 'sample barcode size']

UNDESIRED_ANNOTATIONS = ["emBASE ID", "emBASE URL"]
ENA_TABLES_NAME = ['study', 'sample', 'run', 'experiment']
ANNOTATION_STOCKS_ENA_STUDY = 'ena_study_accession'
ANNOTATION_STOCKS_ENA_BIOSTUDY = 'biostudies_accession'
ANNOTATION_STOCKS_ENA_RUN = 'ena_run_accession'
ANNOTATION_STOCKS_ENA_SAMPLE = 'ena_sample_accession'
ANNOTATION_STOCKS_BIOSAMPLE = 'biosamples_accession'
ANNOTATION_STOCKS_EXPERIMENT = 'ena_experiment_accession'

# TODO remove vars when finalized
EFO_ONTOLOGY = "EFO"
SEQUENCING_EFO_ID = "EFO_0004170"
SEQUENCING_EFO_DESCRIPTION = "nucleic acid sequencing protocol"
TERM_SOURCE_REF = "MGED Ontology"
QUALITY_SCORING_SYSTEM = 'phred'
LIBRARY_ENCODING = 'ascii'
ASCII_OFFSET = '@'
TODO = "# TODO"

runtype_layout_map = {
    SequencingRunType.PAIRED_END: 'PAIRED',
    SequencingRunType.SINGLE_END: 'SINGLE',
    SequencingRunType.MULTI_END: 'MULTI'
}


class StudyValidationReport:
    """
    Class with methods to check study metadata and collects booleans and relevant data relating to the study to be
    exported.
    """

    def __init__(self, study: Study):
        self.study: Study = study
        self.is_study_desc: bool = False
        self.is_protocols: bool = False
        self.protocols: List[str] = []
        self.protocol_types: Dict[str, bool] = {"growth protocol": False, "nucleic acid extraction protocol": False,
                                                "nucleic acid library construction protocol": False}
        self.unexpected_protocol_types: Dict[str, str] = {}
        self.is_assay: bool = False
        self.assays: List[str] = []
        self.is_annotations: bool = False
        self.is_factors: bool = False
        self.is_experimental_designs: bool = False
        self.annotation_check: Dict[str, Dict[str, Dict[str, bool]]] = {}
        self.sample_protocols_check: Dict[str, Dict[str, bool]] = {}
        self.data_check: Dict[str, Dict[str, bool]] = {}

    def validate_study(self, st: Study):
        if st.description:
            self.is_study_desc = True
        if st.experimental_design_terms:
            self.is_experimental_designs = True
        if st.experimental_factors:
            self.is_factors = True
        if st.protocols:
            self.is_protocols = True
        for protocol in st.protocols:
            if not protocol.description:
                self.protocols.append(protocol.name)
            if self.protocol_types.get(protocol.protocol_type.name) is not None:
                self.protocol_types[protocol.protocol_type.name] = True
            else:
                self.unexpected_protocol_types[protocol.name] = protocol.protocol_type.name
        if st.assays:
            self.is_assay = True
        for assay in st.assays:
            if not assay.description:
                self.assays.append(assay.id)

    def validate_annotations(self, df: pd.DataFrame) -> None:
        """
        Creates a dictionary for each samples, datasets and assays that contains a dictionary of annotation: bool
        with False indicating empty cells.
        Dictionary: {
            Sample: {
                <sample_name>: {
                    <annotation_name> : bool,
                    ...
                },
                ...
            },
            Assay: {
                ...
            },
            ...
        }
        """
        for h in ["Sample", "Assay", "Dataset"]:
            reg_annot = rf"{h}\[.+\]"
            if h == "Assay":
                h = "Assay Name"
            reg_id = rf"^{h}$"
            df_slice = df.filter(regex=f"{reg_id}|{reg_annot}").drop_duplicates()  # Get annotations and IDs columns
            dic = {}
            for _, row in df_slice.iterrows():
                row_dict = row.drop(h).astype(bool).to_dict()
                if row_dict:
                    only_annot = reg_annot[reg_annot.find("[") + 1:reg_annot.find("]")]
                    row_dict = {k[k.find("[") + 1:k.find("]")]: v for k, v in row_dict.items()}
                    dic[row[h]] = row_dict
            if dic:
                self.annotation_check[h] = dic
                self.is_annotations = True

    def validate_protocols(self, df: pd.DataFrame, study: Study) -> None:
        """
        Creates a dictionary for each sample, that contains a dictionary of protocol_type: bool
        with False indicating missing protocol type for that sample.
        Dictionary: {
            <sample>: {
                <protocol1>: bool,
                <protocol2>: bool,
                ...
            },
            ...
        }
        """
        dic = {}
        protocol_list = study.protocols
        df = df[["Sample", "Protocols"]].drop_duplicates()
        protocol_id_df: pd.DataFrame = df["Protocols"].str.split(",")
        protocol_id_to_type_map: Dict[str, str] = {}
        for protocol in protocol_list:
            protocol_id_to_type_map[protocol.id] = protocol.protocol_type.name
        df_slice: pd.DataFrame = pd.concat([df["Sample"], protocol_id_df], axis=1)
        for pt in self.protocol_types.keys():
            df_slice[pt] = df_slice["Protocols"].apply(
                lambda x: True if pt in [protocol_id_to_type_map.get(y, None) for y in x if x] else False)
        df_slice.drop("Protocols", axis=1, inplace=True)
        for _, row in df_slice.iterrows():
            row_dict = row.drop("Sample").astype(bool).to_dict()
            dic[row["Sample"]] = row_dict
        self.sample_protocols_check = dic

    def validate_data(self, df: pd.DataFrame) -> None:
        """
        Creates a dictionary for each datafile, that contains a dictionary of <any relevant column>: bool
        with False indicating empty cell for that column.
        Dictionary: {
            <datafile>: {
                <columns1>: bool,
                <columns2>: bool,
                ...
            },
            ...
        }
        """
        df_slice = df[["File Name", "Checksum"]]
        dic = {}
        for _, row in df_slice.iterrows():
            row_dict = row.drop("File Name").astype(bool).to_dict()
            dic[row["File Name"]] = row_dict
        self.data_check = dic


class Report:
    """
    Class that takes a ValidationReport as a parameter. Can then apply its methods to generate reports depending on the
     needs (eg magetab_report for a report relating to a magetab export).
     Reports structured in a list of SectionReport which are a list of Message.
    Report
    ├─ validation: ValidationReport
    └─ section_list: List[SectionReport]
       ├─ SectionReport
       │  ├── name: str
       │  ├── description: str
       │  ├── status: bool
       │  └── recap: List[Message]
       │      ├── Message
       │      │   ├── item: str
       │      │   ├── status: str
       │      │   ├── mess: str
       │      │   └── data [Optional]: Any
    """
    def __init__(self, validation: StudyValidationReport):
        self.validation: StudyValidationReport = validation
        self.section_list: List[SectionReport] = []

    def magetab_report(self):
        study_section: SectionReport = self._study_section()
        annotation_section: SectionReport = self._annotation_section()
        protocol_section: SectionReport = self._protocol_section()
        data_section: SectionReport = self._data_section()
        self.section_list.append(study_section)
        self.section_list.append(protocol_section)
        self.section_list.append(data_section)
        self.section_list.append(annotation_section)

    def _study_section(self):
        section_report = SectionReport(name='Study', description='Report for study validation', status=True)
        mess = None

        status = section_report.PASS
        if not self.validation.is_study_desc:
            section_report.status = False
            status = section_report.WARNING
            mess = "No description"
        section_report.add_message("Study description", status, mess)

        status = section_report.PASS
        if not self.validation.is_experimental_designs:
            section_report.status = False
            mess = "No experimental designs"
            status = section_report.ERROR
        section_report.add_message("Experimental designs", status, mess)

        status = section_report.PASS
        if not self.validation.is_assay:
            section_report.status = False
            status = section_report.ERROR
            mess = "No assay(s)"
        section_report.add_message("Assays", status, mess)

        status = section_report.PASS
        if not self.validation.is_factors:
            section_report.status = False
            status = section_report.WARNING
            mess = "No experimental factor(s)"
        section_report.add_message("Experimental factor(s)", status, mess)

        item = "Protocol"
        status = section_report.PASS
        check = True
        if not self.validation.is_protocols:
            section_report.status = check = False
            section_report.add_message(item, section_report.ERROR, "No protocols")

        if self.validation.protocols:
            section_report.status = check = False
            for p in self.validation.protocols:
                section_report.add_message(item, section_report.WARNING, f"Protocol '{p}' missing description")

        for k, v in self.validation.protocol_types.items():
            if not v:
                if k == "growth protocol":
                    section_report.status = check = False
                    section_report.add_message(item, section_report.ERROR, "No growth protocol")
                if k == "nucleic acid library construction protocol":
                    section_report.status = check = False
                    section_report.add_message(item, section_report.ERROR, "No library construction protocol")
                if k == "nucleic acid extraction protocol":
                    section_report.add_message(item, section_report.INFO, "No extraction protocol")
        if check:
            section_report.add_message(item, section_report.PASS)

        status = section_report.PASS
        if not self.validation.is_annotations:
            section_report.status = False
            status = section_report.ERROR
            mess = "No annotations"
        section_report.add_message("Annotations", status, mess)
        return section_report

    def _annotation_section(self):
        section_report = SectionReport(name='Annotations',
                                       description="Report for missing annotation in samples, assays and datasets",
                                       status=True)
        if not self.validation.is_annotations:
            section_report.status = False
            section_report.add_message("Annotations", section_report.ERROR, "No annotations were found")
            return section_report

        for k, v in self.validation.annotation_check.items():
            if v:
                err = section_report.WARNING
                mess = f"Some {k}s are missing annotations"
                for k2, v2 in v.items():
                    for k3, v3 in v2.items():
                        if not v3:
                            section_report.status = False
                            mess = f"'{k2}' missing annotation for {k3}"
                            section_report.add_message(k, section_report.WARNING, mess)
        return section_report

    def _protocol_section(self):
        section_report = SectionReport(name="Protocols", description="Report for missing protocols in samples",
                                       status=True)
        for sample, columns in self.validation.sample_protocols_check.items():
            for protocol_type, is_there in columns.items():
                if not is_there:
                    section_report.status = False
                    mess = f"'{sample}' missing '{protocol_type}'"
                    status = section_report.WARNING
                    if protocol_type == "nucleic acid extraction protocol":
                        status = section_report.INFO
                    section_report.add_message("Sample", status, mess)
        return section_report

    def _data_section(self):
        section_report = SectionReport(name="Data", description="Report for missing information relating to data",
                                       status=True)
        for datafile, columns in self.validation.data_check.items():
            for header, is_there in columns.items():
                if not is_there:
                    section_report.status = False
                    mess = f"'{datafile}' missing {header}"
                    section_report.add_message("Datafile", section_report.WARNING, mess)
        return section_report


class Message:
    def __init__(self, item: str, status: str, mess: str, data: Any):
        self.item: str = item
        self.status: str = status
        self.mess: str = mess
        self.data: Any = data


class SectionReport:
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    PASS = 'OK'

    def __init__(self, name: str, description: str, status: bool):
        self.name: str = name
        self.description: str = description
        self.status: bool = status
        self.recap: List[Message] = []

    def add_message(self, section: str, status: str, mess: str = None, data: Any = None) -> None:
        self.recap.append(Message(section, status, mess, data))


def write_report_file(report: Report, output_file_path: str):
    output_file_path = os.path.join(output_file_path, f"report_{report.validation.study.id}.txt")
    with open(output_file_path, 'w') as f:
        f.write(f"Study name:\t{report.validation.study.name}\n")
        f.write(f"Study ID:\t{report.validation.study.id}\n\n")

        # Write each section's status and messages
        for section in report.section_list:
            f.write(f"{section.name} checks:\n")
            f.write(f"Status: {'PASS' if section.status else 'FAIL'}\n")
            f.write(f"Description: {section.description}\n")
            if section.recap:
                f.write("Messages:\n")
            for message in section.recap:
                f.write(f"- {message.item} {message.status} {message.mess if message.mess else ''}\n")
                if message.data is not None:
                    f.write(f"- Data: {message.data}\n")
            f.write("\n")


def stocks_factor_format_name(s: str) -> str:
    """
    Takes a string, return mapped value to stocks_factor_to_efo if matching, else a non camelCase formated itself.
    e.g. 'AR Coating' -> 'array surface coating', 'SampleType' -> 'sample type'
    :param s:
    :return:
    """
    if s in stocks_factor_to_efo:
        return stocks_factor_to_efo[s].name
    return re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', s).lower().replace('  ', ' ')


def factor_efo_onto(term, url):
    term_id = url.split('/')[-1]
    onto = term_id.split("_")[0]
    return OntologyTerm(name=term, term_id=term_id, ontology=Ontology(name=onto, url=url))


stocks_factor_to_efo = {
    'Age': factor_efo_onto('age', 'http://www.ebi.ac.uk/efo/EFO_0000246'),
    'Antibody': factor_efo_onto('immunoprecipitate', 'http://www.ebi.ac.uk/efo/EFO_0000541'),
    # 'Antibody Source': (''),
    # 'AntibodyType': (''),
    # 'Applicable Organisms': (''),
    'AR Coating': factor_efo_onto('array surface coating', 'http://www.ebi.ac.uk/efo/EFO_0005069'),
    # 'CellLine': (''),
    'CellType': factor_efo_onto('cell type', 'http://www.ebi.ac.uk/efo/EFO_0000324'),
    # 'Compound': (''),
    # 'Compound Dose': (''),
    'DevelopmentalStage': factor_efo_onto('developmental stage', 'http://www.ebi.ac.uk/efo/EFO_0000399'),
    # 'DiseaseState': (''),
    # 'Donor ID': (''),
    # 'Donor Region': (''),
    # 'Epitope': ('Epitope', 'http://purl.obolibrary.org/obo/NCIT_C13189'),
    # 'Eukaryotic Selection': (''),
    # 'Focal Length': (''),
    # 'Gender': ('').
    # 'GeneOfInterest': (''),
    'Generation': factor_efo_onto('generation', 'http://www.ebi.ac.uk/efo/EFO_0000507'),
    'GeneticModification': factor_efo_onto('genetic modification', 'http://www.ebi.ac.uk/efo/EFO_0000510'),
    'Growth Media': factor_efo_onto('media', 'http://www.ebi.ac.uk/efo/EFO_0000579'),
    # 'Growth Time': (''),
    'individual': factor_efo_onto('individual', 'http://www.ebi.ac.uk/efo/EFO_0000542'),
    'IndividualGeneticCharacteristics': factor_efo_onto('genotype', 'http://www.ebi.ac.uk/efo/EFO_0000513'),
    'InitialTimePoint': factor_efo_onto('initial time point', 'http://www.ebi.ac.uk/efo/EFO_0004425'),
    # 'Organism': ('organism', 'http://purl.obolibrary.org/obo/OBI_0100026'),
    'OrganismPart': factor_efo_onto('organism part', 'http://www.ebi.ac.uk/efo/EFO_0000635'),
    # 'Pairing Key': (''),
    'Passage Number': factor_efo_onto('passage number', 'http://www.ebi.ac.uk/efo/EFO_0007061'),
    'Phenotype': factor_efo_onto('phenotype', 'http://www.ebi.ac.uk/efo/EFO_0000651'),
    # 'ppms_link': (''),
    # 'readtype': (''),
    # 'reagent': ('reagent', 'http://purl.obolibrary.org/obo/CHEBI_33893'),
    # 'SampleType': (''),
    # 'Sex': (''),
    'StrainOrLine': factor_efo_onto('strain', 'http://www.ebi.ac.uk/efo/EFO_0005135'),
    'Temperature': factor_efo_onto('temperature', 'http://www.ebi.ac.uk/efo/EFO_0001702'),
    # 'TreatmentConcentration': (''),
    'TreatmentTime': factor_efo_onto('time', 'http://www.ebi.ac.uk/efo/EFO_0000721'),
    'TreatmentType': factor_efo_onto('treatment', 'http://www.ebi.ac.uk/efo/EFO_0000727')
}

# Kept until change is made on 82
stocks_annotare_library_contruction_map = {
    "10x 3' transcription profiling v1": "10x 3' v1",  # value is ontology correct
    "10x 3' transcription profiling v2": "10x 3' v2",  # value is ontology correct
    "10x 3' transcription profiling v3": "10x 3' v3",  # value is ontology correct
    "10x 5' transcription profiling v1": "10x 5' v1",  # value is ontology correct
    "10x 5' transcription profiling v2": "10x 5' v2 (dual index)",  # value is ontology correct
    "10x Ig enrichment": "10x BCR enrichment",  # key is ontology correct
    "10x TCR enrichment": "10x TCR enrichment",
    "Visium Spatial Gene Expression": "10x Visium",  # key is ontology correct
    "10x scATAC-seq": "10x scATAC-seq",
    "CEL-seq": "CEL-seq",
    "CEL-seq2": "CEL-seq2",
    "CITE-seq": "CITE-seq",
    "CITE-seq (cell surface protein profiling)": "CITE-seq (cell surface protein profiling)",
    "CITE-seq (sample multiplexing)": "CITE-seq (sample multiplexing)",
    "DroNc-seq": "DroNc-seq",
    "Drop-seq": "Drop-seq",
    "inDrop": "inDrop",
    "MARS-seq": "MARS-seq",
    "microwell-seq": "Microwell-Seq",
    "scATAC-seq": "scATAC-seq",
    "scBS-seq": "scBS-seq",
    "scChIP-seq": "scChIP-seq",
    "sci-CAR": "sci-CAR",
    "sci-RNA-seq": "sci-RNA-seq",
    "SCRB-seq": "SCRB-seq",
    "Seq-Well": "Seq-Well",
    "single cell Hi-C": "single cell Hi-C",
    "Smart-seq2": "Smart-seq2",
    "SPLiT-seq": "SPLiT-seq",
    "STRT-seq": "STRT-seq"
}


def single_cell_annotare_fillin(library_construction: str) -> List[str]:
    """
    Matches the values of the column "Library Construction" with Annotare autofill values for the relevant following
    columns.
    Dictionary is stored in cli/annotare_fillin_table.csv. First column are the keys, first row is the header.
    """
    annotare_fillin_file = os.path.join('data/export_utils', 'annotare_fillin_table.csv')
    library_construction_values = {}
    with open(annotare_fillin_file) as f:
        reader = csv.reader(f)
        for row in reader:
            library_construction_values[row[0]] = row[1:]

    return library_construction_values.get(library_construction,
                                           ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])


class StudyExportFormat(str, Enum):
    magetab = "magetab"
    # enaxml = "enaxml"
    enatables = "enatables"
    # enaexcel = "enaexcel"
    tabular = "tabular"


def ena_credentials_file(ena_username, ena_password, ena_credentials, config_dir, export_dir) -> tuple[str, bool]:
    """
    Creates an ENA credential yaml file with username and password if provided.
    Else gets file at the location provided in ena_credentials.
    Else gets ENA credential yaml file path if it exists in either the export dir or the config dir.
    Else return None
    :return: The file path as well as a bool indicating whether the file was created by the method or not.
    """
    to_del_credentials = False
    if ena_username and ena_password:
        cred_file = os.path.join(export_dir, ENA_CREDENTIALS_FILE)
        while os.path.exists(cred_file):
            cred_file = os.path.join(cred_file, '_tmp')
        with open(cred_file, 'w') as c:
            yaml.dump({"username": ena_username, "password": ena_password}, c)
            c.close()
        to_del_credentials = True
    elif ena_credentials:
        cred_file = ena_credentials
    elif Path(config_dir, ENA_CREDENTIALS_FILE).exists():
        cred_file = os.path.join(config_dir, ENA_CREDENTIALS_FILE)
    elif Path(export_dir, ENA_CREDENTIALS_FILE).exists():
        cred_file = os.path.join(export_dir, ENA_CREDENTIALS_FILE)
    else:
        cred_file = None
    return cred_file, to_del_credentials


def create_fake_data(fake_dir, table):
    """
    Creates fake sequencing fastq format data for test submission to the ENA through the ena-upload-cli
    :param fake_dir:
    :param table:
    :return:
    """
    os.mkdir(fake_dir)
    for f in table['file_name']:
        # file = f'{fake_dir}{f}'
        file = os.path.join(fake_dir, f)
        f = open(file, 'w')
        f.write('@NB111111:111:XXXXXXXXX:1:11111:11111:1111 1:N:0:TTTTTTTT')
        f.write('CGGGGGGGGGGTTTTTTTTTTTAAAAAA')
        f.write('+')
        f.write('AAAAA#EEEEEEEEEEEEEEEEEEEEEE')
        f.close()


def create_idf_protocol(prot_obj_list: List[Protocol], assays: List[Assay | SequencingAssay]) -> pd.DataFrame:
    """
    Create the dataframe containing the protocol information to be written down in the IDF format file.
    :param prot_obj_list:
    :param assays:
    :return:
    """
    df = pd.DataFrame()
    df["header"] = MAGETAB_HEADER_IDF_PROTOCOL
    title_to_info: Dict[str, List] = {}
    # Writing assays
    # TODO other assay types
    if assays[0].technology == Technology.SEQUENCING:
        for assay in assays:
            if not assay.instrumentrun:
                logger.error(f'No instrument run found for sequencing assay ID: {assay.id}')
                df = pd.concat(
                    [df, pd.Series(['ERROR: No instrument run found', '', '', '', '',
                                    '', assay.id])], axis=1)
                continue
            model = assay.instrumentrun.instrument.model
            # e.g. Standard NextSeq 500 Paired End Sequencing
            assay_title = f'Standard {model} {assay.runtype.value} Sequencing'
            description = f'{assay.runtype.value} sequencing on {model}'
            if assay.platform.lower() not in description.lower():
                description = f'{assay.runtype.value} sequencing on {assay.platform.lower()} {model}'
            if title_to_info.get(assay_title):
                title_to_info[assay_title][0].append(assay.id)
            else:
                title_to_info[assay_title] = [[assay.id]]
            title_to_info[assay_title].append(model)
            title_to_info[assay_title].append(description)
        for title in title_to_info.keys():
            assay_info = title_to_info[title]
            df = pd.concat(
                [df, pd.Series([title, SEQUENCING_EFO_DESCRIPTION, assay_info[2], assay_info[1], EFO_ONTOLOGY,
                                SEQUENCING_EFO_ID, ";".join(assay_info[0])])], axis=1)
    # Writing protocols
    for obj in prot_obj_list:
        parse_text = HTMLFilter()
        if obj.summary:
            parse_text.feed(obj.summary)
        else:
            parse_text.text = f'ERROR: no summary was found'
            logger.error(f'No summary was found for protocol ID: {obj.id}')
        df = pd.concat(
            [df, pd.Series(
                [obj.name.strip('\n'), obj.protocol_type.name, f'{parse_text.text}', "",
                 obj.protocol_type.ontology.name, obj.protocol_type.term_id,
                 obj.id])], axis=1)
    df = df.fillna("")
    return df


def create_idf_design(study: Study) -> pd.DataFrame:
    """
    Create dataframe containing the study designs to be written in the IDF format file
    :param study:
    :return:
    """
    df = pd.DataFrame()
    df["header"] = MAGETAB_HEADER_IDF_DESIGN
    if not study.experimental_design_terms:
        logger.warning("Design terms are missing from the study")
    for term in study.experimental_design_terms:
        ed_onto = EFO_ONTOLOGY
        ed_onto_id = term.ontology_mappings.get(ed_onto)
        if not ed_onto_id:
            # get some random ontology
            ed_onto = ""
            ed_onto_id = ""
            onto = []
            onto_term = []
            for ontology in term.ontology_mappings.keys():
                onto.append(ontology)
                onto_term.append(term.ontology_mappings.get(ontology))
            if len(onto) > 0:
                ed_onto = onto[0]
                ed_onto_id = onto_term[0].term_id
        else:
            ed_onto_id = ed_onto_id.term_id
        df = pd.concat([df, pd.Series([term.name, ed_onto, ed_onto_id])], axis=1)
    df = df.fillna("")
    return df


def create_idf_experimental_factors(exp_fac: List[str]) -> pd.DataFrame:
    """
    Create dataframe containing the experimental factors of the study to be written in the IDF format file
    :param exp_fac: List of a study's experimental factors
    """
    df = pd.DataFrame()
    df["header"] = MAGETAB_HEADER_IDF_EXPERIMENTAL_FACTORS
    for i in exp_fac:
        name = stocks_factor_format_name(i)
        onto = stocks_factor_to_efo.get(i)
        col = [name, name, onto.ontology.name if onto else TODO, onto.term_id if onto else TODO]
        df = pd.concat([df, pd.Series(col)], axis=1)
    df = df.fillna("")
    return df


def create_idf_users(study: Study) -> pd.DataFrame:
    """
    Create dataframe containing the users of the study to be written in the IDF format file
    :param study:
    :return:
    """
    df = pd.DataFrame()
    df["header"] = MAGETAB_HEADER_IDF_USER_ROLES
    for user in study.user_roles.values():
        r = [role.value for role in user.roles]
        df = pd.concat([df, pd.Series([user.last_name, user.first_name, user.middle_name, user.email,
                                       user.institution, ";".join(r)])], axis=1)
    df = df.fillna("")
    return df


def write_df_in(outpath: Path, df: pd.DataFrame) -> None:
    """
    Function that appends the dataframe to the file in the right format
    :param outpath:
    :param df:
    :return:
    """
    df.to_csv(outpath, mode="a", header=False, index=False, sep="\t")
    f = open(outpath, "a")
    f.write("\n")
    f.close()


def add_default_submitter(study: Study) -> None:
    """
    Adds a default submitter (from the config file) as UserMember in the Study when exporting a magetab from Stocks
    :param study: Study object
    :return: None
    """
    default_email: str = cli.get_default_submitter_email()
    default_role: UserRole = UserRole.SUBMITTER
    name: str = f"{cli.get_default_submitter_firstname()} {cli.get_default_submitter_middlename()} \
                {cli.get_default_submitter_lastname()}"
    user: User = User(username=cli.get_default_submitter_lastname().lower(), email=default_email,
                      middle_name=cli.get_default_submitter_middlename(),
                      first_name=cli.get_default_submitter_firstname(), last_name=cli.get_default_submitter_lastname())
    default_user: UserMember = UserMember(user=user, roles={default_role})
    study.add_user(default_user)


def add_owner_role(study: Study) -> None:
    """
    add the owner of the study to the UserMember list of the study.
    :return:
    """
    owner: UserMember = UserMember(user=study.owner, roles={UserRole.SUBMITTER, UserRole.INVESTIGATOR})
    study.add_user(owner)


def process_assays(table: pd.DataFrame, study: Study, stocks_manager: StocksManager) \
        -> tuple[Dict[str, Assay | SequencingAssay], str | None]:
    """
    Retrieves model.Assay from their id and appends them to the study. Creates a dictionary of information,
    and validates the type.
    :return: Tuple containing dictionary assay_id : assay_information, and the assay_type
    :raises ValueError: Not all the assay are of the same type
    """
    assay_info_table: pd.DataFrame = table.drop_duplicates(
        subset=["Assay ID", "Instrument Model"])[["Assay ID", "Instrument Model"]]
    assay_dict: Dict[str, Assay] = get_assay_list(assay_info_table, study, stocks_manager)
    assay_type: str = check_assay_type(study.assays)
    if not assay_type:
        raise ValueError("Error with assay type value:"
                         "all assays of one study should be of the same platform (e.g. illumina)")
    return assay_dict, assay_type


def get_assay_list(assay_info_table: pd.DataFrame, study: Study, stocks_manager: StocksManager) \
        -> Dict[str, Assay]:
    """
    Appends a list of assays to the study object and create a dictionary of same assays with their id as keys.
    :param assay_info_table: Dataframe containing relevant subset of columns from the stocks export.
    :param study:
    :param stocks_manager:
    :return:
    """
    assay_list: List[Assay] = []
    assay_dict: Dict[str, Assay] = {}
    for row in assay_info_table.itertuples():
        logger.debug(f"Fetching assay ID: {row[1]}")
        assay = stocks_manager.fetch_assay(row[1], load_ownership=True)
        assay.description = parse_html(assay.description)
        instrument = Instrument(name='instrument', model=row[2])
        assay.instrumentrun = InstrumentRun(name='instrumentrun', instrument=instrument, technology=assay.technology,
                                            managed=True, platform=assay.platform)
        assay_list.append(assay)
        assay_dict[row[1]] = assay

    if not assay_list:
        raise ValueError(f"No assay were found in relation to the study {study.id}")
    study.assays = assay_list
    return assay_dict


def create_annofactor_df(annotations_dict: Dict[str, dict[str, AnnotationType | None | list[str] | bool]]) \
        -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Creates dataframes for annotations and experimental factors from the dictionary of annotations.
    :param annotations_dict:
        {
        "<annotation_type_name>": {
            "obj": <AnnotationType>,
            "data": [data]},
            "is_factor": bool
            }
        }
    """
    annotation_df = pd.DataFrame()
    factor_df = pd.DataFrame()
    for k, v in annotations_dict.items():
        annotation_df[f"Characteristics[{stocks_factor_format_name(k)}]"] = v["data"]
        if v["is_factor"]:
            factor_df[f"Factor Value[{stocks_factor_format_name(k)}]"] = v["data"]
    return annotation_df, factor_df


def extract_final_annotations(df: pd.DataFrame, annotations: List[AnnotationType]) \
        -> Dict[str, dict[str, AnnotationType | None | list[str] | bool]]:
    """
    Creates dictionary of final annotations from the information of the export table.
    Headers: "Sample[<annotation_type_name>]", "Assay[<annotation_type_name>]", "Dataset[<annotation_type_name>]".
    If an annotation is the same between samples, assay and dataset, the data kept will be datase > assay > sample.
    :param df: pandas.DataFrame of STOCKS metadata export
    :param annotations: List of stocks.model.AnnotationType
    :return: Dictionary structured as:
    {
    "<annotation_type_name>": {
        "obj": <AnnotationType>,
        "data": [data]},
        "is_factor": bool
        }
    }
    """
    extracted_annotations = {}
    for h in ["Sample", "Assay", "Dataset"]:
        reg = rf"{h}\[.+\]"
        df_slice = df.filter(regex=reg)
        for c in df_slice.columns:
            ann_header = c[c.find("[") + 1:c.find("]")]  # Get annotation name from header (between the [])
            if ann_header not in UNDESIRED_ANNOTATIONS:
                data = list(df_slice[c].values)
                extracted_annotations[ann_header] = {"data": data}
    for k, v in extracted_annotations.items():  # Getting the metadata's metadata
        obj: AnnotationType = next((ann for ann in annotations if ann.name == k), None)  # Matches with AnnotationType
        flt_data = [x for x in v["data"] if x and x.strip()]  # Remove empty strings from data
        ref = flt_data[0]
        is_factor: bool = not all(x == ref for x in flt_data)  # Bool if not all values of annotation are equal
        v["obj"] = obj
        v["is_factor"] = is_factor
    return extracted_annotations


def get_export_table(study_id: str, stocks_manager: StocksManager) -> pd.DataFrame:
    data = stocks_manager.fetch_study_dataset_csv_table(study_id)
    table: pd.DataFrame = arrayexpress_export_to_dataframe(data)
    if table.empty:
        raise ValueError(f"The arrayexpress export is empty for the study {study_id}")
    return table


def arrayexpress_export_to_dataframe(data: bytes) -> pd.DataFrame:
    """
    Convert the bytes file from stocks to a pandas dataframe. Merge the redundant columns.
    :param data:
    :return:
    """
    table = pd.read_table(io.BytesIO(data), dtype=str, sep=",", keep_default_na=False).fillna('').astype(str)
    if "Organism (Annotation)" not in table.columns:
        return table
    if 'Organism' not in table.columns:
        return table
    mask1 = table["Organism"].str.upper() == 'NONE'
    mask2 = table["Organism"].str.upper() == 'NA'
    mask3 = table["Organism"].str.upper() == 'NULL'
    mask4 = table["Organism"].str.strip() == ''
    mask = mask1 + mask2 + mask3 + mask4
    table.loc[mask, "Organism"] = table.loc[mask, "Organism (Annotation)"]
    table.drop(labels="Organism (Annotation)", axis=1, inplace=True)
    return table


def extract_protocol_list(table: pd.DataFrame, stocks_manager: StocksManager) -> List[Protocol]:
    """
    Fetch the list of protocols from stocks from the protocol id list present in the stocks export dataframe.
    :param table:
    :param stocks_manager:
    :return:
    """
    if table["Protocols"].isnull().values.all():
        logger.warning("No protocol ID are found in the export file")
        logger.debug(f"Protocols column printout: {table['Protocols'].to_string()}")
        return []
    elif table["Protocols"].isnull().values.any():
        logger.warning("Some samples do not have corresponding protocols ID in the export file")
        logger.debug(f"Protocols column printout: {table['Protocols'].to_string()}")

    protocol_id_list = pd.unique(table["Protocols"].str.split(",", expand=True).values.ravel())
    logger.debug(f"protocols ID list: {protocol_id_list}")

    protocol_list = []
    for protocol_id in protocol_id_list:
        if protocol_id:
            logger.info(f'Fetching protocol ID: {protocol_id}')
            fetch_protocol = stocks_manager.fetch_protocol(protocol_id)
            fetch_protocol.description = parse_html(fetch_protocol.description)
            fetch_protocol.summary = parse_html(fetch_protocol.summary)
            protocol_list.append(fetch_protocol)
    return protocol_list


def create_protocol_ref(df: pd.DataFrame, protocol_list: List[Protocol]) -> pd.DataFrame:
    """
    Processes the list of protocols in the format needed for a magetab export.
    :param df:
    :param protocol_list:
    :return:
    """

    def _sorter_to_ordered_list(sorter: Dict[str, set[str]]) -> List[str]:
        # Turns a dictionnary of hierarchical relations into a list sorted according to hierarchy.
        # Dictionary relations are: each id or type as key, and as value a set all the ones that follow it.
        ordered_list: List[str] = []
        for key in sorter.keys():
            if key not in ordered_list:
                check = 0
                for ordered_id_idx in range(len(ordered_list)):
                    if ordered_list[ordered_id_idx] in sorter[key]:
                        ordered_list.insert(ordered_id_idx, key)
                        check = 1
                        break
                if check == 0:
                    ordered_list.append(key)
        return ordered_list

    protocol_id_df: pd.DataFrame = df["Protocols"].str.split(",", expand=True)
    protocol_id_to_type_map: Dict[str, str] = {}
    protocol_id_to_name_map: Dict[str, str] = {}
    for protocol in protocol_list:
        protocol_id_to_type_map[protocol.id] = protocol.protocol_type.term_id
        protocol_id_to_name_map[protocol.id] = protocol.name

    # dictionary giving every protocol id as keys, and a set of all the protocol ids that comes after it as values.
    pid_sorter_dict: OrderedDict[str, set[str]] = OrderedDict()
    # dictionary giving every protocol type as keys, and a set of all the protocol types that comes after it as values.
    ptype_sorter_dict: OrderedDict[str, set[str]] = OrderedDict()
    for sample in protocol_id_df.itertuples(index=False):
        sample = [id for id in sample if id]
        if len(sample) == 0:
            continue
        for idx in range(len(sample) - 1):
            next_ptypes = pid_sorter_dict.get(sample[idx])
            if next_ptypes:
                next_ptypes.update(sample[idx + 1:])
            else:
                pid_sorter_dict[sample[idx]] = set(sample[idx + 1:])
        if not pid_sorter_dict.get(sample[-1]):
            pid_sorter_dict[sample[-1]] = set()
    for k in pid_sorter_dict.keys():
        if ptype_sorter_dict.get(protocol_id_to_type_map[k]):
            ptype_sorter_dict[protocol_id_to_type_map[k]].update(
                [protocol_id_to_type_map[id] for id in pid_sorter_dict[k]])
        else:
            ptype_sorter_dict[protocol_id_to_type_map[k]] = {protocol_id_to_type_map[id] for id in pid_sorter_dict[k]}

    # lists of protocol ids and types in order.
    ordered_ids: List[str] = _sorter_to_ordered_list(pid_sorter_dict)  # Order of the ids but not the types
    ordered_types: List[str] = _sorter_to_ordered_list(ptype_sorter_dict)  # Order of the types but not the ids
    protocol_type_to_id_map: Dict[str, List] = {}
    for id in ordered_ids:
        protocol_type = protocol_id_to_type_map.get(id)
        if not protocol_type_to_id_map.get(protocol_type):
            protocol_type_to_id_map[protocol_type] = [id]
        else:
            protocol_type_to_id_map[protocol_type].append(id)
    # True order
    reordered_ids = []
    for ot in ordered_types:
        for oid in protocol_type_to_id_map[ot]:
            reordered_ids.append(oid)

    # write full table -> all protocols in a separate column
    table: np.array = []
    for sample in protocol_id_df.itertuples(index=False):
        id_row = [id for id in sample if id]
        new_row = []
        if len(id_row) == 0:
            table.append([''])
            continue
        for oid in reordered_ids:
            if oid in id_row:
                new_row.append(oid)
            else:
                new_row.append('')
        table.append(new_row)

    # squish table -> merge columns of same type if possible
    table = pd.DataFrame(list(table)).fillna('').T
    pidx = 0
    while pidx < len(table.index) - 1:
        check = 0
        while check == 0 and pidx < len(table.index) - 1:
            if protocol_id_to_type_map[reordered_ids[pidx]] == protocol_id_to_type_map[reordered_ids[pidx + 1]]:
                for p1, p2 in zip(table.iloc[pidx], table.iloc[pidx + 1]):
                    if p1 and p2:  # Only one line needs both protocols present to keep columns separated.
                        check = 1
                        pidx += 1
                        break
                if check == 0:
                    new_col = [''.join(filter(None, [table.iloc[pidx][x],
                                                     table.iloc[pidx + 1][x]])) for x in range(len(table.iloc[pidx]))]
                    table.iloc[pidx] = new_col
                    reordered_ids.pop(pidx + 1)
                    table.drop(index=pidx + 1, inplace=True)
                    table = table.reset_index(drop=True)
            else:
                check = 1
                pidx += 1

    table = table.T
    table.fillna('', inplace=True)
    table = table.astype(str)
    table = table.applymap(lambda x: protocol_id_to_name_map[x] if x else '')
    table.columns = ["Protocol REF" for i in range(len(table.columns.values))]
    return table


def check_assay_type(assays: List[Assay]) -> None | str:
    """
    Takes a list of assays and check if all are the same type.
    :param assays:
    :return: Assay Platform if all types the same, or None.
    :raises ValueError if assays is empty.
    """
    if not assays:
        raise ValueError("Error with assay list: list null or empty.")
    assay_type: str = assays[0].platform
    for assay in assays:
        if assay_type is not assay.platform:
            logger.error(f"Error with assays types: 2 different assay types: {assay_type} and {assay.platform}")
            return None
    return assay_type


def add_user_institutions(study: Study) -> None:
    """
    adds institution from a config file to the study user members
    """
    for user in study.user_roles.values():
        if not user.institution:
            user.institution = cli.get_default_affiliation()


def owner_name(ownable: OwnableMixin) -> str:
    """
    Gets the full name or username of the owner of an ownable item
    """
    if not isinstance(ownable, OwnableMixin):
        raise TypeError(f"Item needs to be ownable")
    return user_name(ownable.owner)


def user_name(user: User | str) -> str:
    """
    Gets the full name or username or last name of a User
    """
    if isinstance(user, str):
        return user
    name = ''
    if user.first_name and user.last_name:
        if user.middle_name:
            name = f"{user.first_name} {user.middle_name} {user.last_name}"
        else:
            name = f"{user.first_name} {user.last_name}"
    elif user.username:
        name = user.username
    elif user.last_name:
        name = user.last_name
    return name


def check_table_bools(df: pd.DataFrame) -> tuple[bool, bool]:
    """
    Checks booleans values of the export table for each or all samples depending on the column.
    """
    check_single_cell = False
    check_spiked = False
    if 'Is Single Cell Sample' in df.columns:
        if len(pd.unique(df['Is Single Cell Sample'])) > 1:
            raise ValueError(f"Error: all samples should have the same value for 'Is Single Cell'."
                             f"Values founds: {pd.unique(df['Is Single Cell'])} ")
        if df['Is Single Cell Sample'].values.all() == 'True':
            check_single_cell = True
    if 'Is Spike In' in df.columns:
        if df['Is Spike In'].values.any() == 'True':
            check_spiked = True
    elif 'Kit name' in df.columns:  # TODO del this after Jelle implements spike in bool
        if df['Kit name'].values.any():
            check_spiked = True
    return check_single_cell, check_spiked


def merge_df_columns(col1: pd.Series, col2: pd.Series) -> pd.Series:
    """
    Takes 2 pandas series and paste the second over the first except for null values.
    :raises: TypeError if an argument is not a pandas.Series object. ValueError if both columns not same size.
    """
    if not type(col1) is pd.Series or not type(col2) is pd.Series:
        raise TypeError("Both arguments need to be pandas Series objs")
    if not len(col1) == len(col2):
        raise ValueError("Both columns need to be of same length")
    res = pd.concat([col1, col2], axis=1).apply(lambda x: x[1] if x[1] else x[0], axis=1)
    return res


def to_ena_format(table: pd.DataFrame, study: Study, assay_type: str, assay_dict: dict[str, SequencingAssay],
                  annotations_dict: Dict[str, dict[str, AnnotationType | None | list[str] | bool]],
                  stocks_manager: StocksManager, filter_sub: bool = True) \
        -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Creates the metadata tables with information relevant to a ENA submission via the ena-upload-cli.
    """
    protocol_id_to_description_map = {}
    for protocol in study.protocols:
        p_desc = protocol.description
        if not p_desc:
            p_desc = 'WARNING: No protocol description.'
        protocol_id_to_description_map[protocol.id] = p_desc.replace("#", "N.").strip()  # Problem with '#' in XML?
    super_protocol = table['Protocols'].apply(
        lambda x: ' ; '.join([p for p in [protocol_id_to_description_map.get(pid, '') for pid in x.split(',')]]))

    study_table = ena_study_df(study, stocks_manager, filter_sub)
    sample_table = ena_sample_df(table, study, super_protocol, annotations_dict, stocks_manager, filter_sub)
    runs_table = ena_runs_df(table, stocks_manager, filter_sub)
    exp_table = ena_experiment_df(table, study, assay_type, assay_dict, super_protocol, annotations_dict,
                                  stocks_manager, filter_sub)
    return study_table, sample_table, runs_table, exp_table


def ena_study_df(study: Study, stocks_manager: StocksManager, filter_sub: bool) -> pd.DataFrame | None:
    """
    Creates a dataframe containing the study informaiton relevant to a ENA submission.
    :return: None if filter_sub and study already possesses ENA or biostudies accession numbers, else dataframe.
    """
    study_ann_list = stocks_manager.list_annotations_from_item(ModelType.STUDY, study.id)
    ena_acc = ''
    biostudy_acc = ''
    for ann in study_ann_list:
        if ann['name'] == ANNOTATION_STOCKS_ENA_STUDY:
            ena_acc = ann['value']
        if ann['name'] == ANNOTATION_STOCKS_ENA_BIOSTUDY:
            biostudy_acc = ann['value']
    if ena_acc or biostudy_acc:
        if filter_sub:
            return None
        else:
            dic = {"alias": [study.id], "title": [study.name],
                   "study_type": ["Other"], "study_abstract": [study.description],
                   "ena_accession": [ena_acc], "biostudies_accession": biostudy_acc}
            return pd.DataFrame(dic)
    # TODO study_type
    dic = {"alias": [study.id], "title": [study.name], "study_type": ["Other"],
           "study_abstract": [study.description]}
    return pd.DataFrame(dic).replace({"#": "N."})


def ena_sample_df(table: pd.DataFrame, study: Study, super_protocol: pd.DataFrame,
                  annotations_dict: Dict[str, dict[str, AnnotationType | None | list[str] | bool]],
                  stocks_manager: StocksManager, filter_sub: bool) -> pd.DataFrame:
    """
    Creates the dataframe containing the samples information relevant to a ENA submission.
    If filter_sub excludes samples which are already annotated with an ENA accession number, else adds accession number
     columns to df.
    """
    df = pd.DataFrame()
    df["alias"] = table['Sample ID']
    df["title"] = table['Sample']
    df["scientific_name"] = "homo sapiens"  # TODO
    df["sample_description"] = super_protocol
    for k, v in annotations_dict.items():
        df[f"sample_attribute[{stocks_factor_format_name(k)}]"] = v["data"]

    if filter_sub:
        _drop_submitted(df, ModelType.SAMPLE, ANNOTATION_STOCKS_ENA_SAMPLE, stocks_manager)
    else:
        _add_acc(df, ModelType.SAMPLE, stocks_manager)
    df.drop_duplicates(inplace=True)
    df.replace({"#": "N."}, inplace=True)
    return df


def _add_acc(df: pd.DataFrame, model: ModelType, stocks_manager: StocksManager, ann: str = None) -> None:
    """
    Adds columns with ena accession number for each sample/dataset
    """
    if model == ModelType.SAMPLE:
        df["ena_accession"] = df["alias"].apply(
            lambda x: stocks_manager.fetch_annotation_value_from_item(model, x, ANNOTATION_STOCKS_ENA_SAMPLE))
        df["biosample_accession"] = df["alias"].apply(
            lambda x: stocks_manager.fetch_annotation_value_from_item(model, x, ANNOTATION_STOCKS_BIOSAMPLE))

    if model == ModelType.DATASET:
        if not ann:
            raise ValueError('Annotation type necessary to fetch datasets accession numbers')
        if ann == ANNOTATION_STOCKS_EXPERIMENT:
            df["ena_accession"] = df["alias"].apply(
                lambda x: stocks_manager.fetch_annotation_value_from_item(model, x.split(";")[-1],
                                                                          ANNOTATION_STOCKS_EXPERIMENT))
        if ann == ANNOTATION_STOCKS_ENA_RUN:
            df["ena_accession"] = df["alias"].apply(
                lambda x: stocks_manager.fetch_annotation_value_from_item(model, x.split(";")[-1],
                                                                          ANNOTATION_STOCKS_ENA_RUN))


def _drop_submitted(df: pd.DataFrame, model: ModelType, ann_type: str, stocks_manager: StocksManager) -> None:
    """
    Delete from dataframes rows of items who have an ENA accession number
    """
    # TODO theres got to be a better way #infocommercial
    df2 = df["alias"].apply(lambda x: stocks_manager.fetch_annotation_value_from_item(model, x.split(';')[-1],
                                                                                      ann_type))
    df2.fillna('', inplace=True)
    for sidx in range(len(df2.index)):
        if df2.iloc[sidx]:
            df.drop(sidx, inplace=True)


def ena_runs_df(table: pd.DataFrame, stocks_manager: StocksManager, filter_sub: bool) -> pd.DataFrame:
    """
    Creates the dataframe containing the datasets information relevant to a ENA submission.
    """
    df = pd.DataFrame()
    df["alias"] = table["Dataset ID"]
    df["experiment_alias"] = [';'.join(id) for id in zip(table["Assay ID"], table["Dataset ID"])]
    df["file_name"] = table["File Name"]
    df["file_type"] = file_type(table)
    df["file_checksum"] = table["Checksum"]
    if filter_sub:
        _drop_submitted(df, ModelType.DATASET, ANNOTATION_STOCKS_ENA_RUN, stocks_manager)
    else:
        _add_acc(df, ModelType.DATASET, stocks_manager, ANNOTATION_STOCKS_ENA_RUN)
    df.replace({"#": "N."}, inplace=True)
    return df


def file_type(table: pd.DataFrame) -> List[str]:
    """
    Parses the file format from the information received in the export table.
    :return: List of file formats which are relevant to a ENA submission
    """
    l = []
    for row in table.iterrows():
        if 'fastq' in row[1]['Type']:
            l.append('fastq')
        elif 'bam' in row[1]['Type']:
            l.append('bam')
        elif 'cram' in row[1]['Type']:
            l.append('cram')
        elif 'tab' in row[1]['Type']:
            l.append('tab')
        elif row[1]['Type'] == 'generic':
            split_filename = row[1]["File Name"].split('.')
            filetype = split_filename[-1]
            if split_filename[-1] == 'gz':
                filetype = split_filename[-2]
            if filetype not in ['bam', 'cram', 'tab', 'fastq']:
                logger.warning(f'File "{row[1]["File Name"]}" of type "{row[1]["Type"]}"/"{filetype}" '
                               f'not handled for ENA submission')
            l.append(filetype)
        else:
            logger.warning(f'File "{row[1]["File Name"]}" of type "{row[1]["Type"]}" not handled for ENA '
                           f'submission')
            l.append(row[1]['Type'])
    return l


def ena_experiment_df(table: pd.DataFrame, study: Study, assay_type: str, assay_dict: dict[str, SequencingAssay],
                      super_protocol: pd.DataFrame,
                      annotations_dict: Dict[str, dict[str, AnnotationType | None | list[str] | bool]],
                      stocks_manager: StocksManager, filter_sub: bool) -> pd.DataFrame:
    """
    Creates the dataframe containing the assays information relevant to a ENA submission.
    """
    df = pd.DataFrame()
    df["alias"] = [';'.join(id) for id in zip(table["Assay ID"], table["Dataset ID"])]
    # Title is "<assay title>; <study name>"
    df["title"] = table["Assay ID"].apply(lambda x: f'Standard {assay_dict[x].instrumentrun.instrument.model} '
                                                    f'{assay_dict[x].runtype.value} Sequencing; {study.name}')
    df["study_alias"] = study.id
    df["sample_alias"] = table['Sample ID']
    df['design_description'] = study.name
    df['library_name'] = table["Sample"]
    df['library_source'] = table['Library Source']
    df['library_strategy'] = table['Library Strategy']
    df['library_selection'] = table['Library Selection']
    df['library_layout'] = table['Assay ID'].apply(lambda x: runtype_layout_map[assay_dict[x].runtype])
    df['insert_size'] = "100"  # TODO
    df['library_construction_protocol'] = super_protocol
    df['platform'] = assay_type
    df['instrument_model'] = table['Instrument Model']
    for k, v in annotations_dict.items():
        if v["is_factor"]:
            df[f"experiment_attribute[{stocks_factor_format_name(k)}]"] = v["data"]
    if filter_sub:
        _drop_submitted(df, ModelType.DATASET, ANNOTATION_STOCKS_EXPERIMENT, stocks_manager)
    else:
        _add_acc(df, ModelType.DATASET, stocks_manager, ANNOTATION_STOCKS_EXPERIMENT)
    df.drop_duplicates(inplace=True)
    df.replace({"#": "N."}, inplace=True)
    return df


def parse_receipt(path: str) -> tuple[dict, dict, dict, dict, dict, dict] | None:
    """
    Reads the XML receipt from a ENA submission and extracts accession numbers.
    :return: 6 dictionaries {stocks_id: accession_number} for ENA, Biosamples and Biostudies
    :raises ValueError: The receipt.xml lacks a 'success' field or if 'success' field value is 'false'.
    """
    if not Path(path).exists():
        raise FileNotFoundError(f'No receipt.xml file from ENA were found at {path}. The STOCKS items will not be '
                                f'updated with accession numbers.')
    tree = ET.parse(path)
    root = tree.getroot()
    study_acc1 = {}
    study_acc2 = {}
    sample_acc_ena = {}
    sample_acc_biosample = {}
    run_acc = {}
    experimen_acc = {}
    if root.attrib.get('success') is None:
        raise ValueError(f"Error: Something is wrong with the receipt.xml file format, it doesnt have a 'success' "
                         f"attribute. Attributes: {root.attrib}")
    if root.attrib.get('success') == 'false':
        logger.warning(f"The ENA submission has failed. Receipt error messages (if any):")
        for err in root.iter('ERROR'):
            logger.warning(f"ENA receipt error message: {err.text}")
        raise ValueError("The ENA submission has failed")
    for mess in root.iter('INFO'):
        logger.info(f"Receipt messages: {mess.text}")
    for elem in root:
        if elem.items():
            id = elem.attrib['alias']
            if elem.tag == 'STUDY':
                study_acc1[id] = elem.attrib['accession']
                for child in elem:
                    study_acc2[id] = child.attrib['accession']
            elif elem.tag == 'RUN':
                run_acc[id] = elem.attrib['accession']
            elif elem.tag == 'EXPERIMENT':
                experimen_acc[id] = elem.attrib['accession']
            elif elem.tag == 'SAMPLE':
                sample_acc_ena[id] = elem.attrib['accession']
                for child in elem:
                    sample_acc_biosample[id] = child.attrib['accession']
    return study_acc1, study_acc2, run_acc, experimen_acc, sample_acc_ena, sample_acc_biosample


def upload_ena_annotation(accession_dicts: tuple[dict, dict, dict, dict, dict, dict], manager: StocksManager) -> bool:
    """
    Updates STOCKS items with accession number from ENA submission.
    Process will continue through exceptions for each item and issue warning messages.
    :raises ValueError: prior to uploading if an annotation type could not be retrieved from the STOCKS server.
    """

    study_acc1, study_acc2, run_acc, experimen_acc, sample_acc_ena, sample_acc_biosample = accession_dicts

    # check if the fetch_annotation_by_name method used in post_annotation won't fail
    ann_name_to_annotype: dict[str, AnnotationType] = {}
    for ann in [ANNOTATION_STOCKS_ENA_STUDY, ANNOTATION_STOCKS_ENA_BIOSTUDY, ANNOTATION_STOCKS_ENA_RUN,
                ANNOTATION_STOCKS_EXPERIMENT, ANNOTATION_STOCKS_ENA_SAMPLE, ANNOTATION_STOCKS_BIOSAMPLE]:
        annotype = manager.fetch_annotationtype_by_name(ann)
        if not annotype:
            raise ValueError(f"No annotation of type {ann} could be found")
        ann_name_to_annotype[ann] = annotype

    done = True
    done = _update_annotation(study_acc1, ModelType.STUDY, ann_name_to_annotype[ANNOTATION_STOCKS_ENA_STUDY], manager,
                              done)
    done = _update_annotation(study_acc2, ModelType.STUDY, ann_name_to_annotype[ANNOTATION_STOCKS_ENA_BIOSTUDY],
                              manager, done)
    done = _update_annotation(run_acc, ModelType.DATASET, ann_name_to_annotype[ANNOTATION_STOCKS_ENA_RUN], manager,
                              done)
    done = _update_annotation(experimen_acc, ModelType.DATASET, ann_name_to_annotype[ANNOTATION_STOCKS_EXPERIMENT],
                              manager, done)
    done = _update_annotation(sample_acc_ena, ModelType.SAMPLE, ann_name_to_annotype[ANNOTATION_STOCKS_ENA_SAMPLE],
                              manager, done)
    done = _update_annotation(sample_acc_biosample, ModelType.SAMPLE, ann_name_to_annotype[ANNOTATION_STOCKS_BIOSAMPLE],
                              manager, done)

    if not done:
        logger.warning("Error while updating the STOCKS server items with information from the receipt.xml. "
                       "Either discrepancies between the information provided and the STOCKS items were found, or some "
                       "items could not be updated.")
    else:
        logger.info("All accession numbers were successfully annotated.")
    return done


def _update_annotation(acc_dic: Dict, model: ModelType, ann: str | AnnotationType, manager: StocksManager, done: bool) \
        -> bool:
    """
    If only 1 update fails, final "done" will be false
    """
    for id, acc in acc_dic.items():
        id = id.split(';')[-1]  # id of experiment is "<assay_id>;<dataset_id>"
        if not _update_annotation_aux(model, id, ann, acc, manager):
            done = False
    return done


def _update_annotation_aux(model: ModelType, uuid: str, ann: str | AnnotationType, content: str | StocksCVTerm,
                           manager: StocksManager) -> bool:
    """
    Tries to add an annotation [ann] with content [content] to a stocks item [model] of uuid [id].
    In case the annotation is already present, compares the content.
    :param model: utils.ModelType enum for STOCKS models of the stocks item
    :param uuid: string ID of STOCKS item
    :param ann: annotation name or stocks.AnnotationType of the annotation to be added to the stocks item
    :param content: string or stocks.StocksCVTerm content of the annotation to be added to the stocks item
    :param manager: StocksManager
    :return: True if annotation added successfully or if annotation exists with identical content, else False.
    """
    if isinstance(ann, str):
        ann = manager.fetch_annotationtype_by_name(ann)
    try:
        manager.save_annotation(model, uuid, ann, content)
    except HTTPException as err:
        if err.status_code == 400:
            item = manager.fetch_item(uuid, model)
            if item[ann.id] != content:
                logger.error(f"Annotation {ann}, item {model.value} of id {uuid}: the accession numbers of the "
                             f"receipt.xml from the ENA and STOCKS do not match. ENA: {content}, "
                             f"STOCKS:{item[ann.id]}")
                return False
            else:
                return True
    except Exception as err:
        logger.error(f"Something went wrong during assigning acession number for {ann} in "
                     f"{model.value} of id {uuid}. Item will not be annotated. Err message: {err}")
        return False
    return True


def get_annotation_id(model: ModelType, id: str, anntype: str, manager: StocksManager) -> List[str]:
    """
    :returns: The ids of all the annotations of type [anntype] in an item [model] of id [id]
    :raises ValueError: if no annotations at all or no occurences of the annotation type were found
    """
    ann_list = manager.list_annotations_from_item(model, id)
    ann_id_list = []
    if not ann_list:
        raise ValueError(f"No annotations were found in {model.value} of id {id}")
    for ann in ann_list:
        if isinstance(ann, dict) and 'name' in ann and 'value' in ann:
            if ann.get('name') == anntype:
                ann_id_list.append(ann.get('id'))
    if not ann_id_list:
        raise ValueError(f"No annotation {anntype} could be find in {model.value} of id {id}")
    return ann_id_list


def _ena_upload_cli(cmd: str, to_del_credentials: bool, ena_cred_path: str, fake_dir: str = None) -> None:
    """
    Runs the ena upload cli as a subprocess with preset arguments: capture_output=True, text=True, shell=True.
    Deletes the directory containing fake data if given. Deletes credential file if needed.
    :param cmd: command passed to the ena upload cli
    :param fake_dir: path of the dir containing fake data to be deleted after upload
    :param ena_cred_path: path of the file containing the credential to be deleted if to_del_credentials is True.
    :raise stocksapi.exceptions.SubProcessError: if subprocess has an exit code other than 0
    """
    run = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if to_del_credentials:
        os.remove(ena_cred_path)
    if fake_dir:
        shutil.rmtree(fake_dir)  # Delete fake data
    if run.returncode != 0:
        raise SubProcessError(stacktrace=run.stderr, cmd=cmd)


def parse_html(txt: str) -> str:
    parse_text = HTMLFilter()
    if not txt:
        return ''
    parse_text.feed(txt)
    return ' '.join(parse_text.text.splitlines())


