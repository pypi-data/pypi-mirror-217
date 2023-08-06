from typing import Any, Dict, Generator, List, Optional, Union

import itertools
import json
from dataclasses import dataclass
from multiprocessing.pool import ThreadPool

import requests
from embedbase_client.base import BaseClient
from embedbase_client.errors import EmbedbaseAPIException
from embedbase_client.model import (
    AddDocument,
    ClientDatasets,
    Document,
    GenerateOptions,
    Metadata,
    SearchSimilarity,
)
from embedbase_client.split import merge_and_return_tokens, split_text
from embedbase_client.utils import sync_stream


class SyncSearchBuilder:
    def __init__(
        self,
        client: BaseClient,
        dataset: str,
        query: str,
        options: Optional[Dict[str, Any]] = None,
    ):
        if options is None:
            options = {}
        self.client = client
        self.dataset = dataset
        self.query = query
        self.options = options

    def get(self) -> List[SearchSimilarity]:
        return self.search()

    def search(self) -> "SyncSearchBuilder":
        """
        Search for documents similar to the given query in the specified dataset.

        Args:
            dataset: The name of the dataset to search in.
            query: The query string to find similar documents.
            limit: The maximum number of similar documents to return (default is None, which returns up to 5 documents).

        Returns:
            A SyncSearchBuilder instance that can be used to retrieve the search results.

        Example usage:
            results = embedbase.search("my_dataset", "What is Python?", limit=3).get()
        """
        top_k = self.options.get("limit", None) or 5
        search_url = f"{self.client.embedbase_url}/{self.dataset}/search"

        request_body = {"query": self.query, "top_k": top_k}

        if "where" in self.options:
            request_body["where"] = self.options["where"]

        headers = self.client.headers
        res = requests.post(
            search_url, headers=headers, json=request_body, timeout=self.client.timeout
        )
        try:
            data = res.json()
        except json.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise EmbedbaseAPIException(res.text)

        if res.status_code != 200:
            raise EmbedbaseAPIException(data.get("error", res.text))

        return [
            SearchSimilarity(
                id=similarity["id"],
                similarity=similarity["score"],
                data=similarity["data"],
                embedding=similarity["embedding"],
                hash=similarity["hash"],
                metadata=similarity["metadata"],
            )
            for similarity in data["similarities"]
        ]

    def where(self, field: str, operator: str, value: Any) -> "SyncSearchBuilder":
        # self.options["where"] = {field: {operator: value}}
        self.options["where"] = {}
        self.options["where"][field] = value
        return self


class SyncListBuilder:
    def __init__(
        self,
        client: BaseClient,
        dataset: str,
        options: Optional[Dict[str, Any]] = None,
    ):
        if options is None:
            options = {}
        self.client = client
        self.dataset = dataset
        self.options = options

    def get(self) -> List[Document]:
        return self.list()

    def list(self) -> "SyncListBuilder":
        list_url = f"{self.client.embedbase_url}/{self.dataset}"

        if "offset" in self.options:
            list_url += f"?offset={self.options['offset']}"
        if "limit" in self.options:
            list_url += f"&limit={self.options['limit']}"

        headers = self.client.headers
        res = requests.get(list_url, headers=headers, timeout=self.client.timeout)
        try:
            data = res.json()
        except json.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise EmbedbaseAPIException(res.text)

        if res.status_code != 200:
            raise EmbedbaseAPIException(data.get("error", res.text))

        return [Document(**document) for document in data["documents"]]

    def offset(self, offset: int) -> "SyncListBuilder":
        self.options["offset"] = offset
        return self

    def limit(self, limit: int) -> "SyncListBuilder":
        self.options["limit"] = limit
        return self


