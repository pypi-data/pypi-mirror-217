## Clients of Searchium cloud platform
#### FVS - is fast vector search
##### get more info https://www.searchium.ai/

---
###### supported methods

- validate_allocation(self) -> bool
- get_loaded_dataset(self) -> List[LoadedDataset]:
- get_datasets -> List[Dataset]
- delete_dataset(dataset_id: str) -> bool
- load_dataset(self, dataset_id: str) -> bool
- unload_dataset(self, dataset_id: str) -> bool
- search(self, dataset_id: str, query: List[List[float]], topk: int = 5) -> SearchResponse
- create_dataset(dataset_id: Optional[str] = None) -> CreateDatasetResponse
- add_chunk(dataset_id: str, list_documents: List[dict]) -> Response
- train_dataset(dataset_id: str) -> Response
- train_status(dataset_id: str) -> TrainStatus
- get_dataset(dataset_id: str) -> Dataset
- delete_document(dataset_id: str, document_id: List[str] = None, delete_all: bool = False) -> ResponseDeleteDocument
---

***example:***

***import searchium***

***searchium.init("your_allocation_id", "your_url")***

***dataset_id = 'your_dataset_uuid'***

***searchium.create_dataset(dataset_id)***

***searchium.add_chunk(dataset_id: str, [{"document_id": str=doc_id, "vector": List[float]=embedding, "metadata": dict=metadata}])***

***searchium.train_dataset(dataset_id)***

***searchium.load_dataset(dataset_id)***

***searchium.search(dataset_id: str, query: List[List[float]], topk: int = 5)***

***searchium.unload_dataset(dataset_id)***

