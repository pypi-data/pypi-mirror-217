import distutils
import logging
from enum import Enum
from html.parser import HTMLParser
from pathlib import Path
from pwd import getpwuid
from subprocess import Popen, PIPE
import smtplib
from email.message import EmailMessage
from typing import Union
from uuid import UUID

from jsonpickle import encode, handlers
from cli import config_parser

logger = logging.getLogger(__name__)

############################
# Constants and common models
#############################

class HTMLFilter(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data


class JsonEnumHandler(handlers.BaseHandler):

    def restore(self, obj):
        pass

    def flatten(self, obj: Enum, data):
        return obj.value


class ExtendedEnum(Enum):
    """
    https://stackoverflow.com/questions/29503339/how-to-get-all-values-from-python-enum-class
    """
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class ModelType(ExtendedEnum):
    ANNOTATION = "annotation"
    ASSAY = "assay"
    ARCHIVE = "archive"
    ATTACHMENT = "attachment"
    CONSUMABLE = "consumable"
    EQUIPMENT = "equipment"
    DATASET = "dataset"
    DATAFILE = "datafile"
    DATAFILECOPY = "datafilecopy"
    DATASETCOLLECTION = "datasetcollection"
    DROPBOX = "dropbox"
    EXPERIMENT = "experiment"
    GROUP = "group"
    INSTRUMENTMODEL = "instrumentmodel"
    INSTRUMENTRUN = "instrumentrun"
    PROJECT = "project"
    PROTOCOL = "protocol"
    STORAGE_VOLUME = "storagevolume"
    SAMPLE = "sample"
    SPECIMEN = "specimen"
    STORAGE_EQUIPMENT = "storageequipment"
    STUDY = "study"
    TERM = "term"
    USER = "user"
    WORKFLOW = "workflow"


class ExperimentStatus(ExtendedEnum):
    PLANNED = 'PLANNED'
    IN_PROGRESS = 'IN PROGRESS'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


class UserRole(ExtendedEnum):
    """
    roles from EFO https://www.ebi.ac.uk/ols/ontologies/efo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FBFO_0000023&lang=en&viewMode=All&siblings=false
    """
    SUBMITTER = 'submitter'
    INVESTIGATOR = 'investigator'
    DATA_ANALYST = 'data analyst'
    EXPERIMENT_PERFORMER = 'experiment performer'


class Technology(ExtendedEnum):
    SEQUENCING = 'sequencing'
    LIGHT_MICROSCOPY = 'light microscopy'
    ELECTRON_MICROSCOPY = 'electron microscopy'
    PROTEOMICS = 'proteomics'
    FLOW_CYTOMETRY = 'flow cytometry'
    METABOLOMICS = 'metabolomics'
    OTHER = 'other'
    NA = 'NA'


# class StocksModelType(ExtendedEnum):
#     ANNOTATION_TYPE = 'ANNOTATIONTYPE'
#     ASSAY_GENERIC = 'GENERICASSAY'
#     ASSAY_ILLUMINA = 'NGSILLUMINAASSAY'
#     ASSAY_NANOPORE = 'NANOPOREASSAY'
#     ASSAY_VOLUME_EM = 'VOLUMEEMASSAY'
#     ASSAY_TRANSMISSION_EM = 'TRANSMISSIONEMASSAY'
#     ASSAY_LIGHT_MICROSCOPY_SCREEN= 'LIGHTMICROSCOPYSCREENASSAY'
#     ASSAY_LIGHT_MICROSCOPY = 'LIGHTMICROSCOPYASSAY'
#     CV_CATEGORY = 'CATEGORIES'
#     CV_TERM = 'TERMS'
#     DATAFILE = 'DATAFILE'
#     DATASET = 'DATASET'
#     DATASETCOLLECTION = 'DATASETCOLLECTION'
#     DEFAULT = 'DEFAULT'
#     EQUIPMENT = 'EQUIPMENT'
#     EXPERIMENT = 'EXPERIMENT'
#     GROUP = 'GROUP'
#     INSTRUMENT_MODEL = 'INSTRUMENTMODEL'
#     INSTRUMENT_RUN = 'INSTRUMENTRUN'
#     PROJECT = 'PROJECT'
#     PROTOCOL = 'PROTOCOL'
#     PROTOCOL_CULTURE_GROWTH = 'CULTURE_GROWTH'
#     PROTOCOL_EXTRACTION = 'EXTRACTION'
#     PROTOCOL_FIXATION = 'FIXATION'
#     PROTOCOL_LIBRARY_PREPARATION = 'LIBRARY_PREPARATION'
#     PROTOCOL_MOLECULAR_BIOLOGY = 'MOLECULAR_BIOLOGY'
#     PROTOCOL_SEQUENCING = 'SEQUENCING'
#     SAMPLE_GENERIC = 'GENERICSAMPLE'
#     SAMPLE_EM = 'EM'
#     SAMPLE_SEQUENCING_LIBRARY = 'SEQUENCINGLIBRARY'
#     STUDY = 'STUDY'
#     USER = 'USER'


class InstrumentType(ExtendedEnum):
    SEQUENCER = 'SEQUENCER'
    MICROSCOPE = 'MICROSCOPE'
    SPECTROMETER = 'SPECTROMETER'


class SequencingRunType(ExtendedEnum):
    SINGLE_END = 'single-end'
    PAIRED_END = 'paired-end'
    MULTI_END = 'multi-end'


class SequencingReadType(ExtendedEnum):
    READ1 = 'read_1'
    READ2 = 'read_2'
    READ3 = 'read_3'
    READ4 = 'read_4'
    INDEX1 = 'index_1'
    INDEX2 = 'index_2'
    ALL_READS = 'all'


class NanoporeAdaptiveMode(ExtendedEnum):
    NONE = 'None'
    OTHER = 'Other'
    ENRICH = 'Enrich'
    DEPLETE = 'Deplete'

class NanoporeLiveBaseCallingType(ExtendedEnum):
    FAST = 'fast'
    HIGH_ACCURACY = 'high accuracy'
    SUPER_HIGH_ACCURACY = 'super high accuracy'
    METHYLATION = 'methylation'
    OTHER = 'other'
    NONE = 'None'


class ObjectState(ExtendedEnum):
    INITIALIZED: 'INITIALIZED'
    NEW = 'NEW'
    REGISTERED = 'REGISTERED'
    TEMPLATE = 'TEMPLATE'


def find_owner(path: Path) -> str:
    """gets the owner name of a file or dir_path"""
    return getpwuid(path.stat().st_uid).pw_name


def rsync(source: str, dest: str, safe: bool = True):
    logger.info(f"rsync {source} to {dest}")
    if safe:
        cmd = ["rsync", "--safe-links", "--one-file-system", "-r", source, dest]
    else:
        cmd = ["rsync", "--copy-links", "-r", source, dest]
    logger.info("%s", " ".join(cmd))
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    std_out, std_err = process.communicate()
    if process.returncode != 0:
        logger.debug(std_out)
        logger.exception(std_err)
        raise Exception(f"Failed to rsync {source} -> {dest}")


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None


def copy_dir(src: str, dst: str):
    if is_tool('rsync'):
        rsync(src=src + "/", dest=dst)  # we make sure source as a trailing '/'
    else:
        logger.info(f"rsync not avail => python copy_tree {src} to {dst}")
        distutils.dir_util.copy_tree(src=src, dst=dst)


def mail_admin(mess: str):
    (mail_host, mail_smtp, admin_name, admin_email) = config_parser.get_mailing_details()

    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(
        f"""
        Dear STOCKS WatchDog {admin_name},
        Watchdog has detected the following non-blocking error:
        {mess}
        
        This warning most likely requires manual actions from you but should not prevent WatchDog from running correctly
        
        Thank you
        """
    )

    msg['Subject'] = f'Watchdog encountered a non blocking problem that requires your intervention'
    msg['From'] = admin_email
    msg['To'] = admin_email

    # Send the message
    s = smtplib.SMTP(mail_smtp)
    s.send_message(msg)
    s.quit()


def mail_admin_job_in_error(mess: str):
    (mail_host, mail_smtp, admin_name, admin_email) = config_parser.get_mailing_details()

    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(mess)

    msg['Subject'] = f'A watchdog job could not finish properly. Action required'
    msg['From'] = admin_email
    msg['To'] = admin_email

    # Send the message
    s = smtplib.SMTP(mail_smtp)
    s.send_message(msg)
    s.quit()

def is_uuid(value: Union[str, int, UUID]) -> bool:
    try:
        UUID(value)
        return True
    except (ValueError, AttributeError):  # str or int, but not uuid
        return False
