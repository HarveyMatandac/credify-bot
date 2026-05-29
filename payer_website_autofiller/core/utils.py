"""Common utils module"""

import os
import json
import hashlib
from contextlib import contextmanager
from patchright.sync_api import sync_playwright
from pyvirtualdisplay import Display
from payer_website_autofiller.db.database import SessionLocal
from payer_website_autofiller.db.models import Job


@contextmanager
def get_virtual_display():
    """PyVirtualDisplay context manager"""
    os.environ["PYVIRTUALDISPLAY_DISPLAYFD"] = "0"
    display = Display(visible=True, backend="xvfb")

    display.start()

    print("display start")
    try:
        yield display
    finally:
        display.stop()
        print("display stopped")


@contextmanager
def get_sync_browser_context():
    """Patchright browser context manager"""

    recording_directory = os.path.join(os.getcwd(), "videos")
    print("recording directory: " + str(recording_directory))
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(record_video_dir=recording_directory)
        try:
            yield context
        finally:
            context.close()
            print("context closed")
            browser.close()
            print("browser closed")


def parse_payload(payload):
    json_string = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    hash_object = hashlib.sha256(json_string.encode("utf-8")).hexdigest()

    return hash_object


# Database methods and functions
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
    return db.query(Job).filter(Job.job_id == job_id).first()


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
        return None

    db.delete(job)
    db.commit()

    return job


def update_job_on_run_state(_, flow_run, state):
    """Prefect hook function for updating state in database realtime"""
    with SessionLocal() as db:
        job_id = flow_run.parameters.get("job_id")

        update_job_by_job_id(db, str(job_id), state, str(flow_run.id))
