# -*- coding: utf-8 -*-
"""
The 'fetch' module of the CLI
"""
import json
from pathlib import Path
from typing import List, Optional

import typer
import logging

from cli import get_default_config_file_path
from cli.config import get_config
from stocksapi.client import StocksClient
from stocksapi.manager import StocksManager
from cli.utils import ModelType

logger = logging.getLogger(__name__)

# name of this module (as appearing on the command line) is the last part of the __name__ eg cli.config -> config
_MODULE_NAME = __name__.rsplit(".", 1)[-1]
# list of command names offered in this module
_CMD_FETCH_ITEM = "item"
_CMD_LIST_ITEMS = "items"
_CMD_LIST_DATASETS = "datasets"
_CMD_LIST_DATAFILECOPIES = "datafiles"

# create the CLI app
app = typer.Typer()

_QUERY_PARAM_OPTION_HELP= "Filter request by these query parameters e.g. --query_param 'name=blah'. " \
                          "Filters are 'AND' combined when multiple filters are provided. Please see API " \
                          "documentation to learn available filters. Simple object properties are usually available " \
                          "as filters."
_ONLY_COUNT_OPTION_HELP="if --count only returns the number of fetched items; else return items in the JSON format"

@app.command(_CMD_FETCH_ITEM, help="Fetch a JSON representation of an item using its UUID")
def fetch_item_by_id(
        uuid: str = typer.Option(
            ...,
            "--id",
            "-i",
            help="The UUID of the object to fetch"
        ),
        query_params: List[str] = typer.Option(
            None,
            "--query_param", "-q",
            help=_QUERY_PARAM_OPTION_HELP
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path"
        )
):
    # Initiate client and manager.
    client: StocksClient = StocksClient(get_config(Path(conf_file_path)))
    stocks_manager: StocksManager = StocksManager(client)

    data = stocks_manager.resolve(uuid=uuid)
    data = stocks_manager.fetch_item(uuid, model=ModelType(data["model_name"]), query_params=query_params)
    print(data)


@app.command(_CMD_LIST_ITEMS, help="""
    Fetch multiple items based on the given parameters. The response is paginated and further
    pages can be retrieved with a query parameter e.g. '--query_param page:1'. Also
    page size can be tweaked with e.g. '--query_param page_size:20'. As data can change on the
    server, pagination can return unreliable results. To overcome this, please use the underlying
    `stocks_client` library instead.
    """
             )
def list_items(
        model: str = typer.Option(
            ...,
            "--model", "-m",
            help=f"model of the items to retrieve e.g. one of {ModelType.list()}"
        ),
        model_type: str = typer.Option(
            None,
            "--type", "-t",
            help="The model's sub-type to fetch. Only for models with sub-types (e.g. consumable, equipment) "
                 "e.g. 'chemical', 'enzyme' for consumable..."
        ),
        filter_type: str = typer.Option(
            None,
            "--filter-type", "-f",
            help="Type of the filter object when filtering results by a linked object e.g. filtering datasets that"
                 " belong to an 'assay'. Works together with the --filter-id "
        ),
        filter_uuid: str = typer.Option(
            None,
            "--filter-id", "-i",
            help="Filter result list by only keeping results related to this object id. "
                 "Works together with the --filter-type"
        ),
        query_params: List[str] = typer.Option(
            None,
            "--query_param", "-q",
            help=_QUERY_PARAM_OPTION_HELP
        ),
        only_count: bool = typer.Option(
            False,
            "--count / --details",
            help=_ONLY_COUNT_OPTION_HELP
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path"
        )
):
    # Initiate client and manager.
    client: StocksClient = StocksClient(get_config(Path(conf_file_path)))
    stocks_manager: StocksManager = StocksManager(client)
    data = _list_items(stocks_manager=stocks_manager, model=model, only_count=only_count, model_type=model_type,
                       filter_uuid=filter_uuid, filter_type=filter_type, query_params=query_params)
    if only_count:
        print(data)
    else:
        print(json.dumps(data))


def _list_items(stocks_manager: StocksManager, model: str, only_count: bool, model_type: Optional[str] = None,
                filter_uuid: Optional[str] = None, filter_type: Optional[str] = None,
                query_params: Optional[List[str]] = None) -> str | List | int:

    if filter_uuid:
        logger.debug(f"Resolving object for filter_uuid {filter_uuid}")
        data = stocks_manager.resolve(uuid=filter_uuid)
        resolved_type: str = data['model_name']
        if filter_type and resolved_type.lower() != filter_type.lower():
            raise typer.BadParameter(f"The provided filtering ID {filter_uuid} does not point to a {filter_type} but to"
                                     f" a {resolved_type}")
        if not query_params:
            query_params = list()
        # format ie key:val must match the expected input format
        query_params.append(f"{data['model_name']}_id={filter_uuid}")
        logger.warning("Filter by UUID: %s (%s)", filter_uuid, data["model_name"])

    return stocks_manager.list_items(model=model, model_type=model_type, query_params=query_params,
                                     return_count=only_count)