@dataclass
class Dataset:
    client: "EmbedbaseClient"
    dataset: str

    def search(self, query: str, limit: Optional[int] = None) -> SyncSearchBuilder:
        """
        Search for documents similar to the given query in the specified dataset.

        Args:
            dataset: The name of the dataset to search in.
            query: The query string to find similar documents.
            limit: The maximum number of similar documents to return (default is None, which returns up to 5 documents).

        Returns:
            A SyncSearchBuilder instance that can be used to retrieve the search results.

        Example usage:
            results = dataset.search("my_dataset", "What is Python?", limit=3).get()
        """
        return SyncSearchBuilder(self.client, self.dataset, query, {"limit": limit})

    def add(self, document: str, metadata: Optional[Dict[str, Any]] = None) -> Document:
        """
        Add a new document to the specified dataset.

        Args:
            dataset: The name of the dataset to add the document to.
            document: A BatchAddDocument instance with the document string and optional metadata.

        Returns:
            A dictionary containing the ID of the added document and the status of the operation.

        Example usage:
            result = dataset.add("my_dataset", "Python is a programming language.", {"topic": "programming"})
        """
        return self.client.add(self.dataset, document, metadata)

    def batch_add(self, documents: List[Document]) -> List[Document]:
        """
        Add multiple documents to the specified dataset in a single batch.

        Args:
            dataset: The name of the dataset to add the documents to.
            documents: A list of documents, each containing the document data and optional metadata.

        Returns:
            A list of documents.

        Example usage:
            documents = [
                {"data": "Python is a programming language.", "metadata": {"topic": "programming"}},
                {"data": "Python is a snake.", "metadata": {"topic": "animals"}},
            ]
            results = dataset.batch_add("my_dataset", documents)
        """
        return self.client.batch_add(self.dataset, documents)

    def create_context(self, query: str, limit: Optional[int] = None) -> List[str]:
        """
        Retrieve documents similar to the given query and create a context.

        Args:
            dataset: The name of the dataset to search in.
            query: The query string to find similar documents.
            limit: The maximum number of similar documents to return (default is None, which returns up to 5 documents).

        Returns:
            A list of strings containing the document data for each similar document.

        Example usage:
            context = dataset.create_context("my_dataset", "What is Python?", limit=3)
        """
        return self.client.create_context(self.dataset, query, limit)

    def clear(self) -> None:
        """
        Clear all documents from the specified dataset.

        Args:
            dataset: The name of the dataset to clear.

        Example usage:
            dataset.clear("my_dataset")
        """
        return self.client.clear(self.dataset)

    def list(self) -> SyncListBuilder:
        """
        Retrieve a list of all documents in the specified dataset.

        Args:
            dataset: The name of the dataset to list.

        Returns:
            A list of document IDs and metadata.

        Example usage:
            documents = dataset.list()
        """
        return SyncListBuilder(self.client, self.dataset, {})

    def chunk_and_batch_add(self, documents: List[AddDocument]) -> List[Document]:
        """
        Chunk and add multiple documents to the specified dataset in a single batch.

        Args:
            documents: A list of documents.

        Returns:
            A list of documents.

        Example usage:
            documents = [
                {"data": "Python is a programming language.", metadata: {"topic": "programming"}},
                {"data": "Java is also a programming language.", metadata: {"topic": "programming"}},
            ]
            results = dataset.chunk_and_batch_add(documents)
        """
        return self.client.chunk_and_batch_add(self.dataset, documents)

    def create_max_context(
        self,
        query: str,
        max_tokens: int,
    ) -> str:
        """
        Create a context from a query by searching for similar documents and concatenating them up to the specified max tokens.

        Args:
            query: The query to search for.
            max_tokens: The maximum number of tokens for the context.

        Returns:
            A string containing the context.

        Example usage:
            context = dataset.create_max_context("What is Python?", max_tokens=100)
        """
        return self.client.create_max_context(self.dataset, query, max_tokens)

    def update(self, documents: List[Document]) -> List[Document]:
        """
        Update the documents in the specified dataset.

        Args:
            documents: A list of documents to update.

        Returns:
            A list of updated documents.

        Example usage:
            documents = [
                Document(id="document_id1", data="Updated document 1"),
                Document(id="document_id2", data="Updated document 2"),
            ]
            results = dataset.update(documents)
        """
        return self.client.update(self.dataset, documents)


