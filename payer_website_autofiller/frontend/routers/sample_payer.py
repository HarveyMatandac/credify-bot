"""Router for sample payer automation"""

from fastapi import APIRouter, Body, Depends, HTTPException
from prefect import flow
from payer_website_autofiller.core.utils import (
    start_automation,
)
from payer_website_autofiller.db.crud.job import (
    get_db,
    get_job,
    update_job_on_run_state,
    delete_job,
)
from payer_website_autofiller.bots.sample_payer.sample_website import (
    handler as sample_handler,
)
from payer_website_autofiller.frontend.schemas import (
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
def sample_automation_flow(
    payload,
    job_id=None,  # pylint: disable=W0613
):
    """sample automation flow"""
    sample_handler.Automation(payload).handle()


@router.get("/sample_website/{job_id}")
def read_sample_website_job(job_id: str, conn=Depends(get_db)):
    """Sample Website GET method"""
    job = get_job(conn, job_id)

    return {job.job_id, job.run_id, job.status}


@router.post("/sample_website/")
def create_sample_website_job(payload: dict = Body(...), conn=Depends(get_db)):
    """Router for sample website automation and job creation"""

    # Start website automation
    result = start_automation(
        payload=payload,
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


@router.delete("/sample_website/{job_id}")
def delete_sample_website_job(job_id: str, conn=Depends(get_db)):
    """Sample Webiste DELETE endpoint"""
    job = delete_job(conn, job_id)

    return {"deleted": job.job_id}
