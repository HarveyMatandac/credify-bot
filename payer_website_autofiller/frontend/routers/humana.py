"""Humana routers module"""

from fastapi import APIRouter, HTTPException
from prefect import flow, task
from prefect.deployments import run_deployment
from patchright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
)
from payer_website_autofiller.bots.humana.behavioral_health import (
    handler as bh_handler,
)
from payer_website_autofiller.bots.humana.specific_states import (
    handler as ss_handler,
)
from payer_website_autofiller.frontend.schemas import (
    ValidationRequest,
    ErrorDetails,
    AutomationResponse,
)

router = APIRouter()
router.base_path = "/humana"  # type: ignore[attr-defined]


# Prefect tasks definitions for Humana automations
@task
def run_behavioral_health_automation(payload):
    """Behavioral Health automation task"""
    automation = bh_handler.Automation(payload)
    automation.handle()


@task
def run_specific_states_automation(payload):
    """Specific States automation task"""
    automation = ss_handler.Automation(payload)
    automation.handle()


# Prefect flows definition for Humana automations
@flow
def humana_automations_flow(payload, sub_type):
    """Humana automation flows"""
    match sub_type:
        case "behavioral_health":
            run_behavioral_health_automation(payload)
        case "specific_states":
            run_specific_states_automation(payload)


@router.post("/behavioral_health/", response_model=AutomationResponse)
async def behavioral_health_endpoint(payload: ValidationRequest):
    """Router for Behavioral Health automation"""

    try:
        # Run in existing deployment in prefect
        await run_deployment(
            name="humana-automations-flow/humana-behavioral-health",
            parameters={
                "payload": payload,
                "sub_type": "behavioral_health",
            },
        )  # type: ignore

        return AutomationResponse(
            status="success", message="Automation Successful!"
        )

    except PlaywrightTimeoutError as e:
        raise HTTPException(
            status_code=408,
            detail=AutomationResponse(
                status="error",
                message="Locator(s) was not detected",
                details=ErrorDetails(
                    error_type="Timeout Error", details=str(e)
                ),
            ),
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            details=AutomationResponse(
                status="error",
                message="Automation Error Occured",
                error=ErrorDetails(
                    error_type="Automation Error", details=str(e)
                ),
            ),
        ) from e


@router.post("/specific_states/", response_model=AutomationResponse)
async def specific_states_endpoint(payload: ValidationRequest):
    """Router for Specific States automation"""
    await run_deployment(
        name="humana-automations-flow/humana-specific-states",
        parameters={
            "payload": payload,
            "sub_type": "specific_states",
        },
    )  # type: ignore

    return {"status": "accepted"}
