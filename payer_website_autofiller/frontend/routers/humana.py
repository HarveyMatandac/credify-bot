from fastapi import APIRouter
from prefect import flow, task
from prefect.deployments import run_deployment
from payer_website_autofiller.bots.hmnbhos import handler as hmnbhos_handler
from payer_website_autofiller.bots.hmnss import handler as hmnss_handler
from payer_website_autofiller.frontend.schemas import ValidationRequest

router = APIRouter()
router.base_path = "/humana"

AUTOMATIONS = {
    "behavioral-health": hmnbhos_handler.Automation,
    "specific-state": hmnss_handler.Automation,
}


@task
def run_automation(payload, handler_type):
    handler_class = AUTOMATIONS.get(handler_type)
    handler = handler_class(payload)
    with handler.start():
        pass


@flow
def handlers(payload):
    run_automation(payload, "behavioral-health")


@router.post("/behavioral_health/", status_code=202)
async def run_behavioral_health(payload: ValidationRequest):
    await run_deployment(
        name="handlers/dataloader", parameters={"payload": payload}
    )

    return {"status": "accepted"}


@router.post("/specific_states/", status_code=202)
# async
def run_specific_states(payload: ValidationRequest):

    # await run_deployment(name="dataloader", parameters={"payload": payload})

    # For debugging
    run_automation(payload, "specific-state")

    return {"status": "accepted"}
