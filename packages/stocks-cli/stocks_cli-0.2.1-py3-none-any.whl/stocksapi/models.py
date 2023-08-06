"""
    Various data models to communicate with the STOCKS API.
"""
import logging
from datetime import datetime, date
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, Extra, validator  # pylint:disable=E0611

from stocks.models import User, Instrument, DatasetFile, InstrumentModel, InstrumentRun, SimpleInstrumentRun, Assay, \
    UserGroup
from cli.utils import Technology, SequencingRunType, ExperimentStatus, NanoporeLiveBaseCallingType, NanoporeAdaptiveMode
from uuid import UUID

logger = logging.getLogger(__name__)

def _check_datetime_from_api(val, as_datetime=False) -> datetime | str | Dict | date:
    """
    Converts the date and datetime received from API such as
    "start_date": {
                "name": "start_date",
                "value": "2023-02-23",
                "category": "property"
            }
    and
    "freeze_date": {
                "name": "freeze_date",
                "value": "2023-02-23T17:04:55.777723+01:00",
                "category": "property"
            }
    :param val:
    :param as_datetime: set to True if a datetime is expected
    :return:
    """
    if isinstance(val, dict) and 'value' in val:
        if not val['value']:
            return ''
        if as_datetime:
            return datetime.fromisoformat(val['value'])
        return datetime.strptime(val['value'], '%Y-%m-%d').date()
    # if not the expected dict, we leave the input unchanged
    return val


def _extract_value_from_api_response(val) -> str | Dict:
    """
        "url": {
            "name": "url",
            "value": "https://gbcs-dev.embl.de:82/api/v2/core/studies/4d57519f-8169-4eaf-acd8-e43924fd911e/",
            "category": "property"
        },
        "id": {
            "name": "id",
            "category": "property",
            "value": "4d57519f-8169-4eaf-acd8-e43924fd911e"
        },
    """
    if isinstance(val, dict) and 'value' in val:
        if not val['value']:
            return ''
        return val['value']
    if isinstance(val, dict) and 'name' in val:
        if val['name']:
            return val['name']

    # if not the expected dict, we leave the input unchanged
    return val


def _extract_name_from_api_response(val) -> str | Dict:
    """
        "name": {
            "name": "name",
            "value": {
                "id": "4d57519f-8169-4eaf-acd8-e43924fd911e",
                "name": "DNA methylation profiles of mouse sperm in response to antibiotic-induced gu... ",
                "model_name": "study",
                "app_name": "core",
                "model_type": null
            },
            "category": "property"
        },
    """
    if isinstance(val, dict) and 'value' in val:
        if isinstance(val['value'], dict) and 'name' in val['value']:
            return val['value']['name']
        return val['value']
    # if not the expected dict, we leave the input unchanged
    return val


# TODO: why dict as return type ?
def _extract_list_value_from_api_response(val) -> List[str] | Dict:
    """
    "design": {
        "name": "design",
        "value": [
            {
                "id": "c549042d-8b61-4b5a-8f17-1cefd9608f10",
                "name": "biological replicate",
                "label": "biological replicate",
                "description": "",
                "dbxref_id": "http://www.ebi.ac.uk/efo/EFO_0002091"
            },
            {
                "id": "e5250856-f0d5-4f39-bfbe-355a6c35d1a6",
                "name": "development or differentiation design",
                "label": "development or differentiation design",
                "description": "",
                "dbxref_id": "http://www.ebi.ac.uk/efo/EFO_0001746"
            },
        ],
        "category": "property"
        }

    "groups": {
            "name": "groups",
            "category": "property",
            "value": [
                {
                    "id": {
                        "name": "id",
                        "category": "property",
                        "value": 2
                    },
                    "name": {
                        "name": "name",
                        "category": "property",
                        "value": "Computational Support Genome Biology"
                    }
                }
            ]
        }
    """
    if isinstance(val, dict) and 'value' in val and isinstance(val.get('value'), list):
        val_list = []
        for d in val.get('value'):
            if d.get('id'):
                if isinstance(d.get('id'), dict) and 'value' in d.get('id'):
                    val_list.append(d.get('id').get('value'))
                else:
                    val_list.append(d.get('id'))
        return val_list
    if isinstance(val, list):
        val_list = []
        for d in val:
            if isinstance(d, dict) and 'id' in d:
                val_list.append(d.get('id'))
        return val_list
    return val

