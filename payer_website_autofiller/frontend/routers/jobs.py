from fastapi import APIRouter, HTTPException
from payer_website_autofiller.frontend.db.database import redis_client

router = APIRouter()
router.base_path = "/jobs"


@router.get("/{job_id}")
def get_job(job_id):
    data = redis_client.hgetall(f"job:{job_id}")

    if not data:
        raise HTTPException(status_code=404, detail="Job not found")

    return data


# @router.get("/all_jobs")
# def get_job(job_id):
#     data = redis_client.hgetall(f"job:{job_id}")

#     if not data:
#         raise HTTPException(status_code=404, detail="Job not found")

#     return data
