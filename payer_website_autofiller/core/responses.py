"""Module for common HTTP responses"""

from fastapi import status
from fastapi.responses import JSONResponse


class JobCreatedResponse(JSONResponse):
    def __init__(
        self,
        job_id,
    ):
        super().__init__(
            status_code=status.HTTP_201_CREATED,
            content={
                "status": status.HTTP_201_CREATED,
                "message": "Job have been created. Automation has started",
                "job_id": job_id,
                # "payer_name": "",
                # ...
            },
        )


class DuplicateJobAcceptedResponse(JSONResponse):
    def __init__(
        self,
        job_id,
    ):
        # Insert db get method here
        super().__init__(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                "status": status.HTTP_202_ACCEPTED,
                "message": "This request already exists",
                "job_id": job_id,
                # "job_status": "",
                # ...
            },
        )
