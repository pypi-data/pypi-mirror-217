# -*- coding: utf-8 -*-
"""
A manager to interact with STOCKS API. Uses the STOCKS client in the background
Guidelines on how to write methods and expected return behavior:
- fetch_* methods expect an ID and will load the corresponding object or throw an error. A distinction is made
between missing permissions which raises PermissionError and other issues which raise HTTPException
 Returned object should be from the STOCKS models i.e. pydantic objects (or alike) should be restricted to transport
  logics and hidden from users.

- list_* or search_* methods always return a potentially empty array (or alike) of objects matching the
request (and the permission system). Returned objects should be from the STOCKS models i.e. pydantic objects (or alike)
 should be restricted to transport logics and hidden from users.
 These methods never raise PermissionError while they can raise HTTPException in case of unexpected issues

"""

import json
import os
from enum import Enum
from pathlib import Path
from typing import Set
from urllib.parse import urljoin
from uuid import uuid4

from stocks import STOCKS_PROTOCOL_TYPE_TO_EFO
# from stocksapi import pydantic_protocol_to_protocol, pydantic_user_to_user, pydantic_illuminaassay_to_assay, \
#     pydantic_dataset_to_dataset, pydantic_study_to_study
from stocksapi.exceptions import HTTPException, MultipleObjectMatchedError, ItemNotFoundException
from stocksapi.models import *
from stocks.models import Protocol, Assay, Study, User, Dataset, AnnotationType, InstrumentRun, DatasetCollection, \
    Sample, SequencingAssay, Project, UserGroup, StocksCVTerm, Experiment, Ontology, OntologyTerm, \
    DatasetFileCopy, SimpleInstrumentRun, OwnableMixin, AnnotableMixin, StocksBaseItem,SequencingLibrary
from stocksapi.client import StocksClient, model_to_url
from cli.utils import HTMLFilter, ModelType, is_uuid, ExtendedEnum

logger = logging.getLogger(__name__)


def handle_response(response, fail_on_missing_permission=True) -> Any | None:
    """
    :param response: Response from the stocks API
    :param fail_on_missing_permission: raise PermissionError if unauthorized request unless false (return None)
    :return: request results or None
    :raises PermissionError if unauthorized request and fail_on_missing_permission True
    :raises ItemNotFoundException if 404 is returned
    :raises HTTPException if other error
    """
    code, results = response
    if code in [200, 201, 204]:
        return results
    elif code == 401:
        if fail_on_missing_permission:
            # logger.debug(f"request error code {code}: Unauthorized.")
            raise PermissionError(results['message'])
        else:
            logger.error(f"request error code {code}: Unauthorized.")
            return None
    elif code == 403:
        if fail_on_missing_permission:
            # logger.debug(f"request error code {code}: Permission.")
            raise PermissionError("Access denied.")
        else:
            logger.error(f"request error code {code}: Permission.")
            return None
    elif code == 404:
        raise ItemNotFoundException(status_code="404")
    # TODO http POST error codes
    else:
        logger.error(f"Got error code {code}: {results} ")
        if isinstance(results, dict) and 'message' in results:
            # logger.error(f"request error code {code} with message: {results['message']}")
            raise HTTPException(status_code=code, detail=results['message'])
        else:
            # logger.error(f"request error code {code} for {results}.")
            raise HTTPException(status_code=code, detail=results)


def _check_result(payload: Dict, uuid: str, model_type: str) -> Dict | List | None:
    """
    Internal method to parse and check the validity of the JSON response received from the Stocks server.
    Returns None if response JSON is None.
    Instance payload:
    {
        "results": {...}
    }
    List payload:
    {
        "previous": null,
        "next": null,
        "current": 1,
        "total": 1,
        "total_pages": 1,
        "results": [
            {...},
            {...}
        ]
    }
    :param payload: Payload received from the Stocks server
    :param uuid: Id used to fetch the payload
    :param model_type:  type of object the fetch is getting.
    :raises TypeError: The payload is not a dictionary
    :raises ValueError: 'results' is not present as dictionary key.
    :return: A JSON or a List of JSON or None
    """
    if payload is None:
        # this method does not handle None that are given by the handle_response method
        return None
    if not isinstance(payload, dict):
        logger.error(f"Request for {model_type} yielded wrong type {type(payload)}. ID: {uuid}")
        raise TypeError(f"Error with {model_type} type: {type(payload)} should be a json.")
    if 'results' not in payload:
        logger.error(f"Request for {model_type} yielded wrong format. ID: {uuid}")
        logger.debug(f"{model_type} printout: {payload}")
        raise ValueError(f"Error with {model_type} value: unexpected dictionary format: 'results' field missing.")
    if isinstance(payload['results'], list):
        if len(payload['results']) == 0:
            logger.debug(f"Search for {model_type} yielded no results. ID: {uuid}")
            # raise ValueError(f"Error with {name} value: results list empty.")
    return payload['results']


def _convertTypeFieldToPydanticNameField(o: PydanticStocksBaseItem):
    """
    convertion needed to POST object
    """
    o.type = PydanticNameField(name=o.type)
    return o

def _convertFieldsToPydanticValueField(o: PydanticStocksBaseItem, fields: List[str]):
    """
    converts a list of props in their equivalent PydanticValueField objects
    """
    for f in fields:
        logger.debug(f)
        v = getattr(o, f, None)
        if v:
            if isinstance(v, Enum):
                v = v.value
            logger.debug(f"{type(v)} +> {v}")
            setattr(o, f, PydanticValueField(value=str(v)))
    return o


