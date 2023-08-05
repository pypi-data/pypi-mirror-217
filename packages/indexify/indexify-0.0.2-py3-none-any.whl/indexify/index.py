import requests

from .data_containers import *
from .utils import _get_payload


class Index:

    def __init__(self, url, index):
        self._url = url
        self._index = index

    def search(self, query: str, top_k: int) -> list[TextChunk]:
        req = SearchChunk(index=self._index, query=query, k=top_k)
        resp = requests.get(f"{self._url}/index/search", json=req.to_dict())
        payload = _get_payload(resp)
        result = []
        for res in payload["results"]:
            result.append(TextChunk(text=res["text"], metadata=res["metadata"]))
        return result
