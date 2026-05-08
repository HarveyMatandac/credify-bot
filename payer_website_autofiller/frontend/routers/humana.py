"""Humana routers module"""

from fastapi import APIRouter
from prefect import flow, task
from prefect.deployments import run_deployment
from payer_website_autofiller.bots.humana.behavioral_health import (
    handler as bh_handler,
)
from payer_website_autofiller.bots.humana.specific_states import (
    handler as ss_handler,
)
from payer_website_autofiller.frontend.schemas import ValidationRequest

router = APIRouter()
router.base_path = "/humana"


# Prefect tasks definitions for Humana automations
@task
def run_behavioral_health_automation(payload):
    """Behavioral Health automation task"""
    automation = bh_handler.Automation(payload)
    result = automation.handle()
    return result


@task
def run_specific_states_automation(payload):
    """Specific States automation task"""
    automation = ss_handler.Automation(payload)
    result = automation.handle()
    return result


# Prefect flows definition for Humana automations
@flow
def humana_automations_flow(payload, sub_type):
    """Humana automation flows"""
    match sub_type:
        case "behavioral_health":
            run_behavioral_health_automation(payload)
        case "specific_states":
            run_specific_states_automation(payload)


@router.post("/behavioral_health/", status_code=202)
async def behavioral_health_endpoint(payload: ValidationRequest):
    """Router for Behavioral Health automation"""
    await run_deployment(
        name="humana-automations-flow/humana-behavioral-health",
        parameters={
            "payload": payload,
            "sub_type": "behavioral_health",
        },
    )

    return {"status": "accepted"}


@router.post("/specific_states/", status_code=202)
async def specific_states_endpoint(payload: ValidationRequest):
    """Router for Specific States automation"""
    await run_deployment(
        name="humana-automations-flow/humana-specific-states",
        parameters={
            "payload": payload,
            "sub_type": "specific_states",
        },
    )

    return {"status": "accepted"}
