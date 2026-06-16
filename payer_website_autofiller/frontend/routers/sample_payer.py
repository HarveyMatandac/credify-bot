"""Router for sample payer automation"""

from fastapi import APIRouter, Depends
from prefect import flow
from payer_website_autofiller.core.utils import start_automation, parse_payload
from payer_website_autofiller.db.crud.job import (
    get_db,
    get_job,
    create_job,
    # update_job_on_run_state,
    delete_job,
)
from payer_website_autofiller.bots.sample_payer.sample_website import (
    handler as sample_handler,
)
from payer_website_autofiller.frontend.schemas import (
    Payload,
)
from payer_website_autofiller.core.exceptions.automation_exceptions import (
    AutomationError,
)
from payer_website_autofiller.core import responses
from sqlalchemy.exc import IntegrityError

router = APIRouter()
router.base_path = "/sample_payer"  # type: ignore[attr-defined]


# Prefect flows definition for sample payer automations
@flow(
    #     on_running=[update_job_on_run_state],
    #     on_completion=[update_job_on_run_state],
    #     on_failure=[update_job_on_run_state],
    #     on_crashed=[update_job_on_run_state],
    #     on_cancellation=[update_job_on_run_state],
)
def sample_automation_flow(
    payload,
    provider_type,
    job_id=None,  # pylint: disable=W0613
):
    """sample automation flow"""
    try:
        match provider_type:
            case "sample_website":
                sample_handler.Automation(payload).handle()
    except AutomationError as e:
        # raise HTTP exception here
        print(e)


@router.get("/sample_website/{job_id}")
def read_sample_website_job(job_id: str, conn=Depends(get_db)):
    """Sample Website GET method"""
    job = get_job(conn, job_id)

    return {job.job_id, job.run_id, job.status}


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
        return responses.DuplicateJobAcceptedResponse(job_id)

    # Start automation
    flow_run = start_automation(
        payload,
        "sample_website",
        conn,
        "sample-automation-flow/sample_website_deployment",
    )

    create_job(conn, job_id, flow_run)

    return responses.JobCreatedResponse(job_id)


@router.delete("/sample_website/{job_id}")
def delete_sample_website_job(job_id: str, conn=Depends(get_db)):
    """Sample Webiste DELETE endpoint"""
    job = delete_job(conn, job_id)

    return {"deleted": job.job_id}
