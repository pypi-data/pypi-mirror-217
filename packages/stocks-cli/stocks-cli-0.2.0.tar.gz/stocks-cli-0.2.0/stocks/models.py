# -*- coding: utf-8 -*-
"""
Defines the STOCKS models
Here we define a few coding convention:
- do not init list or dict props with empty list or dict. They must be None until a value is added
This will allow to get these attributes exported to JSON if empty
- nested objects should always accept either the object or a str so one can either indicate the object or its ID.
In teh case of an ID, it must be a valid STOCKS UUID


"""
import logging
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional, Dict, Union, Any, Set
from jsonpickle import encode
from cli.utils import Technology, SequencingRunType, SequencingReadType, UserRole, ObjectState, \
    ExperimentStatus, NanoporeLiveBaseCallingType, NanoporeAdaptiveMode

logger = logging.getLogger(__name__)


class CreatableMixin:
    def __init__(self, created: Optional[datetime] = None, created_by: Optional["User"] | str = None, **kwargs):
        self.created: datetime | None = created
        self.created_by: Optional["User"] | str = created_by
        super().__init__(**kwargs)


class ModifiableMixin:
    def __init__(self, modified: Optional[datetime] = None, modified_by: Optional["User"] | str = None, **kwargs):
        self.modified: datetime | None = modified
        self.modified_by: Optional["User"] | str = modified_by
        super().__init__(**kwargs)


class DeletableMixin:
    def __init__(self, deleted: bool = False, deleted_by: Optional["User"] | str = None,
                 deleted_date: Optional[datetime] = None, **kwargs):
        self.deleted: bool = deleted
        self.deleted_by: Optional["User"] | str = deleted_by
        self.deleted_date: Optional[datetime] = deleted_date
        super().__init__(**kwargs)


class ProtocolableMixin:
    def __init__(self, protocols: List["Protocol"] | None = None, **kwargs):
        self.protocols: List["Protocol"] | None = protocols
        super().__init__(**kwargs)


class ProtectableMixin:
    # TODO: implement permission support when needed
    def __init__(self, permissions=None, **kwargs):
        self.permissions = permissions
        super().__init__(**kwargs)


class OwnableMixin:
    """
    Mixin for object that can be owned. An Owned object has a owner and is also owned_by a group_name
    """

    def __init__(self, owner: Optional["User"] | str = None, owned_by: str | None = None, **kwargs):
        self.owner: Optional["User"] | str = owner
        self.owned_by: str = owned_by
        if not self.owned_by and isinstance(owner, User) and owner.groups:
            self.owned_by = next(iter([grp.name for grp in owner.groups.values() if grp.is_primary_group]),
                                 list(owner.groups.values())[0].name)
        super().__init__(**kwargs)

    def set_owner(self, owner: "User", also_set_group=True):
        """
        sets the owner and also optionally resets the group_name according to the owner's group_name
        :param owner:
        :param also_set_group: if True the owner's group_name prop propagates to the owned_by field
        :return:
        """
        self.owner = owner
        if also_set_group and owner.groups:
            self.owned_by = next(iter([grp.name for grp in owner.groups.values() if grp.is_primary_group]),
                                 list(owner.groups.values())[0].name)


class AnnotableMixin:
    """
    Mixin for object that can be annotated.
    """

    def __init__(self, annotations: Optional[dict] = None, **kwargs):
        self.annotations: dict | None = annotations
        super().__init__(**kwargs)

    def add_annotation(self, annot_key: str, annot_value: str):
        if not self.annotations:
            self.annotations = {}
        self.annotations[annot_key] = annot_value


###
# Classes that are not yet in STOCKS
###