# TODO: why dict as return type ?
def _extract_username_from_api_response(val) -> str | Dict:
    """
    # Non flat
    "modified_by": {
                "name": "modified_by",
                "value": {
                    "id": 25,
                    "username": "girardot",
                    "full_name": "Charles Girardot"
                },
                "category": "property"
            }
    # Flat
    "modified_by": {
                "id": 1,
                "username": "admin",
            }
    """
    if isinstance(val, dict):
        if 'value' in val:
            if not val['value']:
                return ''
            return val['value']['username']
        if 'username' in val:
            return val['username']
    # if not the expected dict, we leave the input unchanged
    return val


class PaginatedResults(BaseModel, extra=Extra.allow):
    """
    class to encapsulate API paginated results response
    """
    previous: str | None
    next: str | None
    current: int
    total: int
    total_pages: int
    results: Any


# not names pydantic as this object can be returned by the manager
class StocksAttachment(BaseModel, extra=Extra.ignore):
    """
    a wrapper around an attachment
    """
    url: str
    name: str
    created_by: str
    modified_by: str
    created: datetime
    modified: datetime
    peek: str
    size: int
    object_id: str
    content_type: int
    filetype: str
    mimetype: str
    download_url: str
    direct_url: str
    embedded: bool
    is_export: bool
    autogenerated: bool
    tsr_url: Optional[str]
    tsq_url: Optional[str]

    @validator('created', pre=True)
    def check_created(cls, val):
        return _check_datetime_from_api(val, as_datetime=True)

    @validator('modified', pre=True)
    def check_modified(cls, val):
        return _check_datetime_from_api(val, as_datetime=True)


class PydanticUserGroup(BaseModel, extra=Extra.ignore):
    id: str
    name: str


class PydanticUser(BaseModel, extra=Extra.ignore):
    """
    A base class for a user
    """
    username: str  # stocksapi login
    id: str | None  # stocksapi ID
    full_name: str | None  # user full name
    email: str | None  # user email
    groups: List[PydanticUserGroup] | None
    date_joined: datetime | None
    is_active: bool | str | None
    is_superuser: bool | str | None
    is_staff: bool | str | None

    @validator('username', pre=True)
    def extract_username(cls, val):
        return _extract_value_from_api_response(val)

    @validator('id', pre=True)
    def extract_id(cls, val):
        return _extract_value_from_api_response(val)

    @validator('full_name', pre=True)
    def extract_full_name(cls, val):
        return _extract_value_from_api_response(val)

    @validator('email', pre=True)
    def extract_email(cls, val):
        return _extract_value_from_api_response(val)

    @validator('date_joined', pre=True)
    def extract_date_joined(cls, val):
        return _check_datetime_from_api(val, as_datetime=True)

    @validator('is_active', pre=True)
    def extract_is_active(cls, val):
        return bool(_extract_value_from_api_response(val))

    @validator('is_superuser', pre=True)
    def extract_is_superuser(cls, val):
        return bool(_extract_value_from_api_response(val))

    @validator('is_staff', pre=True)
    def extract_is_staff(cls, val):
        return bool(_extract_value_from_api_response(val))

    @validator('groups', pre=True)
    def extract_groups(cls, val):
        logger.debug(f"got groups as {type(val)} => \n {val}")
        group_list = []
        if isinstance(val, dict) and val.get('value'):
            for d in val.get('value'):
                group_list.append(
                    PydanticUserGroup(
                        id=str(_extract_value_from_api_response(d.get('id'))),
                        name=_extract_value_from_api_response(d.get('name'))
                    ))
            return group_list
        elif isinstance(val, dict) and val and isinstance(next(iter(val.values())), UserGroup):
            for v in val.values():
                group_list.append(
                    PydanticUserGroup(**dict(vars(v))))
            return group_list
        elif isinstance(val, list):
            for d in val:
                group_list.append(PydanticUserGroup(**d))

        return val


