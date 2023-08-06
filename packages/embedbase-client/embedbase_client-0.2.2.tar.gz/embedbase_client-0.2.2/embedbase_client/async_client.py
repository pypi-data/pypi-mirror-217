from typing import Any, Dict, List, Optional, Union

import asyncio
import itertools
import json
from dataclasses import dataclass

import httpx
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
from embedbase_client.utils import CustomAsyncGenerator, async_stream


class AsyncSearchBuilder:
    def __init__(
        self, client, dataset: str, query: str, options: Optional[Dict[str, Any]] = None
    ):
        if options is None:
            options = {}
        self.client = client
        self.dataset = dataset
        self.query = query
        self.options = options

    async def get(self) -> List[SearchSimilarity]:
        return await self.search()

    async def search(self) -> "AsyncSearchBuilder":
        """
        Search for documents similar to the given query in the specified dataset asynchronously.

        Returns:
            An AsyncSearchBuilder instance that can be used to retrieve the search results.

        Example usage:
            results = await embedbase.search("my_dataset", "What is Python?", limit=3).get()
        """
        top_k = self.options.get("limit", None) or 5
        search_url = f"{self.client.embedbase_url}/{self.dataset}/search"

        request_body = {"query": self.query, "top_k": top_k}

        if "where" in self.options:
            request_body["where"] = self.options["where"]

        headers = self.client.headers
        async with httpx.AsyncClient() as client:
            res = await client.post(
                search_url,
                headers=headers,
                json=request_body,
                timeout=self.client.timeout,
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

    def where(self, field: str, operator: str, value: Any) -> "AsyncSearchBuilder":
        # self.options["where"] = {field: {operator: value}}
        self.options["where"] = {}
        self.options["where"][field] = value
        return self


class AsyncListBuilder:
    def __init__(
        self,
        client,
        dataset: str,
        options: Optional[Dict[str, Any]] = None,
    ):
        if options is None:
            options = {}
        self.client = client
        self.dataset = dataset
        self.options = options

    async def get(self) -> List[Document]:
        return await self.list()

    async def list(self) -> "AsyncListBuilder":
        """
        Retrieve a list of all documents in the specified dataset asynchronously.

        Returns:
            A list of document IDs and metadata.

        Example usage:
            documents = await embedbase.list()
        """
        list_url = f"{self.client.embedbase_url}/{self.dataset}"

        if "offset" in self.options:
            list_url += f"?offset={self.options['offset']}"
        if "limit" in self.options:
            list_url += f"&limit={self.options['limit']}"

        headers = self.client.headers
        async with httpx.AsyncClient() as client:
            res = await client.get(
                list_url, headers=headers, timeout=self.client.timeout
            )
            try:
                data = res.json()
            except json.JSONDecodeError:
                # pylint: disable=raise-missing-from
                raise EmbedbaseAPIException(res.text)

            if res.status_code != 200:
                raise EmbedbaseAPIException(data.get("error", res.text))

            return [Document(**document) for document in data["documents"]]

    def offset(self, offset: int) -> "AsyncListBuilder":
        self.options["offset"] = offset
        return self

    def limit(self, limit: int) -> "AsyncListBuilder":
        self.options["limit"] = limit
        return self


@dataclass
class AsyncDataset:
    client: "EmbedbaseAsyncClient"
    dataset: str

    def search(self, query: str, limit: Optional[int] = None) -> AsyncSearchBuilder:
        """
        Search for documents similar to the given query in the specified dataset asynchronously.

        Args:
            query: The query string to find similar documents.
            limit: The maximum number of similar documents to return (default is None, which returns up to 5 documents).

        Returns:
            A list of SearchSimilarity instances containing the similarity score, data, embedding hash and metadata of similar documents.

        Example usage:
            results = await dataset.search("What is Python?", limit=3)
        """
        return AsyncSearchBuilder(self.client, self.dataset, query, {"limit": limit})

    async def add(
        self, document: str, metadata: Optional[Dict[str, Any]] = None
    ) -> Document:
        """
        Add a new document to the specified dataset asynchronously.

        Args:
            document: A document.

        Returns:
            A document.

        Example usage:
            result = await dataset.add("Python is a programming language.", {"topic": "programming"})
        """
        return await self.client.add(self.dataset, document, metadata)

    async def batch_add(self, documents: List[AddDocument]) -> List[Document]:
        """
        Add multiple documents to the specified dataset in a single batch asynchronously.

        Args:
            documents: A list of documents.

        Returns:
            A list of documents.

        Example usage:
            documents = [
                {"data": "Python is a programming language.", metadata: {"topic": "programming"}},
                {"data": "Java is also a programming language.", metadata: {"topic": "programming"}},
            ]
            results = await dataset.batch_add(documents)
        """
        return await self.client.batch_add(self.dataset, documents)

    async def create_context(
        self, query: str, limit: Optional[int] = None
    ) -> List[str]:
        """
        Retrieve documents similar to the given query and create a context asynchronously.

        Args:
            query: The query string to find similar documents.
            limit: The maximum number of similar documents to return (default is None, which returns up to 5 documents).

        Returns:
            A list of strings containing the document data for each similar document.

        Example usage:
            context = await dataset.create_context("What is Python?", limit=3)
        """
        return await self.client.create_context(self.dataset, query, limit)

    async def clear(self) -> None:
        """
        Clear all documents from the specified dataset asynchronously.

        Example usage:
            await dataset.clear()
        """
        return await self.client.clear(self.dataset)

    def list(self) -> AsyncListBuilder:
        """
        Retrieve a list of all documents in the specified dataset asynchronously.

        Returns:
            A list of documents.

        Example usage:
            documents = await dataset.list()
        """
        return AsyncListBuilder(self.client, self.dataset)

    async def chunk_and_batch_add(self, documents: List[AddDocument]) -> List[Document]:
        """
        Chunk and add multiple documents to the specified dataset in a single batch asynchronously.

        Args:
            documents: A list of documents.

        Returns:
            A list of documents.

        Example usage:
            documents = [
                {"data": "Python is a programming language.", metadata: {"topic": "programming"}},
                {"data": "Java is also a programming language.", metadata: {"topic": "programming"}},
            ]
            results = await dataset.chunk_and_batch_add(documents)
        """
        return await self.client.chunk_and_batch_add(self.dataset, documents)

    async def create_max_context(
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
            context = await dataset.create_max_context("What is Python?", max_tokens=100)
        """
        return await self.client.create_max_context(self.dataset, query, max_tokens)

    async def update(self, document: Document) -> Document:
        """
        Update the documents in the specified dataset asynchronously.

        Args:
            dataset: The name of the dataset to update.
            documents: A list of documents to update.

        Returns:
            A list of updated documents.

        Example usage:
            documents = [
                {"id": "document_id1", "data": "Updated document 1"},
                {"id": "document_id2", "data": "Updated document 2"},
            ]
            results = await dataset.update(documents)
        """
        return await self.client.update(self.dataset, document)


class EmbedbaseAsyncClient(BaseClient):
    def dataset(self, dataset: str) -> AsyncDataset:
        return AsyncDataset(client=self, dataset=dataset)

    async def create_context(
        self, dataset: str, query: str, limit: Optional[int] = None
    ) -> List[str]:
        """
        Retrieve documents similar to the given query and create a context asynchronously.
        Args:
            dataset: The name of the dataset to perform similarity search on.
            query: The query string to find similar documents.
            limit: The maximum number of similar documents to return (default is None, which returns up to 5 documents).

        Returns:
            A list of strings containing the document data for each similar document.
        Example usage:
            context = await embedbase.create_context("my_dataset", "What is Python?", limit=3)
        """

        top_k = limit or 5
        search_url = f"/{dataset}/search"
        async with httpx.AsyncClient(
            app=self.fastapi_app, base_url=self.embedbase_url
        ) as client:
            res = await client.post(
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
    ) -> AsyncSearchBuilder:
        """
        Search for documents similar to the given query in the specified dataset asynchronously.
        Args:
            dataset: The name of the dataset to perform similarity search on.
            query: The query string to find similar documents.
            limit: The maximum number of similar documents to return (default is None, which returns up to 5 documents).

        Returns:
            A list of SearchSimilarity instances containing the embedding, hash, metadata, and string contents of each
            document, as well as the similarity score between the document and the query.

        Example usage:
            results = await embedbase.search("my_dataset", "What is Python?", limit=3)
        """
        return AsyncSearchBuilder(self, dataset, query, {"limit": limit})

    async def add(
        self, dataset: str, document: str, metadata: Optional[Metadata] = None
    ) -> Document:
        """
        Add a document to the specified dataset asynchronously.
        Args:
            dataset: The name of the dataset to add the document to.
            document: The document string to add to the dataset.
            metadata: Optional metadata about the document.

        Returns:
            A document.
        Example usage
            result = await embedbase.add("my_dataset", "Python is a programming language.", metadata={"topic": "programming"})
        """
        add_url = f"/{dataset}"
        async with httpx.AsyncClient(
            app=self.fastapi_app, base_url=self.embedbase_url
        ) as client:
            res = await client.post(
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
        return Document(**data["results"][0])

    async def batch_add(
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
            results = await embedbase.batch_add("my_dataset", documents)
        """
        add_url = f"/{dataset}"
        async with httpx.AsyncClient(
            app=self.fastapi_app, base_url=self.embedbase_url
        ) as client:
            res = await client.post(
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

        return [Document(**result) for result in data["results"]]

    async def clear(self, dataset: str) -> None:
        """
        Clear all documents from the specified dataset asynchronously.
        Args:
            dataset: The name of the dataset to clear.
        Example usage
            await embedbase.clear("my_dataset")
        """
        url = f"/{dataset}/clear"
        async with httpx.AsyncClient(
            app=self.fastapi_app, base_url=self.embedbase_url
        ) as client:
            res = await client.get(url, headers=self.headers, timeout=self.timeout)
        try:
            data = res.json()
        except json.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise EmbedbaseAPIException(res.text)

        if res.status_code != 200:
            raise EmbedbaseAPIException(data.get("error", res.text))

    async def datasets(self) -> List[ClientDatasets]:
        """
        Retrieve a list of all datasets asynchronously.
        Returns:
            A list of dataset names.
        Example usage
            results = await embedbase.datasets()
        """
        datasets_url = "/datasets"
        async with httpx.AsyncClient(
            app=self.fastapi_app, base_url=self.embedbase_url
        ) as client:
            res = await client.get(
                datasets_url, headers=self.headers, timeout=self.timeout
            )
        try:
            data = res.json()
        except json.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise EmbedbaseAPIException(res.text)

        if res.status_code != 200:
            raise EmbedbaseAPIException(data.get("error", res.text))

        return [ClientDatasets(**dataset) for dataset in data["datasets"]]

    def list(self, dataset: str) -> AsyncListBuilder:
        """
        Retrieve a list of all documents in the specified dataset asynchronously.

        Args:
            dataset: The name of the dataset to list.

        Returns:
            A list of document IDs and metadata.

        Example usage:
            documents = await embedbase.list("my_dataset")
        """
        return AsyncListBuilder(self, dataset, {})

    def generate(
        self, prompt: str, options: GenerateOptions = None
    ) -> CustomAsyncGenerator:
        """
        Generate text from an LLM using a asynchronous generator that fetches generated text data in chunks.

        Args:
            prompt (str): The text prompt to send to the API for generating responses.
            options (dict, optional): Options for the generation process, including history.
                                    Defaults to None.

        Returns:
            CustomAsyncGenerator[str, None, None]: An asynchronous generator that yields generated text data in chunks.
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

        async_gen = async_stream(
            url,
            json.dumps(
                {"prompt": prompt, "system": system, "history": options["history"]}
            ),
            self.headers,
        )
        return CustomAsyncGenerator(async_gen)

    async def chunk_and_batch_add(
        self, dataset: str, documents: List[AddDocument]
    ) -> List[Document]:
        """
        Chunk and add multiple documents to the specified dataset in a single batch asynchronously.

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
            results = await embedbase.chunk_and_batch_add("my_dataset", documents)
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

        results = await asyncio.gather(
            *[
                self.batch_add(dataset, batch)
                for batch in batch_chunks(chunks, parallel_batch_size)
            ]
        )

        return list(itertools.chain.from_iterable(results))

    async def create_max_context(
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
            context = await create_max_context("programming", "Python is a programming language.", 30)
            print(context)
            # Python is a programming language.
            # Python is a high-level, general-purpose programming language.
            # Python is interpreted, dynamically typed and garbage-collected.
            # Python is designed to be highly extensible.
            # Python is a multi-paradig
            # or
            context = await create_max_context(["programming", "science"], "Python lives planet earth.", [3, 30])
            print(context)
            # Pyt
            # The earth orbits the sun.
            # The earth is the third planet from the sun.
            # The earth is the only planet known to support life.
            # The earth formed approximately 4.5 billion years ago.
            # The earth's gravity interacts with other objects in space, especially the sun and the moon.
        """

        async def create_context_for_dataset(d, max_tokens):
            top_k = 100
            context = await self.create_context(d, query, top_k)
            merged_context, size = merge_and_return_tokens(context, max_tokens)

            tries = 0
            max_tries = 3
            while size < max_tokens and tries < max_tries:
                top_k *= 3
                context = await self.create_context(dataset, query, top_k)
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
            context = await create_context_for_dataset(ds, mt)
            contexts.append(context)

        return "\n\n".join(contexts)

    async def update(self, dataset: str, documents: List[Document]) -> List[Document]:
        """
        Update the documents in the specified dataset asynchronously.

        Args:
            dataset: The name of the dataset to update.
            documents: A list of documents to update.

        Returns:
            A list of updated documents.

        Example usage:
            documents = [
                {"id": "document_id1", "data": "Updated document 1"},
                {"id": "document_id2", "data": "Updated document 2"},
            ]
            results = await embedbase.update("my_dataset", documents)
        """
        update_url = f"{self.embedbase_url}/{dataset}"
        async with httpx.AsyncClient() as client:
            res = await client.put(
                update_url,
                headers=self.headers,
                json={"documents": [dict(doc) for doc in documents]},
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