class Ontology:
    """
    Class representing an ontology, it has a name and a URL. Both are supposed to be unique and can be used as unique
     keys.
    """

    def __init__(self, name: str, url: Optional[str] = None, description: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.name: str = name
        self.description: str = description
        self.url: Optional[str] = url


class OntologyTerm:
    """
    A term from an ontology.
    id, name, description, owner and annotations inherited and represent the CV instance from STOCKS,
    and where name can be different from term_name
    """

    def __init__(self, name: str, term_id: str, ontology: Ontology, description: Optional[str] = None, **kwargs):
        """
        :param name: the term's name in the ontology
        :param term_id: the term's id in the ontology
        :param ontology: the ontology this term belongs to
        """
        super().__init__(**kwargs)
        self.name: str = name
        self.term_id: str = term_id
        self.ontology: Ontology = ontology
        self.description = description


###
# Classes that are in STOCKS
###

class StocksBaseItem:
    """
    Base class for a STOCKS object exposing basic id, name and description properties.
    """

    def __init__(self, name: str, id: Optional[str] = None, description: Optional[str] = None, **kwargs):
        if kwargs:
            # kwargs is still not empty, we need to warn this as this maybe not normal
            logger.info(f"Potential typo/bug: kwargs not empty one ce reached StocksBaseItem => {str(kwargs)}")
        self.name: str = name
        self.id: str = id
        self.description: str = description
        # map to STOCKS model type
        self.stocks_model_type: str = "DEFAULT"
        # we do not propagate kwargs to object class
        super().__init__()

    def as_simple_json(self):
        return encode(self, unpicklable=False, indent=2, make_refs=False)


class UserGroup(StocksBaseItem):

    def __init__(self, name: str, id: Optional[str] = None, description: Optional[str] = None,
                 is_primary_group: bool = False, **kwargs):
        """
        :param name: the name of this group_name
        :param id: the STOCKS UUID
        """
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type = "GROUP"
        self.is_primary_group: bool = is_primary_group


class User(StocksBaseItem):
    """
    A base class for a user
    """

    def __init__(self, username: str, last_name: str = None, id: str = None,
                 groups: List['UserGroup'] | Dict[str, 'UserGroup'] = None, email: Optional[str] = None,
                 institution: Optional[str] = None, date_joined: Optional[datetime] = None,
                 is_superuser: Optional[bool] = None, is_staff: Optional[bool] = None, is_active: Optional[bool] = None,
                 middle_name: Optional[str] = None, first_name: str = None, full_name: str = None, name: str = None,
                 **kwargs):
        if not name:
            name = last_name
        super().__init__(name=name, id=id, **kwargs)
        self.stocks_model_type = "USER"
        self.username: str = username
        self.first_name: Optional[str] = first_name
        self.last_name: Optional[str] = last_name
        self.middle_name: Optional[str] = middle_name
        self.unix_group: Optional[str] = None  # unix group_name name
        self.unix_name: Optional[str] = None  # unix user name
        self.email: Optional[str] = email  # user email
        self.orcid: Optional[str] = None  # user ORCID ID

        self.groups: Dict[str, 'UserGroup'] = {}
        if groups:
            self.groups = {}
            if isinstance(groups, list):
                logger.warning(f"groups => {type(groups)}")
                for grp in groups:
                    logger.warning(f"grp {grp} of type \n {type(grp)}")
                    self.groups[grp.name] = grp
            elif isinstance(groups, dict):
                self.groups = groups
        assert(isinstance(self.groups, dict))

        self.institution: Optional[str] = institution  # user institution
        self.date_joined: Optional[datetime] = date_joined
        self.is_superuser: Optional[bool] = is_superuser
        self.is_staff: Optional[bool] = is_staff
        self.is_active: Optional[bool] = is_active
        self.full_name = full_name

    def add_user_group(self, group: UserGroup):
        if not self.groups:
            self.groups = {}
        self.groups[group.name] = group

    def get_primary_group(self) -> UserGroup | None:
        for group in self.groups.values():
            if group.is_primary_group:
                return group
        return None


class UserMember(User):
    """
    A user with a list membership roles
    """

    def __init__(self, user: User, roles: Set[UserRole], **kwargs):
        super().__init__(username=user.username, id=user.id, groups=user.groups, email=user.email,
                         first_name=user.first_name, middle_name=user.middle_name, last_name=user.last_name,
                         institution=user.institution, **kwargs)
        self.roles: Set[UserRole] = roles


class Project(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, AnnotableMixin, StocksBaseItem):
    """
    A class representing a Project
    """

    def __init__(self, name: str, description: Optional[str] = None, id: Optional[str] = None,
                 user_roles: Optional[List[UserMember]] = None, **kwargs):
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type: str = "PROJECT"
        self.user_roles: List[UserMember] = user_roles


class Experiment(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, StocksBaseItem):
    def __init__(self, name: str, status: ExperimentStatus, project: Project | str, is_frozen: bool = False,
                 summary: Optional[str] = None, description: Optional[str] = None,
                 protocol: Optional["Protocol"] = None,
                 start_date: Optional[datetime] = None, completed_date: Optional[datetime] = None,
                 estimated_completion_date: Optional[datetime] = None, freeze_date: Optional[datetime] = None,
                 id: Optional[str] = None, **kwargs):
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type: str = "EXPERIMENT"
        self.status: ExperimentStatus = status
        self.project: "Project" | str = project
        self.is_frozen: bool = is_frozen
        self.summary: str = summary
        self.description: str = description
        self.protocol: Optional["Protocol"] = protocol
        self.start_date: datetime | date | None = start_date
        self.completed_date: datetime | date | None = completed_date
        self.estimated_completion_date: datetime | date | None = estimated_completion_date
        self.freeze_date: datetime | date | None = freeze_date


class StocksCVCategory(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, StocksBaseItem):
    """
    A CV category in STOCKS
    id, name, description, owner and annotations inherited and represent the CV instance from STOCKS,
    and where name can be different from term_name
    """

    def __init__(self, name: str, id: Optional[str] = None, description: Optional[str] = None,
                 default_ontology: Optional[Ontology] = None,
                 allowed_ontologies: Optional[List[Ontology]] = None, **kwargs):
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type = "CATEGORIES"
        self.default_ontology = default_ontology  # source in STOCKS?
        self.allowed_ontologies = allowed_ontologies


class StocksCVTerm(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, StocksBaseItem):
    """
    A CV term in STOCKS
    """

    def __init__(self, name: str, id: Optional[str] = None, description: Optional[str] = None,
                 category: StocksCVCategory | str | None = None,
                 ontology_mappings: Optional[Dict[str, OntologyTerm]] = dict(), **kwargs):
        """
        :param name: the STOCKS term name
        :param category: the STOCKS term category, or a UUID for the category or none
        :param ontology_mappings: optional mappings to ontologies as a dict keyed by Ontology
        """
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type = "TERMS"
        self.category: StocksCVCategory = category
        self.ontology_mappings: Optional[Dict[str, OntologyTerm]] = ontology_mappings


class InstrumentModel(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, StocksBaseItem):
    def __init__(self, name: str, technology: Technology, platform: str,
                 id: Optional[str] = None, description: Optional[str] = None, **kwargs):
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type = "INSTRUMENTMODEL"
        self.technology: Technology = technology
        self.platform: str = platform


class Instrument(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, AnnotableMixin, StocksBaseItem):
    def __init__(self, name: str, model: str, serial_number: Optional[str] = None,
                 id: Optional[str] = None, description: Optional[str] = None, **kwargs):
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type = "EQUIPMENT"
        self.model: InstrumentModel | str = model
        self.serial_number: str = serial_number


class Sample(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, AnnotableMixin, StocksBaseItem):
    def __init__(self, name: str, id: Optional[str] = None, description: Optional[str] = None, **kwargs):
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type = "GENERICSAMPLE"
        self.sample_type: Optional[str] = None
        self.application: Optional[str] = None
        self.provider_sample_name: Optional[str] = None  # eg genecoreid
        self.provider_sample_id: Optional[str] = None  # eg genecorereaction


class SequencingLibrary(Sample):
    def __init__(self, name: str, barcode: Optional[str], id: Optional[str] = None, description: Optional[str] = None,
                 **kwargs):
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type = "SEQUENCINGLIBRARY"
        self.barcode: str = barcode


class DatasetFile(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, AnnotableMixin, StocksBaseItem):
    def __init__(self, name: str, mime_type: str, byte: int, filetype: str, is_dir: bool = False,
                 uri: Optional[str] = None, md5sum: Optional[str] = None,
                 id: Optional[str] = None, description: Optional[str] = None, **kwargs):
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type = "DATAFILE"
        self.uri: str = uri
        self.md5sum: str = md5sum
        self.byte: int = byte
        self.mime_type: str = mime_type
        self.filetype: str = filetype
        # TODO: renae to is_folder to align with API
        self.is_dir: bool = is_dir


class DatasetFileCopy(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, StocksBaseItem):
    def __init__(self, name: str, uri: str, is_primary_copy: bool, shortname: Optional[str] = None,
                 id: Optional[str] = None, **kwargs):
        super().__init__(name=name, id=id, **kwargs)
        self.uri: str = uri
        self.shortname: str = shortname
        self.is_primary_copy: bool = is_primary_copy
        self.dataset: DatasetFile | str | None = None

class FastqFile(DatasetFile):
    def __init__(self, name: str, read_type: SequencingReadType, mime_type: str, byte: int,
                 filetype: str = "fastq",
                 uri: Optional[str] = None, md5sum: Optional[str] = None,
                 id: Optional[str] = None, description: Optional[str] = None, **kwargs):
        super().__init__(name=name, mime_type=mime_type, byte=byte, filetype=filetype,
                         uri=uri, md5sum=md5sum, is_dir=False,
                         id=id, description=description, **kwargs)
        self.read_type: SequencingReadType = read_type


class FastqDir(DatasetFile):
    def __init__(self, name: str, read_type: SequencingReadType, mime_type: str,
                 uri: Optional[str] = None, id: Optional[str] = None, description: Optional[str] = None, **kwargs):
        super().__init__(name=name, mime_type=mime_type, byte=0, filetype="fastq", is_dir=True,
                         uri=uri, md5sum="", id=id, description=description, **kwargs)
        self.read_type: SequencingReadType = read_type


class Fast5File(DatasetFile):
    def __init__(self, name: str, byte: int, uri: Optional[str] = None, md5sum: Optional[str] = None,
                 id: Optional[str] = None, description: Optional[str] = None, **kwargs):
        super().__init__(name=name, mime_type="application/x-hdf5", byte=byte, filetype="fast5",
                         uri=uri, md5sum=md5sum, id=id, description=description, is_dir=False, **kwargs)


class Fast5Dir(DatasetFile):
    def __init__(self, name: str, uri: Optional[str] = None, id: Optional[str] = None,
                 description: Optional[str] = None, **kwargs):
        super(Fast5Dir, self).__init__(name=name, mime_type="application/x-hdf5", byte=0, filetype="fast5", uri=uri,
                                       md5sum="", id=id, description=description, is_dir=True, **kwargs)


class Dataset(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, AnnotableMixin, StocksBaseItem):
    """
    datafiles
    """

    def __init__(self, name: str, is_raw: bool, id: Optional[str] = None, description: Optional[str] = None,
                 datafiles: List[DatasetFile | str] | None = None, dataset_type: str = "generic",
                 samples: List[Sample] | None = None,
                 collection: Optional["DatasetCollection"] = None,
                 **kwargs):
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type = "DATASET"
        self.dataset_type: str = dataset_type
        self.is_raw = is_raw
        self.datafiles: List[DatasetFile] | List[str] | None = datafiles if datafiles else None
        self.samples: List[Sample] = samples
        self.collection: DatasetCollection = collection  # in stocks a dataset can belong to many collections

    def add_datafile(self, df: DatasetFile):
        if not self.datafiles:
            self.datafiles = []
        self.datafiles.append(df)


class DatasetCollection(StocksBaseItem):
    """
    A class representing a collection of dataset. It adds the dataset_id_list to store, in an ordered-preserved way,
    the dataset IDs.
    """

    def __init__(self, name: str, id: Optional[str] = None, description: Optional[str] = None,
                 datasets: List[Dataset | str] | None = list(), **kwargs):
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type = "DATASETCOLLECTION"
        self.datasets: List[Dataset | str] | None = datasets


class Protocol(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, AnnotableMixin, StocksBaseItem):
    """
    A class representing a Protocol. Adds a type as an ontological term
    id, name, description, owner and annotations inherited
    TODO: add support for protocol parameters
    """

    def __init__(self, name: str, protocol_type: OntologyTerm, id: Optional[str] = None,
                 description: Optional[str] = None, summary: Optional[str] = None, **kwargs):
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type = "PROTOCOL"
        self.protocol_type: OntologyTerm = protocol_type
        self.summary: str = summary


class AnnotationType(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, StocksBaseItem):

    def __init__(self, name: str, id: Optional[str] = None, description: Optional[str] = None, **kwargs):
        """
        :param name: the name of this annotation type
        :param id: the STOCKS UUID
        """
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type = "ANNOTATIONTYPE"


class Study(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, AnnotableMixin, DatasetCollection):
    """
    A class representing a Study.
    """

    def __init__(self, name: str, id: Optional[str] = None, description: Optional[str] = None,
                 datasets: Optional[List[Dataset]] = None,
                 user_roles: Optional[Dict[str, UserMember]] = None,
                 experimental_design_terms: Optional[List[StocksCVTerm]] = None,
                 experimental_factors: Optional[List[str]] = None,
                 protocols: List[Protocol | str] | None = None, **kwargs):
        """
        :param name: the study name
        :param datasets: the optional list of datasets grouped in this study
        :param user_roles: the role(s) of each study's participant
        :param experimental_design_terms: the CV terms describing this study design
        :param experimental_factors: the ProtocolType, AnnotationType or str representing the experimental factors
        When a string is given, it represents the key(s) to look up in the annotation dict of the datasets
        :param protocols:
        """
        super().__init__(name=name, id=id, description=description, datasets=datasets, **kwargs)
        self.stocks_model_type = "STUDY"
        self.user_roles: Dict[str, UserMember] = user_roles
        self.experimental_design_terms: Optional[List[StocksCVTerm]] = experimental_design_terms  # design in STCOKS
        self.experimental_factors: Optional[List[str]] = experimental_factors
        self.protocols: Optional[List[Protocol | str]] = protocols  # unique set of protocol used across this study
        self.assays: List[Union[NanoporeAssay, SequencingAssay, Assay]] | None = None
        # TODO: add ref to Project

    def add_experimental_design_term(self, term: StocksCVTerm):
        if not self.experimental_design_terms:
            self.experimental_design_terms = []
        self.experimental_design_terms.append(term)

    def add_experimental_factor(self, exp_factor: str):
        if not self.experimental_factors:
            self.experimental_factors = []
        self.experimental_factors.append(exp_factor)

    def add_protocol(self, protocol: Protocol):
        if not self.protocols:
            self.protocols = []
        self.protocols.append(protocol)

    def add_user(self, user: UserMember) -> None:
        if not self.user_roles:
            self.user_roles = {user.username: user}
        else:
            is_user = self.user_roles.get(user.username)
            if is_user:
                self.user_roles[user.username].roles.update(user.roles)
            else:
                self.user_roles[user.username] = user


class DataProducer:
    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name: str = name


class SimpleInstrumentRun(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, AnnotableMixin, StocksBaseItem):
    def __init__(self, name: str, id: Optional[str] = None, description: Optional[str] = None,
                 instrument: Optional[Instrument | dict] = None, producer: Optional[DataProducer] = None,
                 start_datetime: Optional[Any] = None, end_datetime: Optional[Any] = None,
                 run_duration: Optional[str] = "", assays: List["Assay"] | List[str] | None = None,
                 **kwargs):
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type = "INSTRUMENTRUN"
        if instrument and isinstance(instrument, dict):
             instrument = Instrument(**instrument)
        self.instrument: Instrument = instrument
        self.producer: DataProducer = producer
        self.start_datetime: Any = start_datetime
        self.end_datetime: Any = end_datetime
        self.run_duration: str = run_duration
        self.assays: List["Assay"] | List[str] | None = assays

    def add_assay(self, assay: "Assay"):
        if not self.assays:
            self.assays = list()
        self.assays.append(assay)

class InstrumentRun(SimpleInstrumentRun):
    def __init__(self, name: str, managed: bool, technology: Technology, platform: str,
                 id: Optional[str] = None, description: Optional[str] = None,
                 instrument: Optional[Instrument] = None, producer: Optional[DataProducer] = None,
                 start_datetime: Optional[Any] = None, end_datetime: Optional[Any] = None,
                 run_duration: Optional[str] = "", assays: List["Assay"] | List[str] | None = None,
                 **kwargs):
        super().__init__(name=name, id=id, description=description, instrument=instrument, producer=producer,
                         start_datetime=start_datetime, end_datetime=end_datetime, run_duration=run_duration,
                         assays=assays, **kwargs)
        self.managed: bool = managed  # stocks => is_managed
        self.technology: Technology = technology
        self.platform: str = platform


class Assay(OwnableMixin, CreatableMixin, ModifiableMixin, DeletableMixin, AnnotableMixin, StocksBaseItem):
    def __init__(self, name: str, technology: Technology, id: Optional[str] = None,
                 platform: str = "OTHER", description: Optional[str] = None,
                 datasets: List[Dataset] | None = None, samples: List[Sample] | None = None,
                 instrumentrun: InstrumentRun | str = None, instrumentmodel: InstrumentModel | str = None,
                 multiplexed: bool = None,
                 run_dir: Optional[Path] = None, state: Optional[ObjectState] = None,
                 **kwargs):
        super().__init__(name=name, id=id, description=description, **kwargs)
        self.stocks_model_type = "GENERICASSAY"
        self.technology: Technology = technology
        self.platform: str = platform
        if not multiplexed and samples:
            self.multiplexed = len(samples) > 1
        elif not multiplexed:
            self.multiplexed = False
        else:
            self.multiplexed: bool = multiplexed
        self.instrumentrun: InstrumentRun | str | None = instrumentrun
        self.instrumentmodel: InstrumentModel | str | None = instrumentmodel
        self.run_dir: Optional[Path] = run_dir
        self.state: Optional[ObjectState] = state
        if multiplexed is None and samples:
            self.multiplexed = len(samples) > 1
        self.datasets: List[Dataset] = datasets  # datasets_out
        self.samples: Dict[str, Sample] | None = None  # samples_in
        if samples and len(samples) > 0:
            self.add_samples(samples)

    def add_sample(self, sample: Sample):
        if not self.samples:
            self.samples = []
        self.samples[sample.name] = sample

    def add_samples(self, samples: List[Sample]):
        if not self.samples:
            self.samples = samples
        else:
            self.samples = {}
            for smpl in samples:
                self.samples[smpl.name] = smpl


class SequencingAssay(Assay):
    def __init__(self, name: str, flowcell: str, id: Optional[str] = None,
                 platform: str = "ILLUMINA", description: Optional[str] = None,
                 datasets: Optional[List[Dataset]] = None, samples: Optional[List[Sample]] = None,
                 chemistry: str = "", instrumentrun: InstrumentRun | str = None, lane: int = 1,
                 multiplexed: bool = None, demultiplexed: bool = None,
                 runtype: SequencingRunType = SequencingRunType.SINGLE_END, runmode: str = "",
                 readlength: str = None, **kwargs):
        super().__init__(name=name, id=id, description=description,
                         technology=Technology.SEQUENCING, platform=platform,
                         datasets=datasets, samples=samples, instrumentrun=instrumentrun,
                         multiplexed=multiplexed, **kwargs)
        self.stocks_model_type = "NGSILLUMINAASSAY"

        if demultiplexed is None:
            if multiplexed is False:
                self.demultiplexed = False
            elif datasets and samples and len(datasets) == len(samples) and len(samples) > 1:
                self.demultiplexed = True
            else:
                self.demultiplexed = False
        else:
            self.demultiplexed: bool = demultiplexed

        self.flowcell: str = flowcell
        self.flowcell_version: str = ""
        self.lane: int = lane
        self.runtype: SequencingRunType = runtype
        self.runmode: str = runmode
        self.readlength: str = readlength
        self.chemistry: str = chemistry


class NanoporeAssay(SequencingAssay):
    def __init__(self, name: str, flowcell: str, flowcell_version: str,
                 id: Optional[str] = None, description: Optional[str] = None,
                 datasets: Optional[List[Dataset]] = None, samples: Optional[List[Sample]] = None,
                 chemistry: str = "", instrumentrun: InstrumentRun | str = None,
                 multiplexed: bool = None, demultiplexed: bool = None, run_mode: str = None,
                 **kwargs):
        super().__init__(name=name, id=id, description=description, platform="NANOPORE",
                         flowcell=flowcell,
                         datasets=datasets, samples=samples, chemistry=chemistry,
                         instrumentrun=instrumentrun, lane=1, multiplexed=multiplexed,
                         demultiplexed=demultiplexed, runtype=SequencingRunType.SINGLE_END,
                         runmode=run_mode, **kwargs)
        self.stocks_model_type = "NANOPOREASSAY"
        self.flowcell_version = flowcell_version
        self.live_base_calling: NanoporeLiveBaseCallingType = NanoporeLiveBaseCallingType.NONE
        self.live_read_mapping: bool = False
        self.genome_reference: Optional[str] = None  # genome_reference
        self.adaptive_mode: NanoporeAdaptiveMode = NanoporeAdaptiveMode.NONE
        self.adaptive_mode_details: str = ""
