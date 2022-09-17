import os
from typing import Dict
from fastapi import APIRouter

ASC3_DIR = os.path.dirname(os.path.abspath(__file__))
from utils import get_logger, load_yaml
from models import Classifier

config = load_yaml(os.path.join(ASC3_DIR, "config.yaml"))["API"]
logger = get_logger("router")

api_router = APIRouter()
classifier = Classifier(
    config=config,
    logger=logger,
)
classifier.set_model()


def check_query(query: dict) -> dict:
    """주어진 query에 대해서 딕셔너리의 속성값이 올바르게 들어있는지 확인

    Args:
        query (Query): model.Query에서 정의한 형태

    Return:
        response (dict): "stats", "data", "message"의 key을 가진 데이터

    """
    not_found_keys = list()
    for key in ["sample_id", "inhouse_total_ac", "gene_diseases"]:
        if key not in query:
            not_found_keys.append(key)

    if not_found_keys:
        return {
            "status": "error",
            "data": dict(),
            "message": f"{', '.join(sorted(not_found_keys))} not passed",
        }

    return dict()


@api_router.get("/")
def health() -> Dict[str, str]:
    return {"health": "ok"}


@api_router.post("/predict")
def predict(query: dict) -> Dict:
    response = {"status": "success"}
    response.update(check_query(query))

    if "message" in response:
        logger.warning(response["message"])
        return response

    logger.info(f"SAMPLE ID({query['sample_id']})'s query accepted")

    response["data"] = classifier.predict(query)
    return response
