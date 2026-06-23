"""Router for sample payer automation"""

from fastapi import APIRouter, Depends
from prefect import flow
from payer_website_autofiller.core.utils import start_automation, parse_payload
from payer_website_autofiller.db.crud.job import (
    get_db,
    get_job,
    create_job,
    update_job_on_run_state,
    delete_job,
)
from payer_website_autofiller.bots.sample_payer.sample_website import (
    handler as sample_handler,
)
from payer_website_autofiller.frontend.schemas import (
    Payload,
)
from payer_website_autofiller.core.exceptions import (
    app_exceptions,
)
from payer_website_autofiller.core import responses

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
def sample_automation_flow(
    payload,
    provider_type,
):
    """sample automation flow"""
    match provider_type:
        case "sample_website":
            sample_handler.Automation(payload).handle()


@router.get("/sample_website/get/{job_id}")
def read_sample_website_job(job_id: str, conn=Depends(get_db)):
    """Sample Website GET method"""
    job = get_job(conn, job_id)

    if job is None:
        raise app_exceptions.JobNotFoundException(job_id)

    return responses.JobRequestedResponse(job)


@router.get("/sample_website/get/{payer}")
def get_sample_website_jobs_by_payer(payer: str, conn=Depends(get_db)):
    pass


@router.post("/sample_website")
def create_sample_website_job(
    payload: Payload,
    conn=Depends(get_db),
):
    """Router for sample website automation and job creation"""

    job_id = parse_payload(payload)

    # Check if job_id already exists
    job = get_job(conn, job_id)
    if job:
        return responses.RequestAlreadySubmittedResponse(job)

    # Start automation
    flow_run = start_automation(
        payload,
        "sample_website",
        conn,
        "sample-automation-flow/sample_website_deployment",
    )

    create_job(conn, job_id, flow_run)

    return responses.RequestCreatedResponse(job_id)


@router.delete("/sample_website/delete/{job_id}")
def delete_sample_website_job(job_id: str, conn=Depends(get_db)):
    """Sample Website DELETE endpoint"""
    job = get_job(conn, job_id)
    if job is None:
        raise app_exceptions.JobNotFoundException(job_id)

    response = responses.JobDeletedResponse(job)
    delete_job(conn, job_id)
    return response


@router.delete("/sample_website/delete/{payer}")
def delete_sample_website_jobs_by_payer():
    pass


@router.delete("/sample_website/delete/{status}")
def delete_sample_website_jobs_by_status():
    pass