@app.command(_CMD_LIST_DATASETS, help="List datasets that belong to a project, a study, an assay or a collection")
def list_datasets(
        study: str = typer.Option(
            None,
            "--study",
            "-s",
            help="Get datasets of the specified study id"
        ),
        project: str = typer.Option(
            None,
            "--project",
            "-p",
            help="Get datasets of the specified project id"
        ),
        assay: str = typer.Option(
            None,
            "--assay",
            "-a",
            help="Get datasets of the specified assay id"
        ),
        collection: str = typer.Option(
            None,
            "--collection",
            "-c",
            help="Get datasets of the specified collection id"
        ),
        query_params: List[str] = typer.Option(
            None,
            "--query_param", "-q",
            help=_QUERY_PARAM_OPTION_HELP
        ),
        only_count: bool = typer.Option(
            False,
            "--count / --details",
            help=_ONLY_COUNT_OPTION_HELP
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path"
        )
):
    # use singular form in filter_type
    if study:
        return list_items(model=ModelType.DATASET.value, model_type=None,
                          filter_type="study", filter_uuid=study,
                          query_params=query_params, only_count=only_count, conf_file_path=conf_file_path)
    elif project:
        return list_items(model=ModelType.DATASET.value, model_type=None,
                          filter_type="project", filter_uuid=project,
                          query_params=query_params, only_count=only_count, conf_file_path=conf_file_path)
    elif collection:
        return list_items(model=ModelType.DATASET.value, model_type=None,
                          filter_type="datasetcollection", filter_uuid=collection,
                          query_params=query_params, only_count=only_count, conf_file_path=conf_file_path)
    elif assay:
        # assay should be handled differently ie we need assay=id and not assay_id=id as the list_items()
        # but this will be fixed so this workaround is temporary
        # TODO: remove workaround when server is fixed
        if not query_params:
            query_params = list()
        else:
            query_params = list(query_params)
        query_params.append(f"assay={assay}")
        return list_items(model=ModelType.DATASET.value, model_type=None,
                          filter_type=None, filter_uuid=None,
                          query_params=query_params, only_count=only_count, conf_file_path=conf_file_path)
    else:
        raise typer.BadParameter(f"one of --project, --study, --assay or --collection must be provided")


@app.command(_CMD_LIST_DATAFILECOPIES, help="List data files that belong to a project, a study, an assay, a "
                                            "collection or a dataset")
def list_datafile_copies(
        project: str = typer.Option(
            None,
            "--project",
            "-p",
            help="Get datafiles of the specified project id"
        ),
        study: str = typer.Option(
            None,
            "--study",
            "-s",
            help="Get datafiles of the specified study id"
        ),
        assay: str = typer.Option(
            None,
            "--assay",
            "-a",
            help="Get datafiles of the specified assay id"
        ),
        collection: str = typer.Option(
            None,
            "--collection",
            "-c",
            help="Get datasets of the specified collection id"
        ),
        dataset: str = typer.Option(
            None,
            "--dataset",
            "-d",
            help="Get datafiles of the specified dataset id"
        ),
        primary: bool = typer.Option(
            True,
            "--primary / --all",
            help="Only fetches the primary copy of datafiles; else return all copies"
        ),
        only_count: bool = typer.Option(
            False,
            "--count / --details",
            help=_ONLY_COUNT_OPTION_HELP
        ),
        query_params: List[str] = typer.Option(
            None,
            "--query_param", "-q",
            help=_QUERY_PARAM_OPTION_HELP
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path"
        )
):
    client: StocksClient = StocksClient(get_config(Path(conf_file_path)))
    stocks_manager: StocksManager = StocksManager(client)

    # the filter below is not yet avail and will be ignored by the server
    # we still have it here for when it becomes avail
    # for now, we set only_count=False in _list_items() calls and post-filter
    if primary:
        if not query_params:
            query_params = list()
        else:
            query_params = list(query_params)
        query_params.append(f"is_primary_copy=True")

    # use singular form in filter_type, we have only_count set to False to be able to post filter
    if study:
        items = _list_items(stocks_manager=stocks_manager, model=ModelType.DATAFILECOPY.value, only_count=False,
                            model_type=None, filter_type="study", filter_uuid=study, query_params=query_params)
    elif project:
        items = _list_items(stocks_manager=stocks_manager, model=ModelType.DATAFILECOPY.value, only_count=False,
                            model_type=None, filter_type="project", filter_uuid=project, query_params=query_params)
    elif assay:
        items = _list_items(stocks_manager=stocks_manager, model=ModelType.DATAFILECOPY.value, only_count=False,
                            model_type=None, filter_type="assay", filter_uuid=assay, query_params=query_params)
    elif dataset:
        items = _list_items(stocks_manager=stocks_manager, model=ModelType.DATAFILECOPY.value, only_count=False, model_type=None,
                            filter_type="dataset", filter_uuid=dataset,
                            query_params=query_params)
    elif collection:
        items = _list_items(stocks_manager=stocks_manager, model=ModelType.DATAFILECOPY.value, only_count=False, model_type=None,
                            #filter_type="datasetcollection", filter_uuid=collection,
                            query_params=query_params)
    else:
        raise typer.BadParameter(f"one of --project, --study, --assay, --collection or --dataset must be provided")

    # need further filtering ?
    if primary:
        logger.debug(f"Got {len(items)} data files before optional filtering")

    filtered_items = [x for x in items if x['is_primary_copy']] if primary else items

    if only_count:
        print(len(filtered_items)) # this is not good as the count must be re-computed ie
    else:
        logger.debug(f"Fetched {len(filtered_items)} data files")
        print(json.dumps(filtered_items))