class PydanticReferencedStocksObject(BaseModel, extra=Extra.ignore):
    """
    example
    "project": {
            "name": "project",
            "value": {
                "id": "8492bf1a-1f91-449d-8e5f-18c7df0de038",
                "name": "Tea Project",
                "deleted": false,
                "model_name": "project",
                "app_name": "core",
                "model_type": "DEFAULT"
            },
            "category": "property"
        }
    """
    id: str = ''
    name: str
    deleted: bool | None
    model_name: str = ''
    app_name: str = ''
    model_type: str | None


class PydanticValueField(BaseModel):
    """
    A base class to represent an slot as :
    "id": {"value": null}
    """
    value: str | None = None


class PydanticNameField(BaseModel):
    """
    A base class to represent an slot as :
    "type": {"name": "xyz"}
    """
    name: str | None = None


class PydanticStocksBaseItem(BaseModel):
    """
    A base class for all STOCKS items
    """
    name: str
    id: str | None = None
    description: str | None = None
    owner: str | None = None
    owned_by: str | None = None
    created: datetime | None = None
    created_by: str | None = None
    modified: datetime | None = None
    modified_by: str | None = None
    deleted: bool = False
    deleted_by: str | None = None
    deleted_date: datetime | None = None
    # the PydanticNameField must be used when generating JSON for POST
    type: str | PydanticNameField = Field(default="DEFAULT", alias="stocks_model_type")
    model_name: str | None = None
    app_name: str | None = None

    class Config:
        extra = Extra.ignore
        allow_population_by_field_name = True

    @validator('type', pre=True)
    def extract_type(cls, val):
        x = _extract_value_from_api_response(val)
        return x

    @validator('id', pre=True)
    def check_id(cls, val):
        return _extract_value_from_api_response(val)

    @validator('name', pre=True)
    def check_name(cls, val):
        return _extract_name_from_api_response(val)

    @validator('description', pre=True)
    def check_description(cls, val):
        return _extract_value_from_api_response(val)

    @validator('created_by', pre=True)
    def check_created_by(cls, val):
        return _extract_username_from_api_response(val)

    @validator('owner', pre=True)
    def check_owner(cls, val):
        if isinstance(val, User):
            return val.username
        return _extract_username_from_api_response(val)

    @validator('owned_by', pre=True)
    def extract_owned_by(cls, owned_by):
        if isinstance(owned_by, dict):
            if 'value' in owned_by:
                return owned_by['value']['name']
            return owned_by['name']
        return owned_by

    @validator('modified_by', pre=True)
    def check_modified_by(cls, val):
        return _extract_username_from_api_response(val)

    @validator('deleted_by', pre=True)
    def check_deleted_by(cls, val):
        return _extract_username_from_api_response(val)

    @validator('deleted', pre=True)
    def check_deleted(cls, val):
        if isinstance(val, dict) and 'value' in val:
            return bool(val['value'])
        return val

    @validator('created', pre=True)
    def check_created(cls, val):
        return _check_datetime_from_api(val, as_datetime=True)

    @validator('modified', pre=True)
    def check_modified(cls, val):
        return _check_datetime_from_api(val, as_datetime=True)

    @validator('deleted_date', pre=True)
    def check_deleted_date(cls, val):
        return _check_datetime_from_api(val, as_datetime=True)


class PydanticExperiment(PydanticStocksBaseItem):
    """
    A class representing an experiment.
    """
    is_frozen: bool
    status: ExperimentStatus
    project: str
    summary: str | None = None
    protocol: str | None = None
    start_date: datetime | date | None = None
    completed_date: datetime | date | None = None
    estimated_completion_date: datetime | date | None = None
    freeze_date: datetime | date | None = None

    @validator('is_frozen', pre=True)
    def check_is_frozen(cls, val):
        if isinstance(val, dict) and 'value' in val:
            return bool(val['value'])
        return val

    @validator('project', pre=True)
    def check_project(cls, val):
        if isinstance(val, dict) and 'value' in val:
            return val['value']['id']
        return val

    @validator('protocol', pre=True)
    def check_protocol(cls, val):
        if isinstance(val, dict) and 'value' in val:
            if val['value']:
                return val['value']['id']
            else:
                return None
        return val

    @validator('status', pre=True)
    def check_status(cls, status):
        if isinstance(status, dict) and status['value'] and status['value']['value']:
            return ExperimentStatus(status['value']['value'])
        elif isinstance(status, ExperimentStatus):
            return status
        elif isinstance(status, str):
            return ExperimentStatus(status)

        raise ValueError(f"Cannot convert status value {str(status)} of type {type(status)}")

    @validator('summary', pre=True)
    def extract_summary(cls, summary):
        if isinstance(summary, dict) and 'value' in summary:
            if summary['value']:
                logger.debug(f"summary=> '{summary['value']}'")
                return summary['value']
            else:
                return None
        return summary

    @validator('start_date', pre=True)
    def check_start_date(cls, val):
        return _check_datetime_from_api(val)

    @validator('completed_date', pre=True)
    def check_completed_date(cls, val):
        return _check_datetime_from_api(val, as_datetime=True)

    @validator('estimated_completion_date', pre=True)
    def check_estimated_completion_date(cls, val):
        return _check_datetime_from_api(val)

    @validator('freeze_date', pre=True)
    def check_freeze_date(cls, val):
        return _check_datetime_from_api(val, as_datetime=True)


