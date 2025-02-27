from loguru import logger
from xinference.client import Client


logger.add("logs/init_xinference.log", enqueue=True, rotation="10 MB")


HOST = "localhost"
PORT = 9997
EMBEDDING_MODEL = "bge-m3"
EMBEDDING_BATCH_SIZE = 32
RERANK_MODEL = "bge-reranker-v2-gemma"


list_models_new = [
    {
        "model": EMBEDDING_MODEL,
        "model_type": "embedding",
        "kwarg_model": {"batch_size": EMBEDDING_BATCH_SIZE},
    },
    {
        "model": RERANK_MODEL,
        "model_type": "rerank",
        "kwarg_model": {
            "batch_size": None
        },  # реранк модели бесполезно устанавливать размер батча
    },
]


def init_xinference():
    logger.info("Загрузка моделей в xinference")
    logger.info(f"Модели для загрузки: {list_models_new}")

    client = Client(f"http://{HOST}:{PORT}")

    list_models_old = client.list_models()
    logger.info(
        f"Модели уже загруженные в xinference: {list(list_models_old.keys())}"
    )

    for i in list_models_new:
        model, model_type = i["model"], i["model_type"]

        if model not in list_models_old:
            logger.info(f"Загрузка модели {model}")
            try:
                client.launch_model(model, model_type=model_type)
                logger.info(f"Загрузка модели {model} завершена")
            except Exception as e:
                logger.error(f"Ошибка при загрузке модели: {model}: {e}")
                raise

    logger.info("Загрузка моделей завершена")
