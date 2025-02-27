import aiohttp
from typing import List

import requests
from loguru import logger

# logger.remove()
logger.add("logs/rerank.log", enqueue=True, rotation="10 MB")

HOST = "localhost"
PORT = 9997
RERANK_MODEL = "bge-reranker-v2-gemma"

url = f"http://{HOST}:{PORT}/v1/rerank"
headers = {"accept": "application/json", "Content-Type": "application/json"}


async def get_rerank_async(query: str, documents: List[str]) -> List[float]:
    data = {"model": RERANK_MODEL, "query": query, "documents": documents}
    logger.info(
        f"Запрос {query}. "
        f"Документы: {documents[:3]}... всего документов: {len(documents)}"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                response = await response.json()
                logger.info(f"Ответ модели: {str(response)[:100]}")

                response = [
                    (i["index"], i["relevance_score"]) for i in response["results"]
                ]
                response = [i[1] for i in sorted(response, key=lambda x: x[0])]

                logger.info(
                    f"Ответ сервиса: {response[:3]}... "
                    f"Всего записей: {len(response)}"
                )
        return response

    except Exception as e:
        logger.error(f"Ошибка при работе сервиса реранк модели: {str(e)}")
        raise


def get_rerank(query: str, documents: List[str]) -> List[float]:
    data = {"model": RERANK_MODEL, "query": query, "documents": documents}

    try:
        response = requests.post(url, headers=headers, json=data).json()
        response = [(i["index"], i["relevance_score"]) for i in response["results"]]
        response = [i[1] for i in sorted(response, key=lambda x: x[0])]

        return response
    except Exception as e:
        logger.error(f"Ошибка при работе сервиса: {str(e)}")
        raise
