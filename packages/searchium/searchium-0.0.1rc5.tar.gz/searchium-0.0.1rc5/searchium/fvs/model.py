from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class LoadedDataset(BaseModel):
    datasetId: str = None
    datasetNumOfRecords: int = None
    _hammingK: str = None
    _maxNQueries: str = None
    _neuralMatrixId: str = None
    _normalize: bool = None
    _rerankTopK: int = None
    searchType: str = None
    _typicalNQueries: int = None
    _inMemNumOfRecords: int
    _isLoaded: bool
    _pendingTransactionsInd: bool
    _removedIndexes: List
    _shiftMap: str


class EncodingDetails(BaseModel):
    binDatasetSizeInBytes: str = None
    binFilePath: str = None
    isActive: str = None
    nbits: str = None
    id: str = None


class CreateDatasetResponse(BaseModel):
    datasetId: str = None


class Document(BaseModel):
    document_id: str = None
    vector: List[float] = None
    metadata: Optional[List[dict]] = None


class DatasetStatus(str, Enum):
    COMPLETED = 'completed'
    TRAINING = 'training'
    ERROR = 'error'
    LOADED = 'loaded'
    PENDING = 'pending'
    ADDING = 'adding'
    NOT_LOADED = 'not_loaded'


class TrainStatus(BaseModel):
    datasetStatus: DatasetStatus


class Response(BaseModel):
    status: str = None


class ResponseDeleteDocument(BaseModel):
    removeDataIndexes: List = None


class AddChunkRequest(BaseModel):
    documents: List[Document]


class Dataset(BaseModel):
    _datasetCopyFilePath: str = None
    _datasetFileType: str = None
    datasetName: str = None
    datasetStatus: str = None
    datasetType: str = None
    id: str = None
    numOfRecords: int = None
    numOfFeatures: int = None
    _encodingDetails: List[EncodingDetails] = None


class SearchResponse(BaseModel):
    distance: List[List[float]] = None
    indices: List[List[int]] = None
    metadata: Optional[List[Optional[List[Optional[dict]]]]] = None
    search: float
    total: float


class LoadedDatasets(LoadedDataset):
    __loaded_datasets: List[LoadedDataset] = None

    def get_loaded_datasets_list(self):
        return self.__loaded_datasets
