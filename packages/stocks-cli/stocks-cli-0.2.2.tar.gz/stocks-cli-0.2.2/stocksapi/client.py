# -*- coding: utf-8 -*-
"""
Helper class to interact with a given STOCKS instance
"""
import json
import logging
from typing import Dict, Tuple, Optional, Iterator
from urllib.parse import urljoin
import jwt
import requests
from jwt import DecodeError
from stocksapi.exceptions import AuthenticationError
from cli.utils import ModelType

logger = logging.getLogger(__name__)

# Keeping this just in case
# model_to_url = {
#     "annotation": "annotationtypes/",
#     "annotations": "annotationtypes/",
#     "assay": "assays/assays/",
#     "assays": "assays/assays/",
#     "archive": "data_management/archives",
#     "archives": "data_management/archives",
#     "attachment": "attachments",
#     "attachments": "attachments",
#     "consumable": "stocks/consumables/",
#     "consumables": "stocks/consumables/",
#     "equipment": "stocks/equipment/",
#     "dataset": "data_management/datasets/",
#     "datasets": "data_management/datasets/",
#     "datafile": "data_management/datafiles/",
#     "datafiles": "data_management/datafiles/",
#     "datafilecopy": "data_management/datafilecopies/",
#     "datafilecopies": "data_management/datafilecopies/",
#     "datasetcollection": "data_management/datasetcollections/",
#     "datasetcollections": "data_management/datasetcollections/",
#     "dropbox": "data_management/dropbox/",
#     "dropboxes": "data_management/dropbox/",
#     "experiment": "assays/experiments/",
#     "experiments": "assays/experiments/",
#     "group_name": "groups/",
#     "group": "groups/",
#     "groups": "groups/",
#     "project": "core/projects/",
#     "projects": "core/projects/",
#     "protocol": "protocols/protocols/",
#     "protocols": "protocols/protocols/",
#     "storagevolume": "data_management/storagevolume/",
#     "storagevolumes": "data_management/storagevolumes/",
#     "sample": "stocks/samples/",
#     "samples": "stocks/samples/",
#     "specimen": "stocks/specimen/",
#     "storageequipment": "stocks/storageequipment/",
#     "study": "core/studies/",
#     "studies": "core/studies/",
#     "term": "vocabularies/terms/",
#     "terms": "vocabularies/terms/",
#     "user": "users/",
#     "users": "users/",
#     "workflow": "protocols/workflows/",
#     "workflows": "protocols/workflows/"
# }

# TODO: resolve this map from an endpoint
model_to_url = {
    ModelType.ANNOTATION: "annotationtypes/",
    ModelType.ASSAY: "assays/assays/",
    ModelType.ARCHIVE: "data_management/archives",
    ModelType.ATTACHMENT: "attachments",
    ModelType.CONSUMABLE: "stocks/consumables/",
    ModelType.EQUIPMENT: "stocks/equipment/",
    ModelType.DATASET: "data_management/datasets/",
    ModelType.DATAFILE: "data_management/datafiles/",
    ModelType.DATAFILECOPY: "data_management/datafilecopies/",
    ModelType.DATASETCOLLECTION: "data_management/datasetcollections/",
    ModelType.DROPBOX: "data_management/dropbox/",
    ModelType.EXPERIMENT: "assays/experiments/",
    ModelType.GROUP: "groups/",
    ModelType.INSTRUMENTMODEL: "stocks/instrumentmodels/",
    ModelType.INSTRUMENTRUN: "assays/instrumentruns/",
    ModelType.PROJECT: "core/projects/",
    ModelType.PROTOCOL: "protocols/protocols/",
    ModelType.STORAGE_VOLUME: "data_management/storagevolume/",
    ModelType.SAMPLE: "stocks/samples/",
    ModelType.SPECIMEN: "stocks/specimen/",
    ModelType.STORAGE_EQUIPMENT: "stocks/storageequipment/",
    ModelType.STUDY: "core/studies/",
    ModelType.TERM: "vocabularies/terms/",
    ModelType.USER: "users/",
    ModelType.WORKFLOW: "protocols/workflows/",
}


def handle_response(response) -> Tuple:
    try:
        return response.status_code, response.json()
    except json.JSONDecodeError:
        logger.debug("Could not serialize server response.")
        logger.debug(response.__dict__)
        return response.status_code, response.content


