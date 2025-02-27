import aiohttp
from typing import List

import requests
from loguru import logger

# logger.remove()
logger.add("logs/embedding.log", enqueue=True, rotation="10 MB")


HOST = "localhost"
PORT = 9997
EMBEDDING_MODEL = "bge-m3"


url = f"http://{HOST}:{PORT}/v1/embeddings"
headers = {"accept": "application/json", "Content-Type": "application/json"}


async def get_embeddings_async(input_texts: List[str]) -> List[List[float]]:
    logger.info(
        f"Запрос к эмбед. модели {input_texts[:3]}..."
        f"Всего записей: {len(input_texts)}"
    )

    data = {"model": EMBEDDING_MODEL, "input": input_texts}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                json_response = await response.json()
                logger.info(f"Ответ api: {str(json_response)[:100]}")
                embeddings = [item["embedding"] for item in json_response["data"]]
                logger.info(f"Получено эмбеддингов: {len(embeddings)}")

                return embeddings

    except Exception as e:
        logger.error(f"Ошибка при работе эмбед. сревиса: {e}")
        raise


def get_embeddings(input_texts: List[str]) -> List[List[float]]:
    logger.info(
        f"Запрос к эмбед. модели {input_texts[:3]}..."
        f"Всего записей: {len(input_texts)}"
    )

    data = {"model": EMBEDDING_MODEL, "input": input_texts}

    try:
        response = requests.post(url, headers=headers, json=data).json()

        return [i["embedding"] for i in response["data"]]
    except Exception as e:
        logger.error(f"Ошибка при получении эмбеддингов: {e}")
