import pandas as pd

from tqdm import tqdm
from loguru import logger
from qdrant_client import QdrantClient, models


from src.models.init_xinference import init_xinference
from src.models.embedding_api import get_embeddings

COLLECTION_NAME = "social"

init_xinference()


records = pd.read_csv("./data/parsed_data.csv").fillna("").to_dict(orient="records")

client = QdrantClient(url="localhost")
logger.info(f"Создание коллекции с именем {COLLECTION_NAME}")
client.delete_collection(COLLECTION_NAME, timeout=1000)

embed_size = len(get_embeddings(input_texts=["test"])[0])
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(
        size=embed_size,
        distance=models.Distance.COSINE,
        multivector_config=models.MultiVectorConfig(
            comparator=models.MultiVectorComparator.MAX_SIM
        ),
    ),
    timeout=1000,
)


for index, record in enumerate(tqdm(records)):
    title = record["title"]
    post = record["post"]
    short = record["short"]
    review = record["review"]
    method = record["method"]
    comment = record["comment"]
    tables = record["tables"]

    input_text = [title, post, review, short]
    input_text = [i for i in input_text if i]

    emb = get_embeddings(input_texts=input_text)

    try:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=index,
                    vector=emb,
                    payload={
                        "title": title,
                        "post": post,
                        "short": short,
                        "review": review,
                        "method": method,
                        "comment": comment,
                        "tables": tables,
                    },
                )
            ],
        )
    except:
        print(record)
        print(len(input_text))
        raise