class PydanticStudy(PydanticStocksBaseItem):
    """
    A class representing a Study.
    """
    design: List[str] | None = None

    @validator('design', pre=True)
    def extract_design(cls, val):
        return _extract_list_value_from_api_response(val)


class PydanticCVTerm(PydanticStocksBaseItem):
    """
    "url": {
        "name": "url",
        "value": "https://gbcs-dev.embl.de:82/api/v2/vocabularies/terms/c549042d-8b61-4b5a-8f17-1cefd9608f10/",
        "category": "property"
    },
    "id": {
        "name": "id",
        "category": "property",
        "value": "c549042d-8b61-4b5a-8f17-1cefd9608f10"
    },
    "dbxref_id": {
        "name": "dbxref_id",
        "category": "property",
        "value": "http://www.ebi.ac.uk/efo/EFO_0002091"
    },
    """
    url: str
    dbxref_id: str

    @validator('url', pre=True)
    def extract_url(cls, val):
        return _extract_value_from_api_response(val)

    @validator('dbxref_id', pre=True)
    def extract_dbxref_id(cls, val):
        return _extract_value_from_api_response(val)


class PydanticProtocol(PydanticStocksBaseItem):
    """
    A class representing a Protocol. Adds a type as an ontological term
    id, name, description, owner and annotations inherited
    TODO: add support for protocol parameters
    """
    summary: str

    @validator('summary', pre=True)
    def extract_summary(cls, val):
        return _extract_value_from_api_response(val)


class PydanticSample(PydanticStocksBaseItem):
    class Config:
        extra = Extra.allow


class PydanticInstrumentModel(PydanticStocksBaseItem):
    technology: Technology
    platform: str

    @validator('technology', pre=True)
    def check_technology(cls, technology):
        if isinstance(technology, dict) and technology['value']:
            return Technology(technology['value'])
        if isinstance(technology, str):
            return Technology(technology)
        return technology


class PydanticInstrument(PydanticStocksBaseItem):
    code: str | None = Field(alias="serial_number")
    instrumentmodel: PydanticInstrumentModel | PydanticReferencedStocksObject | str | None = Field(alias="model")

    @validator('instrumentmodel', pre=True)
    def check_instrumentmodel(cls, instrumentmodel):
        if isinstance(instrumentmodel, InstrumentModel):
            return PydanticInstrumentModel(**dict(vars(instrumentmodel)))

        return instrumentmodel


class PydanticSimpleInstrumentRun(PydanticStocksBaseItem):
    instrument: PydanticInstrument | PydanticReferencedStocksObject | str | None
    start_datetime: datetime | None
    end_datetime: datetime | None
    producer: str | None
    responsible_person: PydanticUser | str | None
    assays: List["PydanticAssay"] = list()

    @validator('instrument', pre=True)
    def check_instrument(cls, instrument):
        logging.debug(f"got instrument var of type {type(instrument)} :\n {instrument}")
        if isinstance(instrument, Instrument):
            return PydanticInstrument(**dict(vars(instrument)))
        elif isinstance(instrument, dict):
            return PydanticInstrument.parse_obj(instrument)
        elif isinstance(instrument, UUID):
            return str(instrument)

        return instrument

    @validator('assays', pre=True)
    def check_assays(cls, val):
        if not val:
            return list()
        if not isinstance(val, list):
            # let validation complain
            return val
        l = list()
        for o in val:
            if isinstance(o, Assay):
                l.append(PydanticAssay(**dict(vars(o))))
            elif isinstance(o, dict):
                l.append(PydanticAssay(**o))
            else:
                l.append(o)  # will most likely raise an error if this is not an PydanticAssay
        return l


