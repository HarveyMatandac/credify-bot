from fastapi import APIRouter, BackgroundTasks
from app.bots.hmnbhos.handler import Automation
from app.schemas import ValidationRequest
from app.dependencies import JobLogger

router = APIRouter()
router.base_path = "/hmnbhos"


@router.post("/", status_code=202)
async def run(payload: ValidationRequest, background_tasks: BackgroundTasks):
    job_id = "j123"

    JobLogger().create_job(job_id)

    handler = Automation(payload.model_dump())
    background_tasks.add_task(handler.start, job_id, False)

    return {"job_id": job_id, "status": "accepted"}


@router.get("/sample_0")
def get():
    return "success"
