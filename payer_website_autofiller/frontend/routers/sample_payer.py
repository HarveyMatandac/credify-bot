"""Router for sample payer automation"""

from fastapi import APIRouter, HTTPException
from prefect import flow
from prefect.deployments import run_deployment
from patchright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
)
from payer_website_autofiller.bots.sample_payer.sample_website import (
    handler as sample_handler,
)
from payer_website_autofiller.frontend.schemas import (
    ValidationRequest,
    ErrorDetails,
    AutomationResponse,
)

router = APIRouter()
router.base_path = "/sample_payer"


# Prefect flows definition for sample payer automations
@flow
def sample_automation_flow(payload):
    """sample automation flow"""
    sample_handler.Automation.handle(payload)


@router.post("/sample_website", response_model=AutomationResponse)
async def sample_website(payload):
    """Router for sample website automation"""

    try:
        # Run in existing deployment in prefect
        await run_deployment(
            name="sample-automation-flow/sample_website_deployment",
            parameters={"payload": payload},
        )

        return AutomationResponse(
            status="success", message="Automation Successful!"
        )

    except PlaywrightTimeoutError as e:
        raise HTTPException(
            status_code=408,
            detail=AutomationResponse(
                status="error",
                message="Locator(s) was not detected",
                error=ErrorDetails(error_type="Timeout Error", details=str(e)),
            ),
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=AutomationResponse(
                status="error",
                message="Automation Error Occured",
                error=ErrorDetails(
                    error_type="Automation Error", details=str(e)
                ),
            ),
        ) from e