class PydanticSimpleInstrumentRunPost(BaseModel, extra=Extra.allow):
    """
    wrapper to POST a InstrumentRun
    """
    results: PydanticSimpleInstrumentRun


class PydanticInstrumentRun(PydanticSimpleInstrumentRun):
    """
    an augmented run that match the old run payload developped to accept GeneCore JSON
    """
    technology: Technology
    platform: str
    managed: bool

    @validator('instrument', pre=True)
    def check_instrument(cls, instrument):
        if isinstance(instrument, Instrument):
            return PydanticInstrument(**dict(vars(instrument)))
        if isinstance(instrument, UUID):
            return str(instrument)

        return instrument


class PydanticAssay(PydanticStocksBaseItem, extra=Extra.allow):
    """
    An assay must have either a model or a run. For legacy reasons, we also need to expose the
    instrument at the assay level when POSTing
    """
    multiplexed: bool
    instrumentrun: Optional[str | PydanticSimpleInstrumentRun]
    instrument: Optional[str | PydanticInstrument | PydanticValueField]
    instrumentmodel: str | PydanticInstrumentModel | None = ""

    @validator('instrumentmodel', pre=True)
    def extract_instrumentmodel(cls, val):
        if not val:
            return ''
        logger.debug(f"instrumentmodel validator: val type is {type(val)} => {val}")
        if isinstance(val, InstrumentModel):
            val = dict(vars(val))

        if isinstance(val, dict) and 'technology' in val:
            return PydanticInstrumentModel(**val)

        elif isinstance(val, dict):
            # This must be a PydanticLinked object from assay GET endpoint, we grab the ID
            return val['id']
        return val

    @validator('instrumentrun', pre=True)
    def extract_instrumentrun(cls, val):
        if not val:
            return ''
        logger.debug(f"instrumentrun validator: type is {type(val)} => {val}")
        if isinstance(val, dict):
            if 'value' in val and 'id' in val['value']:
                return val['value']['id']
            if 'id' in val:
                return val['id']
        elif isinstance(val, UUID):
            return str(val)
        elif isinstance(val, SimpleInstrumentRun):
            logger.debug(f"run UUID is {val.id}")
            return str(val.id)

        return val

    @validator('multiplexed', pre=True)
    def extract_multiplexed(cls, val):
        return _extract_value_from_api_response(val)


class PydanticSequencingAssay(PydanticAssay):
    flowcell: str | None = None
    flowcell_version: str | None = None
    lane: str | None = None
    runtype: SequencingRunType | PydanticValueField | None = None
    runmode: str | None = None
    readlength: str | None = None
    chemistry: str | None = None
    live_base_calling: NanoporeLiveBaseCallingType | PydanticValueField = NanoporeLiveBaseCallingType.NONE
    live_read_mapping: bool | None = None
    ref_genome: Optional[str] = None
    adaptive_mode: NanoporeAdaptiveMode | PydanticValueField = NanoporeAdaptiveMode.NONE
    adaptive_mode_details: str | None = None
    demultiplexed: str | None = None

    class Config:
        extra = Extra.ignore

    @validator('live_base_calling', pre=True)
    def extract_live_base_calling(cls, val):
        if isinstance(val, dict) and 'value' in val:
            return NanoporeLiveBaseCallingType(_extract_value_from_api_response(val['value']))
        return val

    @validator('adaptive_mode', pre=True)
    def extract_adaptive_mode(cls, val):
        if isinstance(val, dict) and 'value' in val:
            return NanoporeAdaptiveMode(_extract_value_from_api_response(val['value']))
        return val

    @validator('runtype', pre=True)
    def extract_runtype(cls, val):
        if isinstance(val, dict) and 'value' in val:
            return SequencingRunType(_extract_value_from_api_response(val['value']))
        return val

    @validator('runmode', pre=True)
    def extract_runmode(cls, val):
        return _extract_value_from_api_response(val)

    @validator('lane', pre=True)
    def extract_lane(cls, val):
        return _extract_value_from_api_response(val)

    @validator('flowcell', pre=True)
    def extract_flowcell(cls, val):
        return _extract_value_from_api_response(val)

    @validator('demultiplexed', pre=True)
    def extract_demultiplexed(cls, val):
        return _extract_value_from_api_response(val)


