from fastapi import APIRouter
from prefect import flow, task
from prefect.deployments import run_deployment
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
async def run(payload: ValidationRequest):
    await run_deployment(name="dataloader", parameters={"payload": payload})

    return {"status": "accepted"}


@router.get("/sample_0")
def get():
    return "success"
