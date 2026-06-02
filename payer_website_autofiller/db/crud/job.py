"""Module for job related database functions functions"""

from payer_website_autofiller.db.database import SessionLocal
from payer_website_autofiller.db.models import Job
from payer_website_autofiller.core import exceptions as exc


def get_db():
    """Yield database connection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_job(db, job_id, run_id: str, status: str):
    job = Job(job_id=job_id, run_id=run_id, status=status)
    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_job(db, job_id):
    job = db.query(Job).filter(Job.job_id == job_id).first()

    if job is None:
        raise exc.JobNotFoundException(job_id)
    return


def update_job_by_job_id(db, job_id, status, run_id=None):
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        return None

    job.status = status
    if run_id:
        job.run_id = str(run_id)

    db.commit()
    db.refresh(job)


def delete_job(db, job_id):
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        raise exc.JobNotFoundException(job_id)

    db.delete(job)
    db.commit()

    return job


def update_job_on_run_state(_, flow_run, state):
    """Prefect hook function for updating state in database realtime"""
    with SessionLocal() as db:
        job_id = flow_run.parameters.get("job_id")

        update_job_by_job_id(db, str(job_id), state, str(flow_run.id))
