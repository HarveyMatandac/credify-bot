"""Router for sample payer automation"""

from fastapi import APIRouter, HTTPException, Body, Depends
from prefect import flow
from prefect.deployments import run_deployment
from sqlalchemy.exc import IntegrityError
from patchright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
)
from payer_website_autofiller.core.utils import (
    get_db,
    create_job,
    get_job,
    update_job_by_job_id,
    delete_job,
    update_job_on_run_state,
    parse_payload,
)
from payer_website_autofiller.bots.sample_payer.sample_website import (
    handler as sample_handler,
)
from payer_website_autofiller.frontend.schemas import (
    ErrorDetails,
    AutomationResponse,
)

router = APIRouter()
router.base_path = "/sample_payer"  # type: ignore[attr-defined]


# Prefect flows definition for sample payer automations
@flow(
    on_running=[update_job_on_run_state],
    on_completion=[update_job_on_run_state],
    on_failure=[update_job_on_run_state],
    on_crashed=[update_job_on_run_state],
    on_cancellation=[update_job_on_run_state],
)
def sample_automation_flow(payload, job_id=None):
    """sample automation flow"""
    sample_handler.Automation(payload).handle()


@router.get("/sample_website/{job_id}")
def read_sample_website_job(job_id: str, conn=Depends(get_db)):
    job = get_job(conn, job_id)

    return {job.job_id, job.run_id, job.status}


@router.post("/sample_website/")
def create_sample_website_job(payload: dict = Body(...), conn=Depends(get_db)):
    """Router for sample website automation"""

    # Hash request parameters
    job_id = parse_payload(payload)

    create_job(conn, job_id, "", status="Created")

    # Run in existing deployment in prefect
    run_deployment(
        name="sample-automation-flow/sample_website_deployment",
        parameters={"payload": payload, "job_id": job_id},
    )

    return AutomationResponse(
        status="success", message="Automation Successful!"
    )


@router.put("/sample_website/{job_id}")
def update_sample_website_job(job_id: str, state: str, conn=Depends(get_db)):
    update_job_by_job_id(conn, job_id, state)

    return {"updated": job_id}


@router.delete("/sample_website/{job_id}")
def delete_sample_website_job(job_id: str, conn=Depends(get_db)):
    job = delete_job(conn, job_id)

    return {"deleted": job.job_id}