class StocksManager:

    def __init__(self, client: StocksClient):
        """
        :param client: an initialized client to talk to the STOCKS API
        """
        self.client = client
        self.logged_in_user: User = self.fetch_user(client.username)

    def upload_attachment(self, path: str, id: str, model_type: ModelType):
        """
        Adds an attachement file to STOCKS item. Keeps the file name.
        :param path: Path to file to upload
        :param id: UUID of STOCKS item to attach file to
        :param model_type: utils.ModelType of item
        :raises ValueError: if parsing of modeltype not conform to path formated as "x/y/"
        """
        # url = f"{model_to_url[model_type]}{id}/attachments/"
        appmodel = model_to_url[model_type].split("/")
        if len(appmodel) < 3:
            raise ValueError(f"Wrong model type {model_type.value} to upload an attachment")
        name = os.path.basename(path)
        params = self.get_query_params({"app": appmodel[0], "model": model_type.value, "object_id": id})
        file = {"file": (name, open(path, 'rb').read(), "text/plain")}  # 'text/plain' mimetype to force "raw" upload
        resp = handle_response(self.client.post("attachments/", file=file, query_params=params))

    def fetch_annotation_id_from_item(self, model: ModelType, id: str, ann_type: str | None = None) -> str | None:
        """
        Search for an annotation within an item and returns its id if the annotation is found, else None.
        :param model: ModelType of the item to be searched
        :param id: STOCKS uuid of the item to be searched
        :param ann_type: Annotation Type of the annotation looked for
        :return: Id of an annotation if present, else None
        """
        res = self._fetch_annotation_from_item(model, id, ann_type)
        if res:
            return res[1]
        return None

    def fetch_annotation_value_from_item(self, model: ModelType, id: str, ann_type: str | None = None) -> str | None:
        """
        Search for an annotation within an item and returns its value if the annotation is found, else None.
        :param model: ModelType of the item to be searched
        :param id: STOCKS uuid of the item to be searched
        :param ann_type: Annotation Type of the annotation looked for
        :return: Value of an annotation if present, else None
        """
        res = self._fetch_annotation_from_item(model, id, ann_type)
        if res:
            return res[0]
        return None

    def _fetch_annotation_from_item(self, model: ModelType, id: str, ann_type: str | None = None) \
            -> tuple[str, str] | None:
        """
        TODO make this more generic
        Search for an annotation within an item and returns its value and id if the annotation is found, else None.
        :param model: ModelType of the item to be searched
        :param id: STOCKS uuid of the item to be searched
        :param ann_type: Annotation Type of the annotation looked for
        :return: Value, id of an annotation if present, else None
        """
        url = f'{model_to_url[model]}{id}/annotations/'
        query_params = self.get_query_params({"search": ann_type})
        res = _check_result(handle_response(self.client.get(url, query_params)), id, ann_type)
        if res:
            return res[0]["value"], res[0]["id"]
        return None

    def fetch_dataset_metatable(self, uuid: str, format: str = "csv", for_magetab = False):
        """
        Fetch a dataset-oriented summary table for a given study.
        :param uuid: the study/project/assay/datasetcollection UUID
        :param format: 'csv' or 'xlsx' (or raise a ValueError).
        :param for_magetab: this is a temp param, which you can turn to False to use the new generic API datafilemeta_export endpoint
        :return: csv formatted text or binary text if format is 'xlsx'
        """
        query_params = self.get_query_params(None)
        query_params["response_format"] = "flat"
        query_params["page_size"] = "max"
        if format not in ["xlsx", "csv"]:
            raise ValueError(f"Wrong format, must be xlsx or csv: {format}")
        # fetch
        status, data = self.client.resolve(uuid)
        if data["model_name"] == ModelType.STUDY.value:
            query_params["study_id"] = uuid
        elif data["model_name"] == ModelType.PROJECT.value:
            query_params["project_id"] = uuid
        elif data["model_name"] == ModelType.DATASETCOLLECTION.value:
            query_params["datasetcollection_id"] = uuid
        elif data["model_name"] == ModelType.ASSAY.value:
            query_params["assay"] = uuid
        elif data["model_name"] == ModelType.DATASET.value:
            query_params["dataset_id"] = uuid
        else:
            raise ValueError(f'Wrong value provided in the UUID. This must be a Study/Project/Assay/DatasetCollection'
                             f' UUID while {uuid} points to a {data["model_name"]} object')

        url = model_to_url[ModelType.DATASET]
        url = urljoin(url, "datafilemeta_export")
        data = handle_response(self.client.get(url, query_params))
        if data is None:
            logger.info(f"Request for metatable export yielded not results. Study ID: {uuid}")
        return data

    def list_annotations_from_item(self, model: ModelType, id: str) -> List:
        """
        Returns a list of all the annotations for one item of type [model] and id [id].
        :raises TypeError: if 'model' argument not ModelType.
        :raises ValueError: if 'results' field misisng from JSON response.
        """
        if type(model) is not ModelType:
            raise TypeError(f"Argument model {model} needs to be ModelType")
        url = f'{model_to_url[model]}{id}/annotations/'
        query_params = self.get_query_params(None)
        res = handle_response(self.client.get(url, query_params))
        if 'results' not in res:
            raise ValueError(f"'results' field missing from response for item {id}")
        return res['results']

    def fetch_stocks_cv_term(self, uuid: str) -> StocksCVTerm | None:
        """
        Fetch a CV Term object from Stocks server.
        Extracts Ontology and Ontology Term from the dbxref if present.
        :param uuid: The CV Term's UUID.
        :return: models.StocksCVTerm from stocks package
        """
        results = self.fetch_item(uuid, ModelType.TERM)
        pydantic_term: PydanticCVTerm = PydanticCVTerm.parse_obj(results)
        dbxref_id = pydantic_term.dbxref_id
        d = pydantic_term.dict()
        if dbxref_id:
            onto = Ontology(name=dbxref_id.split("/")[-1].replace(':', '_').split("_")[0], url=dbxref_id.rsplit("/", 1)[0])
            onto_term = OntologyTerm(name=pydantic_term.name, term_id=dbxref_id.split("/")[-1], ontology=onto)
            ontology_mappings = {onto.name: onto_term}
            d['ontology_mappings'] = ontology_mappings
        term: StocksCVTerm = StocksCVTerm(**d)
        return term

    def fetch_assay(self, uuid: str, load_ownership: bool=False) -> SequencingAssay | None:
        """
        gets assay details
        :param uuid: the assay's UUID
        :param load_ownership: True to fetch User onject from stocks, else owner is username
        :return: a subclass of model.Assay from stocks package
        """
        results = self.fetch_item(uuid, ModelType.ASSAY)
        ass_type = None
        if 'platform' in results and 'value' in results['platform']:
            if isinstance(results["platform"]["value"], dict):
                ass_type = results["platform"]["value"]["value"]
            ass_type = results["platform"]["value"]
        if not ass_type:
            logger.error(f"Error when fetching assay from server: platform value is missing. Assay ID: {uuid}")
            raise ValueError("Error when fetching assay from server: platform value is missing.")

        logger.debug(f"Assay platform: {ass_type}")
        if ass_type.upper() == "ILLUMINA":
            pydantic_assay = PydanticSequencingAssay.parse_obj(results)
            d = pydantic_assay.dict()
            assay = SequencingAssay(**d)

        # TODO non-ILLUMINA assays
        else:
            raise ValueError(f"Error when fetching assay with id {uuid}. Assay Type not supported: {ass_type}.")
            # assay = Assay(name='na', technology=Technology.OTHER)

        if load_ownership:
            self.init_ownership(assay)
        return assay

    def fetch_item(self, uuid: str, model: ModelType, query_params: dict | List = None) -> Any:
        """
        low level method to get item details as returned by the server, with optional query_params
        :param uuid: the item's UUID
        :param model: the STOCKS model name
        :param query_params: either a dict or a list of 'key=value' filters
        :raises ItemNotFoundException on 404
        :return: JSON
        """
        if not isinstance(model, ModelType):
            raise TypeError(f"Parameter model should be of utils.ModelType")
        logger.debug(f"Fetching {model.value} with ID {uuid}")
        query_params = self.get_query_params(query_params)
        try:
            data = handle_response(self.client.get(urljoin(model_to_url.get(model), uuid), query_params))
            return _check_result(data, uuid, model.value)
        except ItemNotFoundException as e:
            e.type = model.value
            e.uuid = uuid
            raise

    def fetch_item_by_name(self, name: str, model: ModelType, query_params: dict | List = None) -> dict | None:
        """
        low level method to get item details as returned by the server by their name
        :param name: the item's name
        :param model: the STOCKS model name
        :param query_params: either a dict or a list of 'key=value' filters
        :return: the item if a unique item matched the query or None if query did not return any hit
        :raise: MultipleObjectMatchedError if multiple objects match the query
        """
        if not isinstance(model, ModelType):
            raise TypeError(f"Parameter model should be of utils.ModelType")
        query_params = self.get_query_params(query_params)
        query_params['name'] = name
        data = handle_response(self.client.get(model_to_url.get(model), query_params))
        dict_or_list = _check_result(data, uuid=name, model_type=model.value)
        if isinstance(dict_or_list, dict):
            return dict_or_list
        elif len(dict_or_list) == 0:
            return None
        elif len(dict_or_list) == 1:
            return dict_or_list[0]
        else:
            raise MultipleObjectMatchedError(results=dict_or_list,
                                             message=f"Looking up {model} objects with name {name} raised"
                                                     f" {len(dict_or_list)} hits. Please use a list method.")


    # def fetch_dataset(self, filter_uuid: str) -> Dataset:
    #     """
    #     gets dataset details
    #     :param filter_uuid: the dataset's UUID
    #     :return: model.Dataset from stocks package
    #     """
    #     results = handle_fetch(self.client.get(model_to_url.get("datasets") + filter_uuid))["results"]
    #     # TODO proper pydantic object and then pydan_to_dataset
    #     # pydantic_dataset = PydanticDataset.parse_obj(results)
    #     # dataset = pydanDataset_to_dataset(pydantic_dataset)
    #     dataset = pydantic_dataset_to_dataset(results)
    #     return dataset

    def fetch_equipment(self, uuid: str) -> Instrument | None:
        data = self.fetch_item(uuid=uuid, model=ModelType.EQUIPMENT)
        py: PydanticInstrument = PydanticInstrument.parse_obj(data)
        fields = py.dict(by_alias=True)
        return Instrument(**fields)

    def fetch_instrument_model(self, uuid: str) -> InstrumentModel | None:
        data = self.fetch_item(uuid=uuid, model=ModelType.INSTRUMENTMODEL)
        py: PydanticInstrumentModel = PydanticInstrumentModel.parse_obj(data)
        fields = py.dict(by_alias=True)
        return InstrumentModel(**fields)

    def fetch_instrument_run(self, uuid: str) -> InstrumentRun | None:
        data = self.fetch_item(uuid=uuid, model=ModelType.INSTRUMENTRUN)
        py: PydanticSimpleInstrumentRun = PydanticSimpleInstrumentRun.parse_obj(data)
        instrument_id: str = py.instrument.id
        # fetch instruemnt details
        data_instr = self.fetch_item(uuid=instrument_id, model=ModelType.EQUIPMENT)
        instrument = PydanticInstrument.parse_obj(data_instr)
        # properly init the model
        data_instr_model = self.fetch_item(
            uuid=instrument.instrumentmodel.id, model=ModelType.INSTRUMENTMODEL)
        instrument.instrumentmodel = PydanticInstrumentModel.parse_obj(data_instr_model)
        # save
        py.instrument = instrument

        fields = py.dict(by_alias=True)
        # we need to add 'managed', 'technology', and 'platform'
        fields['managed'] = False
        fields['technology'] = py.instrument.instrumentmodel.technology
        fields['platform'] = py.instrument.instrumentmodel.platform
        return InstrumentRun(**fields)

    def fetch_project(self, uuid: str) -> Project | None:
        """
        gets study details
        :param uuid: the study's UUID
        :return: model.Study from stocks package
        """
        results = self.fetch_item(uuid, ModelType.PROJECT)
        py: PydanticStocksBaseItem = PydanticStocksBaseItem.parse_obj(results)

        project: Project = Project(id=uuid, name=py.name, description=' '.join(py.description.splitlines()))

        return project

    def fetch_protocol(self, uuid: str) -> Protocol:
        """
        gets protocol details
        :param uuid: the protocol's UUID
        :return: model.Protocol from stocks package
        :raises: ValueError if the protocol type was not found
        """
        results = self.fetch_item(uuid, ModelType.PROTOCOL)
        pydantic_protocol = PydanticProtocol.parse_obj(results)
        if not STOCKS_PROTOCOL_TYPE_TO_EFO.get(pydantic_protocol.type):
            logger.error(f"{pydantic_protocol.type} was not found in stocks.STOCKS_PROTOCOL_TYPE_TO_EFO")
            raise ValueError(f"The protocol type {pydantic_protocol.type} has no mapping to the EFO "
                             f"ontology")
        protocol_type: str = STOCKS_PROTOCOL_TYPE_TO_EFO[pydantic_protocol.type]
        ontology: Ontology = Ontology(protocol_type[1].split("_")[0])
        ontology_term: OntologyTerm = OntologyTerm(protocol_type[0], protocol_type[1], ontology)
        d = pydantic_protocol.dict()
        d['protocol_type'] = ontology_term
        protocol = Protocol(**d)

        return protocol

    def fetch_study(self, uuid: str, load_ownership=False, load_annotations=False) -> Study | None:
        """
        gets study details
        :param uuid: the study's UUID
        :param load_ownership: Boolean, True if User object should be fetched from stocks from the owner ID.
        :param load_annotations: Boolean, True if annotations should be fetched from stocks.
        :return: model.Study from stocks package
        """
        results = self.fetch_item(uuid, ModelType.STUDY)
        pydantic_study: PydanticStudy = PydanticStudy.parse_obj(results)

        # Get design terms as CV objects
        experimental_design_terms: List[StocksCVTerm] = []
        for d in pydantic_study.design:
            stocks_cv_term: StocksCVTerm = self.fetch_stocks_cv_term(d)
            experimental_design_terms.append(stocks_cv_term)
        d = pydantic_study.dict()
        d['experimental_design_terms'] = experimental_design_terms
        study = Study(**d)

        if load_ownership:
            self.init_ownership(study)
        if load_annotations:
            self.add_annotations(study)
        return study

    def fetch_study_dataset_csv_table(self, study_uuid: str):
        """
        Fetch a CSV-formatted dataset-oriented summary table for a given study.
        :param study_uuid: the study's UUID
        :return: binary text in excel-ready format
        """
        return self.fetch_dataset_metatable(study_uuid, "csv")

    def fetch_study_dataset_excel_table(self, study_uuid: str):
        """
        Fetch a excel-formatted dataset-oriented summary table for a given study.
        :param study_uuid: the study's UUID
        :return: binary text in excel-ready format
        """
        return self.fetch_dataset_metatable(study_uuid, "xlsx")

    def fetch_usage_logs_csv_table(self, start_date: datetime, end_date: datetime, resolution: str, aggregate: bool):
        """
        Fetch usage logs in a CSV format
        :param start_date: usage logs starting from this date
        :param end_date: usage logs starting till this date
        :param resolution: group user count per day, month or year. One of 'day', 'month', 'year'
        :param aggregate: Aggregate user counts. If set to false, a row per unique user is returned.
        :return: binary text in excel-ready format
        """
        return self._fetch_usage_logs_table(start_date=start_date, end_date=end_date, resolution=resolution,
                                            aggregate=aggregate, format="csv")

    def fetch_usage_logs_excel_table(self, start_date: datetime, end_date: datetime, resolution: str, aggregate: bool):
        """
        Fetch usage logs in a CSV format
        :param start_date: usage logs starting from this date
        :param end_date: usage logs starting till this date
        :param resolution: group user count per day, month or year. One of 'day', 'month', 'year'
        :param aggregate: Aggregate user counts. If set to false, a row per unique user is returned.
        :return: binary text in excel-ready format
        """
        return self._fetch_usage_logs_table(start_date=start_date, end_date=end_date, resolution=resolution,
                                            aggregate=aggregate, format="xlsx")

    def fetch_usage_logs(self, start_date: datetime, end_date: datetime, resolution: str, aggregate: bool):
        """
        Fetch usage logs in a JSON format
        :param start_date: usage logs starting from this date
        :param end_date: usage logs starting till this date
        :param resolution: group user count per day, month or year. One of 'day', 'month', 'year'
        :param aggregate: Aggregate user counts. If set to false, a row per unique user is returned.
        :return: binary text in excel-ready format
        """
        return self._fetch_usage_logs_table(start_date=start_date, end_date=end_date, resolution=resolution,
                                            aggregate=aggregate, format="json")

    def fetch_user(self, username_or_uuid: str, only_active=False) -> User:
        """
        gets user details
        :param username_or_uuid: the user's UUID or username
        :param only_active: True to filter to only active users. Default: False.
        :return: model.User from stocks package
        :raise ValueError: if response is None or if is_active parameter is True and user "is_active" field is False.
        """
        results = self.fetch_item(username_or_uuid, ModelType.USER)
        if not results:
            raise ValueError(f"No user with username or uuid {username_or_uuid}")
        if only_active and not results["is_active"]:
            raise ValueError(f"User {username_or_uuid} is not an active user")
        return StocksManager._to_user(results, username_or_uuid=username_or_uuid)

    # def fetch_user_by_username(self, username: str) -> User | None:
    #     """
    #     gets user details
    #     :param username: the user's username
    #     :return: model.User from stocks package
    #     :raises: ValueError if no user with username.
    #     """
    #
    #     qp = {'username': username, 'is_active': True}
    #     query_params = self.get_query_params(query_params=qp)
    #     user_json = handle_response(self.client.get(model_to_url.get(ModelType.USER), query_params))
    #     results = _check_result(user_json, username, 'User')
    #     if len(results) == 0:
    #         raise ValueError(f"No user with name {username}")
    #     results = results[0]
    #     logger.debug(results)
    #
    #     return StocksManager._to_user(results, username_or_uuid=username)

    def fetch_annotationtype_by_name(self, name) -> AnnotationType:
        """
        Gets annotation type object by name. Does not handle MultipleObjectMatchedError as it is not supposed to
        happen for annotationtypes
        :return: a models.AnnotationType from stocks package
        """
        res = self.fetch_item_by_name(name, ModelType.ANNOTATION)
        if not res:
            raise ValueError(f"No annotation type with name {name} was found")
        # TODO pydantic AnnotationType.
        # Works as is for now for all fields except 'created' and 'modified' which contain dictionaries formatted
        # as non-flat response format (with 'name', 'value' and 'category' fields)
        return AnnotationType(**res)

    def list_annotation_types(self) -> List[AnnotationType]:
        """
        gets the list of all supported Annotation Types
        :return: a list of model.AnnotationType from stocks package
        """
        query_params = {"fields": "name,id", "page_size": "max"}
        results = handle_response(self.client.get(model_to_url.get(ModelType.ANNOTATION), query_params))["results"]
        annotation_list = [AnnotationType(name=ann["name"], id=ann["id"]) for ann in results]

        return annotation_list

    def list_datafilecopies(self, filter_type: str = None, filter_uuid: str = None, only_primary_copy=True) \
            -> List[DatasetFileCopy]:
        """
        list datafile copies as DatasetFile
        :param filter_type: project, study, assay, dataset or datasetcollection
        :param filter_uuid: the uuid of the filter_type's object
        :param only_primary_copy: if only primary copies should be returned

        :return:
        """
        query_params = self.get_query_params()

        if filter_uuid and filter_type:
            query_params[f"{filter_type}_id"] = filter_uuid

        # the filter below is not yet avail and will be ignored by the server
        # we still have it here for when it becomes avail
        # for now, we set only_count=False in _list_items() calls and post-filter
        if only_primary_copy:
            query_params['is_primary_copy'] = True

        items = self.list_items(model=ModelType.DATAFILECOPY.value, model_type=None, query_params=query_params,
                                return_count=False)

        # need further filtering ?
        filtered_items = [x for x in items if x['is_primary_copy']] if only_primary_copy else items

        files: List[DatasetFileCopy] = []
        for record in filtered_items:
            logger.debug(record)
            py: PydanticDatasetFileCopy = PydanticDatasetFileCopy.parse_obj(record)
            dfc = DatasetFileCopy(**dict(vars(py)))
            files.append(dfc)
            dfc.dataset = py.datafile.id
        return files

    def list_datasets(self, filter_type: str = None, filter_uuid: str = None, only_count: bool = False) \
            -> List[Dataset] | int:
        """

        :param filter_type: project, study, assay, dataset or datasetcollection
        :param filter_uuid: the uuid of the filter_type's object
        :param only_count: only return item number
        :return:
        """
        query_params = self.get_query_params()

        if filter_uuid and filter_type and filter_type != "assay":
            query_params[f"{filter_type}_id"] = filter_uuid
        elif filter_uuid and filter_type == "assay":
            query_params["assay"] = filter_uuid

        items = self.list_items(model=ModelType.DATASET.value, model_type=None, query_params=query_params,
                                return_count=only_count)

        if only_count:
            return items

        datasets: List[Dataset] = []
        for record in items:
            logger.debug(record)
            py: PydanticDataset = PydanticDataset.parse_obj(record)
            ds = Dataset(**dict(vars(py)))
            datasets.append(ds)
        return datasets

    def list_dropboxes(self, for_username: str | None = None) -> Dict[str, str]:
        """
        List dropboxes that belong to the caller or another username in which case the caller must be an admin

        :param for_username: 
        :return: dict -> group name, dropbox's str(Path)
        """
        query_params = {}
        if for_username:
            query_params['username'] = for_username
        query_params = self.get_query_params(query_params)
        url = model_to_url[ModelType.DROPBOX]
        data = handle_response(self.client.get(url, query_params))
        dropboxes = {}

        for d in data:
            dropboxes[d['group']['value']['name']] = d['path']
        return dropboxes

    def list_experiment_attachments(self, experiment_id, include_embedded=False) -> List[Any]:
        return self._list_attachments(
            app="assays", model="experiment", id=experiment_id, include_embedded=include_embedded)

    def list_experiment_archives(self, experiment_id: str, most_recent_only: bool = False) \
            -> List[StocksAttachment]:
        """
        get the attachments corresponding to the zip exports
        :param most_recent_only: only the most recent one is returned
        :param experiment_id:
        :return:
        """
        atts: List[StocksAttachment] = self._list_attachments(
            app="assays", model="experiment", id=experiment_id, include_embedded=False,
            extra_filters={'is_export': True, 'mimetype': 'application/zip'})

        if most_recent_only and len(atts):
            return [atts[0]]
        return atts

    def list_experiment_nightly_backups(self, experiment_id: str, most_recent_only: bool = False) \
            -> List[StocksAttachment]:
        """
        get the attachments corresponding to the pdf nightly backups
        :param most_recent_only: only the most recent one is returned
        :param experiment_id:
        :return:
        """
        atts: List[StocksAttachment] = self._list_attachments(
            app="assays", model="experiment", id=experiment_id, include_embedded=False,
            extra_filters={'is_export': True, 'mimetype': 'application/pdf'})

        if most_recent_only and len(atts):
            return [atts[0]]
        return atts

    def list_experiments(self, owner: Optional[str] = None, group_name: Optional[str] = None,
                         project_id: Optional[str] = None, include_deleted: bool = False) -> List[Experiment]:
        """

        :param owner: filter on the owner; please provide valid username
        :param group_name: restrict to a particular group_name, pls provide a valid group_name name
        :param project_id: restrict to experiments linked to this project
        :param include_deleted:
        :return:
        """

        query_params = {"page_size": "max", "deleted": "false"}
        if include_deleted:
            query_params['deleted'] = "true"
        if owner:
            query_params['owner'] = owner
        if group_name:
            query_params['owned_by'] = group_name
        if project_id:
            query_params['project_id'] = project_id

        results = handle_response(self.client.get(model_to_url.get(ModelType.EXPERIMENT), query_params=query_params))["results"]
        exps: List[Experiment] = []
        for record in results:
            py: PydanticExperiment = PydanticExperiment.parse_obj(record)

            exps.append(Experiment(**dict(vars(py))))

        return exps

    def list_instruments(self, technology: Technology | None = None, platform: str | None = None,
                         code: str|None = None, name: str|None = None, include_deleted: bool = False
                         ) -> List[Instrument]:

        url = model_to_url[ModelType.EQUIPMENT]
        query_params = self.get_query_params()
        query_params["page_size"] = "max"
        if include_deleted:
            query_params['deleted'] = "true"
        if technology:
            query_params['technology'] = technology.value
        if platform:
            query_params['platform'] = platform
        if name:
            query_params['name'] = name
        if code:
            query_params['code'] = code

        data = handle_response(self.client.get(url, query_params))
        pgr = PaginatedResults(**data)

        instruments: List[Instrument] = []
        for record in pgr.results:
            py: PydanticInstrument = PydanticInstrument.parse_obj(record)
            fields = py.dict(by_alias=True)
            instruments.append(Instrument(**fields))

        return instruments

    def list_instrument_models(self, technology: Technology | None = None, platform: str | None = None,
                               name: str|None = None, include_deleted: bool = False
                               ) -> List[InstrumentModel]:

        url = model_to_url[ModelType.INSTRUMENTMODEL]
        query_params = self.get_query_params()
        query_params["page_size"] = "max"
        if include_deleted:
            query_params['deleted'] = "true"
        if technology:
            query_params['technology'] = technology.value
        if platform:
            query_params['platform'] = platform
        if name:
            query_params['name'] = name

        data = handle_response(self.client.get(url, query_params))
        pgr = PaginatedResults(**data)

        instrument_models: List[InstrumentModel] = []
        for record in pgr.results:
            py: PydanticInstrumentModel = PydanticInstrumentModel.parse_obj(record)
            fields = py.dict(by_alias=True)
            instrument_models.append(InstrumentModel(**fields))

        return instrument_models

    def list_instrument_runs(self, name: str | None = None, instrument_name: str | None = None,
                             owner: str | None = None, include_deleted: bool = False) -> List[InstrumentRun]:

        url = model_to_url[ModelType.INSTRUMENTRUN]
        query_params = self.get_query_params()
        query_params["page_size"] = "max"
        if include_deleted:
            query_params['deleted'] = "true"
        if instrument_name:
            query_params['instrument'] = instrument_name
        if name:
            query_params['name'] = name
        if owner:
            query_params['owner'] = owner

        data = handle_response(self.client.get(url, query_params))
        pgr = PaginatedResults(**data)

        instrument_runs: List[InstrumentModel] = []
        # a dict to buffer instruments
        instruments: dict[str, PydanticInstrument] = {}
        for record in pgr.results:
            py: PydanticSimpleInstrumentRun = PydanticSimpleInstrumentRun.parse_obj(record)
            instrument_id: str = py.instrument.id
            if instrument_id not in instruments:
                data_instr = self.fetch_item(uuid=instrument_id, model=ModelType.EQUIPMENT)
                instrument = PydanticInstrument.parse_obj(data_instr)
                # properly init the model
                data_instr_model = self.fetch_item(
                    uuid=instrument.instrumentmodel.id, model=ModelType.INSTRUMENTMODEL)
                instrument.instrumentmodel = PydanticInstrumentModel.parse_obj(data_instr_model)
                #save
                instruments[instrument_id] = instrument
            py.instrument = instruments[instrument_id]

            fields = py.dict(by_alias=True)
            # we need to add 'managed', 'technology', and 'platform'
            fields['managed'] = False
            fields['technology'] = py.instrument.instrumentmodel.technology
            fields['platform'] = py.instrument.instrumentmodel.platform
            instrument_runs.append(InstrumentRun(**fields))

        return instrument_runs

    def list_items(self, model: str, model_type: str | None = None, query_params: dict | List = None,
                   return_count: bool = False) \
            -> List[Dict[Any, Any]] | int:
        """
        low level method to list items of a model  as returned by the server, with optional query_params


        :param model: model name to list items of, e.g. consumable
        :param model_type: model type to filter model list by, e.g. chemical
        :param query_params: either a dict or a list of 'key=value' filters
        :param return_count: only return the number of results
        :return: data
        """
        query_params = self.get_query_params(query_params)
        query_params["page_size"] = "max"
        if return_count:
            query_params["page_size"] = "1"
        if model_type:
            query_params["model_type"] = model_type

        url = model_to_url[ModelType(model)]
        data = handle_response(self.client.get(url, query_params))
        logger.debug(data)
        pgr = PaginatedResults(**data)
        if return_count:
            return pgr.total
        return pgr.results

    def list_groups(self, as_dict: bool = False, keys_lower_case: bool = True) \
            -> List[UserGroup] | dict[str, UserGroup]:
        """
        gets the list of groups defined in STOCKS
        :return: a list of group_name names
        """
        query_params = {"fields": "name,id", "page_size": "max"}
        results = handle_response(self.client.get(model_to_url.get(ModelType.GROUP), query_params))["results"]
        g_list: List[UserGroup] = []
        for ann in results:
            py: PydanticStocksBaseItem = PydanticStocksBaseItem.parse_obj(ann)
            # TODO : these 2 methods seems to be gone !!
            id: str = py.get_id(py)
            name: str = py.get_name(py)
            g_list.append(UserGroup(name=name, id=id))

        logger.debug(g_list[0].as_simple_json())
        if as_dict and not keys_lower_case:
            return {x.name: x for x in g_list}
        if as_dict and keys_lower_case:
            return {x.name.lower(): x for x in g_list}

        return g_list

    def register_derived_datasets(self, collections: List[DatasetCollection], run_dir: Path, username: str,
                                  transfer_whole_input_dir: bool, study: Study | str, group: UserGroup | str = None):
        """
        Registers one or more DatasetCollections of derived Datasets. To register raw datasets, one must rather use
        register_raw_assay_datasets().
        Datasets may have link(s) to samples, or not.

        :param collections: one or more DatasetCollections of derived Datasets.
        :param run_dir: absolute path to the run directory i.e. pointing to the folder in user's dropbox
        :param username: the unix username or STOCKS' user internal ID. Will also be the
        :param transfer_whole_input_dir: whether the whole run dir is to be ingested (True) or only the described
        datasets (False). In the latter case, the relative sub-structure is still preserved
        :param study: all datasets will be linked to this study, must exist i.e. study.id must be properly initialized
        :type group: an existing STOCKS user group name or UserGroup (which the username is part of)
        or None in which case the user's primary group is used.
        """

        user: User = self.fetch_user(username)
        if not user:
            raise ValueError(f"user {username} is not found in this STOCKS server")

        primary_group_id = None
        group_id = None
        user_in_group: bool = False
        for a_group in user.groups.values():
            if a_group.is_primary_group:
                primary_group_id = a_group.id
            if group and isinstance(group, UserGroup) and a_group.id == group.id:
                group_id = a_group.id
                user_in_group = True
            elif group and isinstance(group, str) and (a_group.name.lower() == group.lower() or a_group.id == group):
                group_id = a_group.id
                user_in_group = True

        if not group_id:
            group_id = primary_group_id
        elif not user_in_group:
            raise ValueError(f"user {username} is not in group {group.name}")

        url = model_to_url[ModelType.DATASETCOLLECTION]
        url = urljoin(url, "register/")
        study_id = study
        if isinstance(study, Study):
            study_id = study.id
        post_obj: PyDatasetListPost = StocksManager._create_dataset_collection_post(
            collections, run_dir=run_dir, owner=username, owned_by_group=group_id,
            transfer_whole_input_dir=transfer_whole_input_dir, study_id=study_id)
        payload_str: str = post_obj.json(exclude_none=True, exclude_unset=True)

        logger.debug(payload_str)
        logger.debug("\n\n\n\n\n\n")
        res_json = handle_response(
            self.client.post(path=url, payload=json.loads(payload_str), query_params={'format': 'json'}))
        return res_json

    def register_raw_assay_datasets(self, instrument_run: InstrumentRun, run_dir: Path, username: str, unixgroup: str,
                                    allow_pooled_samples: bool, transfer_whole_input_dir: bool, study: Study | str
                                    ) -> Dict:
        """
        Registers an instrument run and all associated datasets, samples & datasetcollections.

        :param instrument_run: the run to register
        :param run_dir: the directory containing all the data to import. When given, the whole directory is imported in
        :param username: the owner's (unix) username
        :param unixgroup: the owner's (unix) group_name
        :param allow_pooled_samples: if True a sample can link to many datasets
        :param transfer_whole_input_dir: if true the whole dir 'run_dir' will be ingested
        :param study: an existing Study object or a UUID

        STOCKS i.e. including described datasets but also any extra information. If run_dir is None, only dataset files
        will be imported (they must hold an absolute path)
        :return:
        """
        # TODO check URL with Jelle
        # data_management/datasetcollections/register/
        url = model_to_url[ModelType.DATASETCOLLECTION]
        url = urljoin(url, "register/")
        study_id = study
        if isinstance(study, Study):
            study_id = study.id
        post_obj: PyDatasetListPost = StocksManager._create_instrument_run_post(
            instrument_run=instrument_run, run_dir=run_dir, owner=username, owned_by_group=unixgroup,
            allow_pooled_samples=allow_pooled_samples, transfer_whole_input_dir=transfer_whole_input_dir,
            study_id=study_id, old_payload=True)

        # keep unset as we need some empty but expected value in the payload
        payload_str: str = post_obj.json(exclude_none=True, exclude_unset=False)

        res_json = handle_response(
            self.client.post(path=url, payload=json.loads(payload_str), query_params={'format': 'json'}))
        return res_json

    def resolve(self, uuid: str) -> Dict | None:
        """
        Use the resolver to find minimal information about the related UUID
        :param uuid:
        :return:
            {'id': '43090720-b88e-488a-8c8e-15cca27cdb2f',
             'name': 'Batch ccreate',
             'model_type': 'ANTIBODY',
             'model_name': 'consumable',
             'app_name': 'stocks'}

            or None if the UUID was not found

        """
        data:Dict = handle_response(self.client.resolve(uuid))
        if not data['id']:
            return None
        return data

    def save_annotation(self, item_type: ModelType, uuid: str, annotation_type: AnnotationType | str,
                        content: str | StocksCVTerm) -> None:
        """
        Adds an annotation of the type annotation_type with conExperimentTypetent as value, to a STOCKS item of type item_type and id
        uuid.
        :param item_type: STOCKS item type e.g. 'sample' or 'study'
        :param uuid: STOCKS id of the item
        :param annotation_type: annotation type e.g. 'Age' or 'arrayexpress_id'
        :param content: value of the annotation to be added
        """
        path = f"{model_to_url[item_type]}{uuid}/annotations/"
        if not isinstance(annotation_type, str) and not isinstance(annotation_type, AnnotationType):
            raise TypeError('Argument annotation_type needs to be string or stocks.models.AnnotationType')
        if isinstance(annotation_type, str):
            arg = annotation_type
            annotation_type = self.fetch_annotationtype_by_name(annotation_type)
            if not annotation_type:
                raise ValueError(f"No annotation of type {arg} could be found. The {item_type} {uuid} "
                                 f"will not be updated")
        if isinstance(content, StocksCVTerm):
            content = content.name
        payload = {"annotation_type_id": annotation_type.id, "value": content}
        logger.debug(f"Posting annotation ({annotation_type.name}: {content}) at {item_type} of id '{uuid}'")
        handle_response(self.client.post(path, payload))

    def save_instrument_run(self, name: str, instrument: Instrument, description: str | None = None,
                            start_datetime: str | None = None, end_datetime: str | None = None,
                            producer: str | None = None) -> SimpleInstrumentRun:
        """
        Only saves the run i.e. ignores linked assays. Thoses must be saved separately with the save_assay()
        Expects a payload like :
        {
        "results":
            {
              "description":  "blah,
              "start_datetime": "2023-06-14 16:38:49",
              "end_datetime": "2023-06-15 16:38:49",
              "instrument": {
                  "id": "f3287861-3019-4d1a-ab51-3c185877c486"
              },
              "name": "Charles Demo",
              "producer": "Eppendorf",
              "responsible_person": {
                  "username": "admin"
              },
              "assays":[]
            }
        }
        """
        path = f"{model_to_url[ModelType.INSTRUMENTRUN]}"

        py_run: PydanticSimpleInstrumentRun = PydanticSimpleInstrumentRun(
            name=name,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            producer=producer,
            description=description,
            instrument=PydanticInstrument(
                id=instrument.id, name=instrument.name, code=instrument.serial_number),
            responsible_person=PydanticUser(username=self.client.username)
        )

        post_obj: PydanticSimpleInstrumentRunPost = PydanticSimpleInstrumentRunPost(results=py_run)
        payload_str: str = post_obj.json(exclude_none=True)

        data = handle_response( self.client.post(path, payload=json.loads(payload_str),
                             query_params={'format': 'json', "response_format": "flat"}))
        data = data['results']
        data.pop("assays")
        saved_py:PydanticSimpleInstrumentRun = PydanticSimpleInstrumentRun(**data)
        logger.debug(f"instrument of type {type(saved_py.instrument)}")
        fields = saved_py.dict(by_alias=True)
        logger.debug(f"fields: {fields}")
        return SimpleInstrumentRun(**fields)

    def save_assay(self, assay: Assay,
                   instrument_run: InstrumentRun = None) -> str:
        """
        Saves an assay but not its associated datasets i.e. datasets must be saved in a second call using register_*
        methods. If the instrument_run is not provided, either an instrumentrun or an instrumentmodel must be set on
         the assay object (if both, the run information superseeds model information).

        @param assay: the assay object
        @param instrument_run: an existing InstrumentRun (ie valid UUID) that superseeds the instrument run or
        instrument model information that may exist in the assay object
        @return: the Assay UUID
        """
        # @param username: provide this to make the assay owned by this user. Admin only. By default, the assay is owned
        # by the logged in user
        # @param group: group name or ID. Provide this to make the assay owned by this group. The group must be be one of
        # the logged in user groups.

        if not instrument_run and not assay.instrumentrun and not assay.instrumentmodel:
            raise ValueError("An instrument run or a model must be set on the assay, or a separate run should be "
                             "provided in method call")
        if instrument_run:
            logger.debug(f"setting assay.instrumentrun to {instrument_run.as_simple_json()}")
            logger.debug(f"instrumentrun.instrument is {type(instrument_run.instrument)}")
            assay.instrumentrun = instrument_run

        path = f"{model_to_url[ModelType.ASSAY]}"
        logger.debug(f"ASSAY  : {assay.as_simple_json()}")
        py_assay: PydanticAssay = self._to_pydantic_assay(assay, run=None)
        # make sure id, instrumentmodel/instrumentrun are not null as those are required POST fields
        if not py_assay.instrumentmodel:
            py_assay.instrumentmodel = ""

        if not py_assay.instrumentrun:
            py_assay.instrumentrun = ""
        else:
            # make sure we have the instrument slot also set with instrument uuid
            # which must exist when a run is given (the run may not exit)
            py_assay.instrument = py_assay.instrumentrun.instrument

        py_assay = self._prepare_object_for_post(py_assay)

        if py_assay.instrumentmodel:
            py_assay.instrumentmodel = _convertTypeFieldToPydanticNameField(py_assay.instrumentmodel)

        post_obj: PydanticSimpleAssayPost = PydanticSimpleAssayPost(results=py_assay)
        payload_str: str = post_obj.json(exclude_none=True)
        assay_type: str = assay.stocks_model_type
        data = handle_response(
            self.client.post(path, payload=json.loads(payload_str), query_params={
                'format': 'json', "response_format": "flat", "type": assay_type}
                             ))

        data = data['results']
        logger.debug(data)
        # TODO: we could return the assay object but then we need to make sure to share the code
        # with loadAssay()
        return data['id']

    def _prepare_object_for_post(self, stocks_object: PydanticStocksBaseItem,
                                alt_owner: PydanticUser | None = None,
                                alt_owned_by: PydanticUserGroup | None = None):
        """
        operate conversion to produce a valid JSON
        """

        # 'type' needs to be converted to PydanticNameField

        stocks_object = _convertTypeFieldToPydanticNameField(stocks_object)
        # choice fields need to be turned into PydanticValueField
        fields: List[str] = None
        if isinstance(stocks_object, PydanticSequencingAssay):
            fields = ['runtype', 'live_base_calling', 'adaptive_mode']

        if fields:
            stocks_object = _convertFieldsToPydanticValueField(stocks_object, fields=fields)

        # set owner
        if alt_owner:
            stocks_object.owner = alt_owner
        else:
            stocks_object.owner = PydanticUser(**dict(vars(self.logged_in_user)))

        # set owned_by
        if alt_owned_by:
            stocks_object.owned_by = alt_owned_by
        else:
            primary_group: UserGroup = self.logged_in_user.get_primary_group()
            stocks_object.owned_by = PydanticUserGroup(id=primary_group.id, name=primary_group.name)

        return stocks_object

    def init_ownership(self, ownable: OwnableMixin) -> None:
        """
        Fetch a stocks.models.User from stocks from the userame or uuid contained in the owner field of a stocks items
        :param ownable: Any stocks item which inherites from the OwnableMixin subclass.
        """
        if not isinstance(ownable, OwnableMixin):
            raise TypeError(f"Item needs to be ownable")
        owner = ownable.owner
        if isinstance(owner, str):
            owner: User = self.fetch_user(owner)
        ownable.set_owner(owner)

    def add_annotations(self, annotable: AnnotableMixin | StocksBaseItem) -> None:
        """
        Fetches from stocks annotation belonging to an annotable item and attaches them to the object.
        :param annotable: Any stocks item which inherites from the AnnotableMixin subclass.
        """
        if not isinstance(annotable, AnnotableMixin):
            raise TypeError(f"Item needs to be ownable")

        for ann in self.list_annotations_from_item(ModelType.STUDY, annotable.id):
            annotable.add_annotation(ann["name"], ann["value"])



    ##
    # PRIVATE METHODS BELOW
    #

    def _fetch_usage_logs_table(self, start_date: datetime, end_date: datetime, resolution: str,
                                aggregate: bool, format: str):
        """
        Fetch usage logs in a csv or excel format
        :param start_date: usage logs starting from this date
        :param end_date: usage logs starting untill this date
        :param resolution: group user count per day, month or year. One of 'day', 'month', 'year'
        :param aggregate: Aggregate user counts. If set to false, a row per unique user is returned.
        :param format: one of xlsx, csv or json
        :return: binary text in excel-ready format
        """
        if format not in ["xlsx", "csv", "json"]:
            raise ValueError("format must be one of: xlsx, csv or json ")

        query_params = {"format": format,
                        "start_date": f"{start_date:%Y-%m-%d}",
                        "end_date": f"{end_date:%Y-%m-%d}",
                        "resolution": resolution,
                        "aggregate": aggregate}

        query_params = self.get_query_params(query_params)

        return handle_response(self.client.get("core/usagelogs", query_params))

    def _list_attachments(self, app: str, model: str, id: str, include_embedded=False, extra_filters: dict = None) \
            -> List[StocksAttachment]:
        query_params = {"page_size": "max", "deleted": "false", "app": app, "model": model, "object_id": id}
        if not include_embedded:
            query_params['embedded'] = "false"
        if extra_filters:
            query_params.update(extra_filters)

        # order with most recent first
        query_params['ordering'] = "-created"

        results = handle_response(self.client.get(model_to_url.get(ModelType.ATTACHMENT), query_params=query_params))
        # here there is no embedding into a results slot
        atts: List[StocksAttachment] = []
        for record in results:
            atts.append(StocksAttachment.parse_obj(record))

        return atts

    ##
    # STATIC METHODS BELOW
    #

    @staticmethod
    def _create_dataset_collection_post(collections: List[DatasetCollection], run_dir: Path, owner: str, owned_by_group: str,
                                        transfer_whole_input_dir: bool, study_id: str, managed_data: bool = False,
                                        old_payload: bool = True) \
            -> PyDatasetListPost | PyOldDatasetListPost:
        """

        :param transfer_whole_input_dir:
        :param study_id:
        :param run_dir: the path to the source data directory. If given, this whole input dir_path will be imported; else only
        the dataset files will be imported
        :param owner: the valid username owning all objects of this upload
        :param owned_by_group: the valid group_name name owning all objects of this upload
        :return:
        """
        if old_payload:
            o = PyOldDatasetListPost(input_dir=str(run_dir), allow_pooled_samples = True, owned_by = owned_by_group)
        else:
            o = PyDatasetListPost(input_dir=str(run_dir), allow_pooled_samples = True, owned_by = owned_by_group)

        if run_dir is None:
            o.transfer_whole_input_dir = False
        else:
            o.transfer_whole_input_dir = transfer_whole_input_dir

        # convert the collection
        cnum = 0
        o.collections = list()
        for collection in collections:
            cnum = cnum + 1
            attrs = dict(vars(collection))
            if not collection.id:
                # we set an ID also using this dataset index to make sure every created dataset collection
                # has a unique ID.
                attrs['id'] = f"dataset_collection_{cnum}"
            attrs['owner'] = owner
            attrs['owned_by'] = owned_by_group
            attrs['is_raw'] = collection.datasets[0].is_raw  # transfer raw from dataset, a collec dont mix raw/non-raw
            pycol: PydanticDatasetCollection = PydanticDatasetCollection(**attrs)
            o.collections.append(pycol)

            #convert the datasets
            o.datasets = list()
            i = 0
            for ds in collection.datasets:
                i = i + 1
                datafile_list: List[PydanticDatasetFile] = list()
                for dsf in ds.datafiles:
                    attrs_df = dict(vars(dsf))
                    print(dsf.as_simple_json())
                    # datafile_list.append(
                    #     PydanticDatasetFile(name=dsf.name, uri=dsf.uri, type=dsf.filetype, is_folder=dsf.is_dir,
                    #                         is_managed=managed_data))
                    attrs_df['is_managed'] = managed_data
                    datafile_list.append(PydanticDatasetFile(**attrs_df))

                attrs = dict(vars(ds))

                attrs['id'] = f"dataset_{cnum}_{i}"
                # non raw dataset may have no sample nor assay
                attrs.pop('sample')

                attrs['collection'] = pycol.id  # replace object by their ID
                attrs.pop('datafiles')  # we removed this first as the prop name is different
                attrs['datafiles'] = datafile_list  # add data files
                attrs['owner'] = owner
                attrs['owned_by'] = owned_by_group
                attrs['studies'] = [study_id]
                pydataset = PydanticDataset(**attrs)
                # save
                o.datasets.append(pydataset)

        return o

    @staticmethod
    def _create_instrument_run_post(instrument_run: InstrumentRun, run_dir: Path, owner: str, owned_by_group: str,
                                    allow_pooled_samples: bool, transfer_whole_input_dir: bool, study_id: str,
                                    old_payload: bool = True) \
            -> PyDatasetListPost | PyOldDatasetListPost:
        """

        :param transfer_whole_input_dir:
        :param study_id:
        :param allow_pooled_samples:
        :param instrument_run: the instrument run to export
        :param run_dir: the path to the source data directory. If given, this whole input dir_path will be imported; else only
        the dataset files will be imported
        :param owner: the valid username owning all objects of this upload
        :param owned_by_group: the valid group_name name owning all objects of this upload
        :return:
        """
        if old_payload:
            o = PyOldDatasetListPost(input_dir=str(run_dir), allow_pooled_samples=allow_pooled_samples, owned_by=owned_by_group)
        else:
            o = PyDatasetListPost(input_dir=str(run_dir), allow_pooled_samples=allow_pooled_samples, owned_by=owned_by_group)

        if run_dir is None:
            o.transfer_whole_input_dir = False
        else:
            o.transfer_whole_input_dir = transfer_whole_input_dir

        ##
        # add run; mandatory props have matching names
        ##
        o.run = StocksManager._to_pydantic_run(instrument_run)
        o.datasets = list()
        if not o.run.id:
            o.run.id = str(uuid4())  # there is a unique run in the POST

        managed_data = instrument_run.managed

        ##
        # we loop over assays and extract all needed objects; in particular we assign them a unique id for
        # internal reference
        #
        ##
        assay_id2assay: dict[str, PydanticAssay] = dict()
        collection_name2collection: dict[str, PydanticDatasetCollection] = dict()
        sample_name2sample: dict[str, PydanticSample] = dict()

        sp_count: int = 0
        for i, assay in enumerate(instrument_run.assays):
            # ie assay must exist
            if not assay.id or not is_uuid(assay.id):
                raise ValueError(f"No valid UUID on assay {assay.as_simple_json()}.\n"
                                 f"Assays must be registered before loading datasets!")
            # make sure owned_by is set
            if not assay.owned_by:
                assay.owned_by = owned_by_group
            # pass in all assay props as a dict
            py_assay: PydanticAssay = StocksManager._to_pydantic_assay(assay, run=o.run, merge_in_run_info=old_payload)

            # set run id & ownership
            py_assay.owner = owner
            # record assay by their ID
            assay_id2assay[py_assay.id] = py_assay
            collection_name2sample_names: Dict[str, Set] = {}  # to check if sample are used only once per col
            ##
            # loop over datasets
            ##
            sample_count_in_assay: int = 0
            for j, ds in enumerate(assay.datasets):

                # get the datasetcollection for this dataset; create one if needed
                col: DatasetCollection = ds.collection
                if col and col.name not in collection_name2collection:
                    attrs = dict(vars(col))
                    if not col.id:
                        # we set an ID also using this dataset index to make sure every created dataset collection
                        # has a unique ID. The 'j' user is not so important since we identify the collection by their
                        # name
                        # attrs['id'] = f"assay_collection_{i}_{j}"
                        attrs['id'] = str(uuid4())
                    attrs['owner'] = owner
                    attrs['owned_by'] = owned_by_group
                    attrs['is_raw'] = ds.is_raw  # transfer raw from dataset, a collection do not mix raw and non raw
                    pycol: PydanticDatasetCollection = PydanticDatasetCollection(**attrs)  # id, name and description
                elif col.name in collection_name2collection:
                    pycol: PydanticDatasetCollection = collection_name2collection[col.name]
                else:
                    # get a default collection for this assay
                    pycol: PydanticDatasetCollection = PydanticDatasetCollection(
                        id=str(uuid4()),
                        name=f"Default Data Collection for Assay {assay.name}",
                        owner=owner,
                        owned_by=owned_by_group,
                        is_raw=ds.is_raw)
                #  save in dict
                collection_name2collection[pycol.name] = pycol
                if pycol.name not in collection_name2sample_names:
                    collection_name2sample_names[pycol.name] = set()
                seen_samples_for_this_collection: Set = collection_name2sample_names[pycol.name]

                # get sample for this dataset
                sps: List[Sample] = ds.samples if ds.samples else []
                pysamples: List[PydandicSample] = []
                sp_existing_ids: List[str] = []
                for sp in sps:
                    pysample: PydanticSample = None
                    if sp:
                        sample_count_in_assay = sample_count_in_assay + 1
                    # if sample has an ID, it means the sample exits in stocks
                    if sp and not sp.id:
                        # then we'll create a sample if necessary, assuming sample name is unique i.e reference to
                        # identical sample name means sample pooling (at least within a datasetcollection)
                        if not allow_pooled_samples and sp.name in seen_samples_for_this_collection:
                            mess: str = f"Multiple samples found with the same name: {sp.name} while sample pooling" \
                                        f" option is False. When loading data, sample names must be unique."
                            raise ValueError(mess)
                        elif sp.name in sample_name2sample:
                            # we just get the already created sample
                            pysample = sample_name2sample[sp.name]
                        else:
                            logger.debug(f"About to create new sample, sp count is {sp_count}")
                            sp_count = sp_count + 1
                            attrs = dict(vars(sp))
                            attrs['id'] = str(uuid4())
                            attrs['new'] = True  # this is needed to tell the server if the sample exists or not
                            attrs['owner'] = owner
                            attrs['owned_by'] = owned_by_group
                            if isinstance(sp, SequencingLibrary) and 'barcode' not in attrs or not attrs['barcode']:
                                attrs['barcode'] = "NA"
                            logger.debug(f"ATTRS ===> {attrs}")
                            pysample = PydanticSample(**attrs)
                            sample_name2sample[sp.name] = pysample
                            seen_samples_for_this_collection.add(sp.name)
                            collection_name2sample_names[pycol.name] = seen_samples_for_this_collection

                        pysamples.append(pysample)
                    elif sp and sp.id:
                        sp_existing_ids.append(sp.id)

                # create the PydanticDataset
                # note that every dataset is considered NEW
                datafile_list: List[PydanticDatasetFile] = list()
                for dsf in ds.datafiles:
                    datafile_list.append(
                        PydanticDatasetFile(name=dsf.uri, uri=dsf.uri, type=dsf.filetype, is_folder=dsf.is_dir,
                                            is_managed=managed_data))

                attrs = dict(vars(ds))
                attrs['id'] = f"dataset_{i}_{j}"  # this is unique
                all_sample_ids = []
                if pysamples:
                    all_sample_ids = [o.id for o in pysamples]  # replace object by their ID
                if sp_existing_ids:
                    all_sample_ids = all_sample_ids.append(sp_existing_ids)  # case of existing sample ie a pysample was not created

                if all_sample_ids:
                    attrs['samples'] = all_sample_ids
                elif ds.is_raw:
                    mess: str = f"Raw dataset: {sp.as_simple_json()} does not link to sample while mandatory for" \
                                f" raw data."
                    raise ValueError(mess)
                else:
                    # non raw dataset may have no sample
                    attrs.pop('samples')

                attrs['collection'] = pycol.id  # replace object by their ID
                attrs.pop('datafiles')  # we removed this first as the prop name is different
                attrs['datafiles'] = datafile_list  # add data files
                attrs['owner'] = owner
                attrs['owned_by'] = owned_by_group
                attrs['studies'] = [study_id]
                attrs['assay'] = py_assay.id
                pydataset = PydanticDataset(**attrs)
                # save
                o.datasets.append(pydataset)

            if isinstance(py_assay, PydanticSequencingAssayRunInfo):
                py_assay.nr_of_samples = sample_count_in_assay

        # set remaining PyDatasetListPost slots
        o.assays = list(assay_id2assay.values())
        o.collections = list(collection_name2collection.values())
        o.samples = list(sample_name2sample.values())

        # done
        return o

    @staticmethod
    def get_query_params(query_params: List[str] | Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        get the default set of query params. The optional query_params is copied into the default dict, potentially
        overwriting defaults
        :param query_params: a list of key=value strings
        :return:
        """
        _query_params: Dict[str, Any] = {"response_format": "flat", "deleted": "False"}
        if not query_params:  # This avoids logger error message everytime query params are instancied here.
            return _query_params

        if query_params and isinstance(query_params, list) or isinstance(query_params, tuple):
            for param in query_params:
                k, v = param.split("=") if '=' in param else param.split(":")
                _query_params[k] = v
        elif query_params and isinstance(query_params, dict):
            _query_params.update(query_params)
        else:
            logger.error(f"Do not know how to handle query_params of type {type(query_params)}: {query_params}."
                         f" Those will be ignored in query")
        return _query_params

    @staticmethod
    def _to_user(results: dict, username_or_uuid: str) -> User:
        logger.debug(type(results))

        # parse results in pydantic object
        pydantic_user = PydanticUser.parse_obj(results)
        logger.debug(pydantic_user)

        # identify the primary group
        if 'primary_group' in results and 'value' in results['primary_group'] and 'name' in results['primary_group'][
            'value']:
            primary_group = results.get('primary_group').get('value').get('name')
        elif 'primary_group' in results and 'name' in results['primary_group']:
            primary_group = results.get('primary_group').get('name')
        else:
            raise ValueError(f"No primary group was found for user: {username_or_uuid}")
        logger.debug((f"primary group is {primary_group}"))


        # convert
        d: dict = dict(pydantic_user.dict())
        d.pop("groups") # we dont pass groups as it will fail the init()
        u: User = User(**d)
        # build the UserGroup objets
        for g in pydantic_user.groups:
            _g: UserGroup = UserGroup(**g.dict())
            if primary_group and g.name == primary_group:
                _g.is_primary_group = True
            u.add_user_group(_g)

        # TODO Name logic to be improved

        names = pydantic_user.full_name.strip().split(" ")
        u.first_name =  names[0]
        u.last_name = names[-1]
        logger.debug(u.as_simple_json())
        return u

    @staticmethod
    def _to_pydantic_assay(assay: Assay, run: PydanticInstrumentRun | None, merge_in_run_info: bool = False) \
            -> PydanticAssay | PydanticSequencingAssayRunInfo:
        """

        @param assay: the assay
        @param run: the object holding the run information, MUST be given if merge_in_run_info
        @param merge_in_run_info: if true the run information (instrument, technology, platform and is_managed)
         are added as properties of the assay
        @return:
        """
        if merge_in_run_info and not run:
            raise ValueError("run must be given when merge_in_run_info is true")
        # pass in all assay props as a dict
        attrs = dict(vars(assay))
        logger.debug(attrs)
        #print(f" attrs: {attrs}")
        if merge_in_run_info:
            attrs['instrumentrun'] = run.id
        elif run:
            attrs['instrumentrun'] = run
        elif assay.instrumentrun:
            attrs['instrumentrun'] = StocksManager._to_pydantic_simple_run(assay.instrumentrun)

        if assay.stocks_model_type == "NANOPOREASSAY" or assay.stocks_model_type == "NGSILLUMINAASSAY":
            if merge_in_run_info:
                attrs['instrument'] = run.instrument
                attrs['technology'] = run.technology
                attrs['platform'] = run.platform
                attrs['is_managed'] = run.managed

                py_assay = PydanticSequencingAssayRunInfo(**attrs)
            else:
                py_assay = PydanticSequencingAssay(**attrs)
        else:
            py_assay = PydanticAssay(**attrs)

        return py_assay

    @staticmethod
    def _to_pydantic_run(run: InstrumentRun) -> PydanticInstrumentRun:
        return PydanticInstrumentRun(**dict(vars(run)))

    @staticmethod
    def _to_pydantic_simple_run(run: InstrumentRun) -> PydanticSimpleInstrumentRun:
        return PydanticSimpleInstrumentRun(**dict(vars(run)))