# needed for unclear reasons
PydanticSimpleInstrumentRun.update_forward_refs()
PydanticInstrumentRun.update_forward_refs()


class PydanticSimpleAssayPost(BaseModel, extra=Extra.allow):
    """
    wrapper to POST a new assay
    """
    results: PydanticAssay


class PydanticSequencingAssayRunInfo(PydanticSequencingAssay):
    """
    Adds fields to catch the run info
    """
    technology: Technology
    platform: str
    is_managed: bool = Field(..., alias="managed")
    is_template: Optional[bool] = False
    nr_of_samples: Optional[int] = 1
    instrument: PydanticInstrument | str | None

    @validator('instrument', pre=True)
    def check_instrument(cls, instrument):
        if isinstance(instrument, Instrument):
            return PydanticInstrument(**dict(vars(instrument)))
        return instrument


class PydanticDatasetCollection(PydanticStocksBaseItem):
    is_raw: bool


class PydanticDatasetFile(PydanticStocksBaseItem, extra=Extra.allow):
    uri: Optional[str] = None
    type: Optional[str] = Field(default=None, alias="filetype")
    is_folder: Optional[bool] = Field(default=None, alias="is_dir")
    is_managed: Optional[bool] = None
    status: Optional[str] = "NEW"


class PydanticDatasetFileCopy(PydanticStocksBaseItem, extra=Extra.ignore):
    uri: str
    shortname: str
    is_primary_copy: bool
    datafile: PydanticDatasetFile | str | None

    @validator('datafile', pre=True)
    def check_datafile(cls, datafile):
        if isinstance(datafile, DatasetFile):
            return PydanticDatasetFile(**dict(vars(datafile)))
        if isinstance(datafile, dict):
            return PydanticDatasetFile(**datafile)
        if isinstance(datafile, UUID):
            return str(UUID)

        return datafile


class PydanticDataset(PydanticStocksBaseItem):
    qc: str | None = None
    dataset_type: str | None = None
    is_raw: bool | None = None
    is_managed: bool = False
    datafiles: List[PydanticDatasetFile]
    collection: str | None = None
    samples: List[PydanticSample | str ] | None
    # note the order is important as pydantic will follow this order when parsing objects
    parent_samples: List[str | PydanticSample | PydanticReferencedStocksObject] | None
    studies: List[str | PydanticStudy | PydanticReferencedStocksObject] | None
    assay: str | PydanticAssay | PydanticReferencedStocksObject | None

    @validator('qc', pre=True)
    def check_qc(cls, qc):
        if isinstance(qc, dict):
            return qc['label']
        return qc

    @validator('dataset_type', pre=True)
    def check_dataset_type(cls, dataset_type):
        if isinstance(dataset_type, dict):
            return dataset_type['label']
        return dataset_type


##
## Pydantic classes used to post new datasets with optional samples, associated assays, collection
## and instrument run
## We have the following situations
## - derived datasets with optional link to sample(s) and parent dataset(s); also reference to assay is possible
## - raw dataset(s) with link to sample(s) and assay(s) information and run information
##

class PyDatasetListPost(BaseModel, extra=Extra.ignore):
    input_dir: str
    allow_pooled_samples: bool
    transfer_whole_input_dir: bool = True
    owned_by: str
    run: Optional[PydanticInstrumentRun]
    assays: Optional[List[PydanticAssay]] = list()
    collections: Optional[List[PydanticDatasetCollection]] = list()
    samples: Optional[List[PydanticSample]] = list()
    datasets: Optional[List[PydanticDataset]] = list()


class PyOldDatasetListPost(PyDatasetListPost):
    class Config:
        extra = Extra.ignore
        fields = {'run': {'exclude': True}}
