import json

import requests
from pydantic.tools import parse_obj_as

from searchium.client.init import Config
from searchium.fvs.model import *


def validate_allocation() -> bool:
    """
    Validate user allocation on cloud platform
    :return: bool
    """
    link = f"{Config.link}/board/allocation/validate"
    body = {"allocationId": f"{Config.allocation_id}"}
    get = requests.post(link, json=body)
    if get.status_code == 200:
        return True
    else:
        return False


def get_loaded_dataset() -> List[LoadedDataset]:
    """
    Get list loaded datasets
    :return: List[LoadedDataset]
    """
    link = f"{Config.link}/board/allocation/list"
    get = requests.get(link, headers=Config.headers)
    if get.status_code == 200:
        loaded = get.json()['allocationsList'][f'{Config.allocation_id}']['loadedDatasets']
        obj_as = parse_obj_as(List[LoadedDataset], loaded)
        return obj_as
    else:
        raise Exception(get.json())


def get_datasets() -> List[Dataset]:
    """
    Get list imported datasets
    :return: List[Dataset]
    """
    link = f"{Config.link}/dataset/list"
    get = requests.get(link, headers=Config.headers)
    if get.status_code == 200:
        list_datasets = get.json()['datasetsList']
        obj_as = parse_obj_as(List[Dataset], list_datasets)
        return obj_as
    else:
        raise Exception(get.json())


def get_dataset(dataset_id: str) -> Dataset:
    datasets: List[Dataset] = get_datasets()
    for data in datasets:
        if data.id == dataset_id:
            return data
    raise Exception(f"dataset by id: {dataset_id} is not found")


def delete_dataset(dataset_id: str) -> bool:
    """
    Delete dataset by dataset id
    :param dataset_id:
    :return: bool
    """
    link = f"{Config.link}/dataset/remove/{dataset_id}"
    get = requests.delete(link, headers=Config.headers)
    if get.status_code == 200:
        return True
    else:
        raise Exception(get.json())


def load_dataset(dataset_id: str) -> bool:
    """
    load dataset by dataset id
    :param dataset_id: str
    :return: bool
    """
    link = f"{Config.link}/dataset/load"
    body = {"allocationId": f"{Config.allocation_id}", "datasetId": f"{dataset_id}", "normalize": True,
            "typicalNQueries": 1, "maxNQueries": 50, "hammingK": 3200}
    get = requests.post(link, json=body, headers=Config.headers)
    if get.status_code == 200:
        return True
    else:
        raise Exception(get.json())


def unload_dataset(dataset_id: str) -> bool:
    """
    unload dataset by dataset id
    :param dataset_id: str
    :return: bool
    """
    link = f"{Config.link}/dataset/unload"
    body = {"allocationId": f"{Config.allocation_id}", "datasetId": f"{dataset_id}"}
    get = requests.post(link, json=body, headers=Config.headers)
    if get.status_code == 200:
        return True
    else:
        raise Exception(get.json())


def search(dataset_id: str, query: List[List[float]], topk: int = 5) -> SearchResponse:
    """
    search query in dataset
    return result object SearchResponse
    where fields are:
    distance - distance
    indices - indices
    metadata - optional
    search - netto apu search time
    total - full search time FVS
    :return: search result
    """
    link = f"{Config.link}/dataset/search"
    body = {"allocationId": f"{Config.allocation_id}", "datasetId": f"{dataset_id}", "topk": topk,
            "queriesFilePath": query}
    get = requests.post(link, json=body, headers=Config.headers)
    if get.status_code == 200:
        obj_as = parse_obj_as(SearchResponse, get.json())
        #return obj_as.dict(exclude_none=True)
        return obj_as
    else:
        raise Exception(get.json())


def create_dataset(dataset_id: Optional[str] = None) -> CreateDatasetResponse:
    """
    :return: str dataset_id
    """
    link = f"{Config.link}/dataset/create"
    body = {"datasetId": dataset_id}
    get = requests.post(link, json=body, headers=Config.headers)
    if get.status_code == 200:
        obj_as = parse_obj_as(CreateDatasetResponse, get.json())
        return obj_as
    else:
        raise Exception(get.json())


def train_dataset(dataset_id: str) -> Response:
    link = f"{Config.link}/dataset/train"
    body = {"datasetId": dataset_id}
    get = requests.post(link, json=body, headers=Config.headers)
    if get.status_code == 200:
        obj_as = parse_obj_as(Response, get.json())
        return obj_as
    else:
        raise Exception(get.json())


def get_dataset_status(dataset_id: str) -> TrainStatus:
    link = f"{Config.link}/dataset/status/{dataset_id}"
    get = requests.get(link, headers=Config.headers)
    if get.status_code == 200:
        obj_as = parse_obj_as(TrainStatus, get.json())
        return obj_as
    else:
        raise Exception(get.json())


def add_chunk(dataset_id: str, list_documents: List[dict]) -> Response:
    """
    :param dataset_id: str
    :param list_documents: List[dict] where dict contains
    {"document_id": str, vector: List[float], metadata: dict}
    :return: status ok
    """
    link = f"{Config.link}/dataset/add/chunk"
    records = [doc["vector"] for doc in list_documents]
    metadata = [doc["metadata"] if "metadata" in doc and (doc["metadata"] is not None) else None for doc in list_documents]
    document_ids = [doc["document_id"] for doc in list_documents]
    body = {"datasetId": dataset_id, "records": records, "metadata": metadata, "docsIds": document_ids}
    get = requests.post(link, json=body, headers=Config.headers)
    if get.status_code == 200:
        response = get.json()
        if "error" in response:
            raise Exception(response)
        return parse_obj_as(Response, response)
    else:
        raise Exception(get.json())
    pass


def delete_document(dataset_id: str, document_id: List[str] = None, delete_all: bool = False) -> ResponseDeleteDocument:
    link = f"{Config.link}/dataset/remove/documents"
    body = {"datasetId": dataset_id, "docsIds": document_id, "deleteAll": delete_all}
    get = requests.post(link, json=body, headers=Config.headers)
    if get.status_code == 200:
        print(f" response: {get.json()}")
        obj_as = parse_obj_as(ResponseDeleteDocument, get.json())
        return obj_as
    else:
        raise Exception(get.json())


def _check_connection() -> bool:
    # Alive
    # /alive
    pass