class StocksClient:
    def __init__(self, config_content: Optional[dict],
                 url: Optional[str] = None,
                 username: Optional[str] = None,
                 token: Optional[str] = None,
                 with_authentication: bool = True):
        """
        :param config_content: dictionary containing all relevant connection details as read from the config file
        :param url: stocks API URL to use, overwrites config_content's url if applicable
        :param username: stocks' api username to use, overwrites config_content's url if applicable
        :param token: stocks' api token to use, overwrites config_content's url if applicable
        :param with_authentication: if set to False, this client does requests anonymously
        """
        if config_content:
            default_url = config_content["default"]
            self.url = urljoin(default_url, "api/v2/")
            self.token = config_content[default_url].get("token", None)
            self.username = config_content[default_url].get("username", username)

        if url:
            self.url = urljoin(url, "api/v2/")
        if username:
            self.username = username
        if token:
            self.token = token

        self.with_authentication = with_authentication

    def connect(self):
        try:
            return self.get("version/")
        except requests.exceptions.ConnectionError as e:
            return None, str(e)

    def _get_headers(self, **kwargs):
        if self.with_authentication:
            if not self.token:
                raise AuthenticationError("No Token set.")
            try:
                decoded = jwt.decode(self.token, verify=False)
                return {"Authorization": f"Bearer {self.token}"}
            except DecodeError:
                # assume api token
                return {"Authorization": f"Token {self.token}"}
        return {}

    # def handle_response(self, response):
    #     try:
    #         return response.status_code, response.json()
    #     except json.JSONDecodeError:
    #         logger.debug("Could not serialize server response.")
    #         logger.debug(response.__dict__)
    #         return response.status_code, response.content

    def authenticate(self, password):
        # $ curl -X POST -d "username=dummy&password=123456" http://stocks.embl.de/api/token-auth/
        response = requests.post(urljoin(self.url, "token-auth/"),
                                 json={"username": self.username, "password": password}
                                 )
        logger.debug(response)
        if response.ok:
            self.token = response.json()["token"]
            self.with_authentication = True
        elif response.status_code == 401:
            raise AuthenticationError(f"Username and password combination not accepted: {response.content}",
                                      status_code=response.status_code)

    def get(self, path, query_params=None):
        url = urljoin(self.url, path)
        logger.debug("Fetching url: %s", url)
        logger.debug("With query params: %s", query_params)
        response = requests.get(url, headers=self._get_headers(), params=query_params)
        logger.debug(f"Got response from {response.url}")
        return handle_response(response)

    def put(self, path, payload, query_params=None):
        url = urljoin(self.url, path)
        logger.debug("PUT to url: %s", url)
        logger.debug("With query params: %s", query_params)
        logger.debug("Payload: %s", payload)
        response = requests.put(url,
                                json=payload,
                                headers=self._get_headers(),
                                params=query_params)
        return handle_response(response)

    def post(self, path, payload=None, file=None, query_params=None):
        url = urljoin(self.url, path)
        logger.debug("POST to url: %s", url)
        logger.debug("With query params: %s", query_params)
        logger.debug("Payload: %s", payload)
        logger.debug("File: %s", file)
        response = requests.post(url,
                                 json=payload,
                                 files=file,
                                 headers=self._get_headers(),
                                 params=query_params)
        return handle_response(response)

    def delete(self, path, query_params=None):
        url = urljoin(self.url, path)
        logger.debug("DELETE to url: %s", url)
        logger.debug("With query params: %s", query_params)
        response = requests.delete(url,
                                   headers=self._get_headers(),
                                   params=query_params)
        return handle_response(response)

    def list(self, model, model_type="DEFAULT", query_params=None):
        """
        :type model: str
        :param model: model name to list items of, e.g. consumable
        :type model: str
        :param model_type: model type to filter model list by, e.g. chemical
        :type query_params: dict
        :param query_params: additional query params
        :rtype: dict, int
        :return: response data, status code
        """
        url = model_to_url[model]
        if not query_params:
            query_params = {}
        if model_type:
            query_params["model_type"] = model_type
        return self.get(url, query_params=query_params)

    def list_all(self, *args, **kwargs):  # type: (...) -> Iterator[dict]
        """
        Paginator enabled list(), only returns the result objects and returns an iterator
        """
        status, response = self.list(*args, **kwargs)
        for ret_obj in response["results"]:
            yield ret_obj
        while response["next"]:
            status, response = self.get(response["next"])
            for ret_obj in response["results"]:
                yield ret_obj

    def resolve(self, uuid, query_params=None):
        """
        Use the resolver to find minimal information about the related UUID
        :param uuid:
        :param query_params:
        :return:
        """
        return self.get(f"resolver/{uuid}", query_params=query_params)

    def search(self, query: str, query_params: Dict = None):
        """
        Use the resolver to search through the instance
        """
        return self.get(f"resolver/?query={query}", query_params=query_params)

    def fetch(self, uuid: str, model: str, query_params: Dict = None):
        """
        Fetch a single item
        :param uuid: object id to retrieve
        :param model: plural model name to list items of, e.g. consumables
        :param query_params: additional query params
        :return: response data, status code
        """
        url = urljoin(model_to_url[model], uuid)
        logger.debug(url)
        if not query_params:
            query_params = {}
        return self.get(url, query_params=query_params)
