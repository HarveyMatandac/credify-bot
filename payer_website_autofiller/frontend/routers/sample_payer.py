"""Router for sample payer automation"""

from fastapi import APIRouter, Depends, HTTPException
from prefect import flow
from prefect.client.schemas import FlowRun
from payer_website_autofiller.core.utils import start_automation, parse_payload
from payer_website_autofiller.db.crud.job import (
    get_db,
    get_job,
    update_job_on_run_state,
    delete_job,
)
from payer_website_autofiller.bots.sample_payer.sample_website import (
    handler as sample_handler,
)
from prefect.deployments import run_deployment
from payer_website_autofiller.frontend.schemas import (
    Payload,
    AutomationResponse,
    AutomationError,
    RequestDuplicateEntryError,
)

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

    run_deployment(
        name="sample-automation-flow/sample_website_deployment",
        parameters={
            "payload": payload,
            "provider_type": "sample_website",
        },
        # timeout=0,
    )

    # assert isinstance(flow_run, FlowRun)

    return {
        "job_id": job_id,
    }


@router.delete("/sample_website/{job_id}")
def delete_sample_website_job(job_id: str, conn=Depends(get_db)):
    """Sample Webiste DELETE endpoint"""
    job = delete_job(conn, job_id)

    return {"deleted": job.job_id}