class EmbedbaseClient(BaseClient):
    def __init__(
        self,
        embedbase_url: str = "https://api.embedbase.xyz",
        embedbase_key: Optional[str] = None,
        timeout: Optional[float] = 30,
    ):
        super().__init__(embedbase_url, embedbase_key, timeout=timeout)


    def create_context(
        self, dataset: str, query: str, limit: Optional[int] = None
    ) -> List[str]:
        """
        Retrieve documents similar to the given query and create a context.

        Args:
            dataset: The name of the dataset to search in.
            query: The query string to find similar documents.
            limit: The maximum number of similar documents to return (default is None, which returns up to 5 documents).

        Returns:
            A list of strings containing the document data for each similar document.

        Example usage:
            context = embedbase.create_context("my_dataset", "What is Python?", limit=3)
        """
        top_k = limit or 5
        search_url = f"{self.embedbase_url}/{dataset}/search"
        res = requests.post(
            search_url,
            headers=self.headers,
            json={"query": query, "top_k": top_k},
            timeout=self.timeout,
        )
        try:
            data = res.json()
        except json.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise EmbedbaseAPIException(res.text)

        if res.status_code != 200:
            raise EmbedbaseAPIException(data.get("error", res.text))

        return [similarity["data"] for similarity in data["similarities"]]

    def search(
        self, dataset: str, query: str, limit: Optional[int] = None
    ) -> SyncSearchBuilder:
        """
        Search for documents similar to the given query in the specified dataset.

        Args:
            dataset: The name of the dataset to search in.
            query: The query string to find similar documents.
            limit: The maximum number of similar documents to return (default is None, which returns up to 5 documents).

        Returns:
            A SyncSearchBuilder instance that can be used to retrieve the search results.

        Example usage:
            results = embedbase.search("my_dataset", "What is Python?", limit=3).get()
        """
        return SyncSearchBuilder(self, dataset, query, {"limit": limit})

    def where(
        self, dataset: str, query: str, field: str, operator: str, value: Any
    ) -> SyncSearchBuilder:
        return SyncSearchBuilder(
            self,
            dataset,
            query,
        ).where(field, operator, value)

    def add(
        self, dataset: str, document: str, metadata: Optional[Metadata] = None
    ) -> Document:
        """
        Add a new document to the specified dataset.

        Args:
            dataset: The name of the dataset to add the document to.
            document: A document.

        Returns:
            A document.

        Example usage:
            result = embedbase.add("my_dataset", "Python is a programming language.", {"topic": "programming"})
        """
        add_url = f"{self.embedbase_url}/{dataset}"
        res = requests.post(
            add_url,
            headers=self.headers,
            json={"documents": [{"data": document, "metadata": metadata}]},
            timeout=self.timeout,
        )
        try:
            data = res.json()
        except json.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise EmbedbaseAPIException(res.text)

        if res.status_code != 200:
            raise EmbedbaseAPIException(data.get("error", res.text))

        data = res.json()

        return Document(
            **data["results"][0],
        )

    def batch_add(self, dataset: str, documents: List[AddDocument]) -> List[Document]:
        """
        Add multiple documents to the specified dataset in a single batch.

        Args:
            dataset: The name of the dataset to add the documents to.
            documents: A list of documents.

        Returns:
            A list of documents.

        Example usage:
            documents = [
                {"data": "Python is a programming language.", metadata: {"topic": "programming"}},
                {"data": "Java is also a programming language.", metadata: {"topic": "programming"}},
            ]
            results = embedbase.batch_add("my_dataset", documents)
        """
        add_url = f"{self.embedbase_url}/{dataset}"
        res = requests.post(
            add_url,
            headers=self.headers,
            json={"documents": documents},
            timeout=self.timeout,
        )
        try:
            data = res.json()
        except json.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise EmbedbaseAPIException(res.text)

        if res.status_code != 200:
            raise EmbedbaseAPIException(data.get("error", res.text))

        return [
            Document(
                **result,
            )
            for result in data["results"]
        ]

    def clear(self, dataset: str) -> None:
        """
        Clear all documents from the specified dataset.

        Args:
            dataset: The name of the dataset to clear.

        Example usage:
            embedbase.clear("my_dataset")
        """
        url = f"{self.embedbase_url}/{dataset}/clear"
        res = requests.get(url, headers=self.headers, timeout=self.timeout)
        try:
            data = res.json()
        except json.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise EmbedbaseAPIException(res.text)

        if res.status_code != 200:
            raise EmbedbaseAPIException(data.get("error", res.text))

    def dataset(self, dataset: str) -> Dataset:
        return Dataset(client=self, dataset=dataset)

    def datasets(self) -> List[ClientDatasets]:
        """
        Retrieve a list of all datasets.

        Returns:
            A list of dataset names and metadata.

        Example usage:
            datasets = embedbase.datasets()
        """
        datasets_url = f"{self.embedbase_url}/datasets"
        res = requests.get(datasets_url, headers=self.headers, timeout=self.timeout)
        try:
            data = res.json()
        except json.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise EmbedbaseAPIException(res.text)

        if res.status_code != 200:
            raise EmbedbaseAPIException(data.get("error", res.text))

        return [ClientDatasets(**dataset) for dataset in data["datasets"]]

    def list(self, dataset: str) -> SyncListBuilder:
        """
        Retrieve a list of all documents in the specified dataset.

        Args:
            dataset: The name of the dataset to list.

        Returns:
            A list of document IDs and metadata.

        Example usage:
            documents = embedbase.list("my_dataset")
        """
        return SyncListBuilder(self, dataset, {})

    def generate(
        self, prompt: str, options: GenerateOptions = None
    ) -> Generator[str, None, None]:
        """
        Generate text from an LLM using a synchronous generator that fetches generated text data in chunks.

        Args:
            prompt (str): The text prompt to send to the API for generating responses.
            options (dict, optional): Options for the generation process, including history.
                                    Defaults to None.

        Returns:
            Generator[str, None, None]: A synchronous generator that yields generated text data in chunks.
        """
        url = (options and options.get("url")) or "https://app.embedbase.xyz/api/chat"

        options = options or {
            "history": [],
        }

        system = ""
        if options.get("history"):
            system_index = next(
                (
                    i
                    for i, item in enumerate(options["history"])
                    if item["role"] == "system"
                ),
                -1,
            )
            if system_index > -1:
                system = options["history"][system_index]["content"]
                del options["history"][system_index]

        return sync_stream(
            url,
            json.dumps(
                {"prompt": prompt, "system": system, "history": options["history"]}
            ),
            self.headers,
            self.timeout,
        )

    def chunk_and_batch_add(
        self, dataset: str, documents: List[AddDocument]
    ) -> List[Document]:
        """
        Add multiple documents to the specified dataset in a single batch asynchronously.

        Args:
            dataset: The name of the dataset to add the documents to.
            documents: A list of documents.

        Returns:
            A list of documents.

        Example usage:
            documents = [
                {"data": "Python is a programming language.", metadata: {"topic": "programming"}},
                {"data": "Java is also a programming language.", metadata: {"topic": "programming"}},
            ]
            results = embedbase.chunk_and_batch_add("my_dataset", documents)
        """
        chunks = []
        for document_index, document in enumerate(documents):
            for chunk_index, chunk in enumerate(split_text(document["data"])):
                chunks.append(
                    {
                        "data": chunk.chunk,
                        "metadata": {
                            **document.get("metadata", {}),
                            "documentIndex": document_index,
                            "chunkIndex": chunk_index,
                            "chunkStart": chunk.start,
                            "chunkEnd": chunk.end,
                        },
                    }
                )

        parallel_batch_size = 100

        def batch_chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        results = []

        def add_batch(batch):
            results.append(self.batch_add(dataset, batch))

        with ThreadPool() as pool:
            pool.map(add_batch, batch_chunks(chunks, parallel_batch_size))

        return list(itertools.chain.from_iterable(results))

    def create_max_context(
        self,
        dataset: Union[str, List[str]],
        query: str,
        max_tokens: Union[int, List[int]],
    ) -> str:
        """
        Create a context from a query by searching for similar documents and
        concatenating them up to the specified max tokens.

        Args:
            dataset: The name of the dataset to search.
            query: The query to search for.
            max_tokens: the maximum number of tokens for the context.

        Returns:
            A string containing the context.

        Example usage:
            context = create_max_context("programming", "Python is a programming language.", 30)
            print(context)
            # Python is a programming language.
            # Python is a high-level, general-purpose programming language.
            # Python is interpreted, dynamically typed and garbage-collected.
            # Python is designed to be highly extensible.
            # Python is a multi-paradig
            # or
            context = create_max_context(["programming", "science"], "Python lives planet earth.", [3, 30])
            print(context)
            # Pyt
            # The earth orbits the sun.
            # The earth is the third planet from the sun.
            # The earth is the only planet known to support life.
            # The earth formed approximately 4.5 billion years ago.
            # The earth's gravity interacts with other objects in space, especially the sun and the moon.
        """

        def create_context_for_dataset(dataset, max_tokens):
            top_k = 100
            context = self.create_context(dataset, query, top_k)
            merged_context, size = merge_and_return_tokens(context, max_tokens)

            tries = 0
            max_tries = 3
            while size < max_tokens and tries < max_tries:
                top_k *= 3
                context = self.create_context(dataset, query, top_k)
                merged_context, size = merge_and_return_tokens(context, max_tokens)
                tries += 1

            if size < max_tokens:
                print(
                    f"Warning: context for dataset '{dataset}' is smaller than the max tokens ({size} < {max_tokens})"
                )
            return merged_context

        if not isinstance(dataset, list):
            dataset = [dataset]

        if not isinstance(max_tokens, list):
            max_tokens = [max_tokens for _ in range(len(dataset))]

        if len(dataset) != len(max_tokens):
            raise ValueError("The number of datasets and max_tokens should be equal.")

        contexts = []
        for ds, mt in zip(dataset, max_tokens):
            context = create_context_for_dataset(ds, mt)
            contexts.append(context)

        return "\n\n".join(contexts)

    def update(self, dataset: str, documents: List[Document]) -> List[Document]:
        """
        Update the documents in the specified dataset.

        Args:
            dataset: The name of the dataset to update.
            documents: A list of documents to update.

        Returns:
            A list of updated documents.

        Example usage:
            documents = [
                Document(id="document_id1", data="Updated document 1"),
                Document(id="document_id2", data="Updated document 2"),
            ]
            results = embedbase.update("my_dataset", documents)
        """
        update_url = f"{self.embedbase_url}/{dataset}"
        res = requests.put(
            update_url,
            headers=self.headers,
            json={"documents": [doc.dict() for doc in documents]},
            timeout=self.timeout,
        )
        try:
            data = res.json()
        except json.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise EmbedbaseAPIException(res.text)

        if res.status_code != 200:
            raise EmbedbaseAPIException(data.get("error", res.text))

        return [Document(**result) for result in data["results"]]

    def generate_text(self, model: str, prompt: str, options: Optional[dict] = None):
        """
        Generate text using a specific language model.

        Args:
            model (str): The name or identifier of the language model.
            prompt (str): The input text prompt for generating the output text.
            options (dict, optional): Additional options for the generation process.

        Returns:
            The generated text as a string.

        Example usage:
            client = EmbedbaseClient("https://api.embedbase.xyz", "YOUR_API_KEY")
            generated_text = client.generate_text("openai/gpt-3.5-turbo", "Hello, how are you?")
            print(generated_text)
        """
        if options is None:
            options = {}

        url = "https://app.embedbase.xyz/api/chat"
        data = {"prompt": prompt, "model": model, "stream": False, **options}

        response = requests.post(
            url, headers=self.headers, json=data, timeout=self.timeout
        )
        response.raise_for_status()

        result = response.json()
        return result["generated_text"]

    def stream_text(self, model: str, prompt: str, options: Optional[dict] = None):
        """
        Generate text using a specific language model in a streaming fashion.

        Args:
            model (str): The name or identifier of the language model.
            prompt (str): The input text prompt for generating the output text.
            options (dict, optional): Additional options for the generation process.

        Yields:
            Each generated text chunk as a string.

        Example usage:
            client = EmbedbaseClient("https://api.embedbase.xyz", "YOUR_API_KEY")
            for chunk in client.stream_text("openai/gpt-3.5-turbo", "Hello, how are you?"):
                print(chunk)
        """
        if options is None:
            options = {}

        url = "https://app.embedbase.xyz/api/chat"
        data = {"prompt": prompt, "model": model, "stream": True, **options}

        # use sync_stream

        return sync_stream(
            url,
            json.dumps(data),
            self.headers,
            self.timeout,
        )

    @staticmethod
    def list_models() -> List[Dict[str, Any]]:
        """
        Lists all models available on the platform.

        Returns:
            A list of dictionaries, each containing information about a model.

        Example usage:
            models = EmbedbaseClient.list_models()
            print(models)
        """
        headers = {
            "Authorization": "Bearer patBrBkdsFw0ArVlF.89a5669f5fd05d20e1d0f77216d072d929b13a215c0471b9a1a2d764537cbe8d"
        }

        response = requests.get(
            "https://api.airtable.com/v0/appwJMZ6IAUnKpSwV/all",
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        return [
            {
                "id": record["id"],
                "object": "model",
                "owned_by": record["fields"].get("contact", "anonymous"),
                "permission": ["read"],
                "createdTime": record["createdTime"],
                **record["fields"],
            }
            for record in data["records"]
            if "url" in record["fields"]
        ]

    def get_models(self) -> List[Dict[str, Any]]:
        """
        Retrieves a list of models available for use.

        Returns:
            A list of dictionaries, each containing information about a model.

        Example usage:
            client = EmbedbaseClient("https://api.embedbase.xyz", "YOUR_API_KEY")
            models = client.get_models()
            print(models)
        """
        other_models = self.list_models()
        models = [
            {"name": "openai/gpt-4", "description": "OpenAI's GPT-4 model"},
            {
                "name": "openai/gpt-3.5-turbo-16k",
                "description": "OpenAI's GPT-3.5 Turbo 16k model",
            },
            {
                "name": "openai/gpt-3.5-turbo",
                "description": "OpenAI's GPT-3.5 Turbo model",
            },
            {"name": "google/bison", "description": "Google's Bison model"},
            {
                "name": "bigscience/bloomz-7b1",
                "description": "BigScience's Bloomz 7b1 model",
            },
            *[
                {"name": model["model"], "description": json.dumps(model)}
                for model in other_models
            ],
        ]
        return models

    def use_model(self, model_name: str):
        """
        Create an instance of a language model for generating and streaming text.

        Args:
            model_name (str): The name or identifier of the language model.

        Returns:
            An instance of the Model class with generate_text and stream_text as methods.

        Example usage:
            client = EmbedbaseClient("https://api.embedbase.xyz", "YOUR_API_KEY")
            gpt3_model = client.use_model("openai/gpt-3.5-turbo")
            generated_text = gpt3_model.generate_text("Hello!")
            for chunk in gpt3_model.stream_text("Hi!"):
                print(chunk)
        """
        generate_text = self.generate_text
        stream_text = self.stream_text

        class Model:
            def generate_text(
                self, prompt: str, options: Optional[Dict[str, Any]] = None
            ):
                return generate_text(model_name, prompt, options)

            def stream_text(
                self, prompt: str, options: Optional[Dict[str, Any]] = None
            ):
                return stream_text(model_name, prompt, options)

        model = Model()
        model.client = self
        return model
