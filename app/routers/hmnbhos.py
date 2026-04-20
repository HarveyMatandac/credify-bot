from fastapi import APIRouter
from app.bots.hmnbhos.handler import Automation

router = APIRouter()
router.base_path = "/hmnbhos"


@router.post("/")
def run(payload: dict):
    handler = Automation(payload.model_dump())
    handler_response = handler.start()

    return {"status": "accepted", "result": handler_response}


@router.get("/sample_0")
def get():
    return "success"
