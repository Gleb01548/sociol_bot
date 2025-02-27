from typing import List

from loguru import logger
from qdrant_client import QdrantClient
from src.models.embedding_api import get_embeddings
from src.models.rerank_api import get_rerank
from src.models.init_xinference import init_xinference


init_xinference()


class ContextSearch:
    def __init__(
        self,
        collection_name: str,
        qdrant_url: str,
        limit: int = 5,
    ):
        self.collection_name = collection_name
        self.qdrant_client = QdrantClient(qdrant_url)
        self.limit = limit

    def query_records(self, query: str) -> list:
        vector = get_embeddings([query])[0]

        return self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=self.limit,
            timeout=10_000,
        ).points

    def create_info(self, points):
        info = []
        for point in points:
            text = ""
            text += point.payload["title"]
            text += "\n\n"
            text += point.payload["post"]
            text += "\n\n"
            text += point.payload["short"]
            text += "\n\n"
            text += point.payload["review"]
            text += "\n\n"
            text += point.payload["tables"]
            text += "\n\n"
            text += point.payload["comment"]
            text += "\n\n"
            text += point.payload["method"]
            text += "\n\n"
            info.append(text)
        return info

    def reranker_func(self, question, info):
        logger.info(question, info)
        try:
            score = get_rerank(query=question, documents=info)
        except Exception as e:
            logger.info(f"Ошибка: {e}. {info}")
            logger.info(f"Ошибка: {[[question, i] for i in texts]}")

            raise

        index_score = sorted(
            [(index, score) for index, score in enumerate(score)],
            key=lambda x: x[1],
            reverse=True,
        )
        reranked_points = [info[i[0]] for i in index_score]

        return reranked_points

    def create_context(self, user_message: str) -> List[dict]:
        points = self.query_records(query=user_message)

        info = self.create_info(points)
        print("vector")
        info = self.reranker_func(question=user_message, info=info)
        print("rerank")

        return info
