from fastapi import APIRouter
from prefect import flow, task
from payer_website_autofiller.bots.hmnbhos.handler import Automation
from payer_website_autofiller.frontend.schemas import ValidationRequest

router = APIRouter()
router.base_path = "/hmnbhos"


@task
def hmnbnos_run(payload):
    handler = Automation(payload)
    with handler.start():
        pass


@flow
def handlers(payload):
    hmnbnos_run(payload)


@router.post("/", status_code=202)
def run(payload: ValidationRequest):
    job_id = "j123"

    handlers(payload)

    return {"job_id": job_id, "status": "accepted"}


@router.get("/sample_0")
def get():
    return "success"
