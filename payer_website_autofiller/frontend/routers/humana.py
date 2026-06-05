"""Humana routers module"""

from fastapi import APIRouter, Depends, HTTPException
from prefect import flow
from prefect.deployments import run_deployment
from payer_website_autofiller.bots.humana.behavioral_health import (
    handler as bh_handler,
)
from payer_website_autofiller.bots.humana.specific_states import (
    handler as ss_handler,
)
from payer_website_autofiller.frontend.schemas import (
    # ValidationRequest,
    AutomationResponse,
)
from payer_website_autofiller.db.crud.job import (
    get_db,
    get_job,
    update_job_on_run_state,
    delete_job,
)
from payer_website_autofiller.core.utils import (
    start_automation,
)

router = APIRouter()
router.base_path = "/humana"  # type: ignore[attr-defined]


# Prefect flows definition for Humana automations
@flow(
    on_running=[update_job_on_run_state],
    on_completion=[update_job_on_run_state],
    on_failure=[update_job_on_run_state],
    on_crashed=[update_job_on_run_state],
    on_cancellation=[update_job_on_run_state],
)
def humana_automations_flow(payload, provider_type):
    """Humana automation flows"""
    match provider_type:
        case "behavioral_health":
            automation = bh_handler.Automation(payload)
        case "specific_states":
            automation = ss_handler.Automation(payload)

    automation.handle()


@router.get("/behavioral_health/{job_id}")
def read_behavioral_health_job(job_id: str, conn=Depends(get_db)):
    """Sample Website GET method"""
    job = get_job(conn, job_id)

    return {job.job_id, job.run_id, job.status}


@router.post("/behavioral_health", response_model=AutomationResponse)
async def create_behavioral_health_job(payload, conn=Depends(get_db)):
    """Router for Behavioral Health automation"""

    # Start website automation
    result = start_automation(
        payload=payload,
        provider_type="behavioral_health",
        db=conn,
        deployment_name="sample-automation-flow/sample_website_deployment",
    )

    if result:
        raise HTTPException(
            status_code=409,
            detail=AutomationResponse(
                status="error",
                message="duplicate entry",
                details=f"Job '{result.job_id}' already exists",
            ).model_dump(),
        )

    return AutomationResponse(
        status="success", message="Automation Successful!"
    )


@router.delete("/behavioral_health/{job_id}")
def delete_behavioral_health_job(job_id: str, conn=Depends(get_db)):
    """Sample Webiste DELETE endpoint"""
    job = delete_job(conn, job_id)

    return {"deleted": job.job_id}


@router.get("/specific_states/{job_id}")
def read_specific_states_job(job_id: str, conn=Depends(get_db)):
    """Sample Website GET method"""
    job = get_job(conn, job_id)

    return {job.job_id, job.run_id, job.status}


@router.post("/specific_states", response_model=AutomationResponse)
async def create_specific_states_job(payload):
    """Router for Specific States automation"""
    await run_deployment(
        name="humana-automations-flow/humana-specific-states",
        parameters={
            "payload": payload,
            "provider_type": "specific_states",
        },
    )  # type: ignore

    return {"status": "accepted"}


@router.delete("/specific_states/{job_id}")
def delete_specific_states_job(job_id: str, conn=Depends(get_db)):
    """Sample Webiste DELETE endpoint"""
    job = delete_job(conn, job_id)

    return {"deleted": job.job_id}
