from app.db.database import redis_client


class JobLogger:
    def create_job(self, job_id):
        redis_client.hset(
            f"job:{job_id}",
            mapping={
                "status": "pending",
                "error": "",
            },
        )

    def update_job(self, job_id, status, error=""):
        redis_client.hset(
            f"job:{job_id}",
            mapping={
                "status": status,
                "error": error,
            },
        )
