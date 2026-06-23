"""Module for common HTTP responses"""

from fastapi import status
from fastapi.responses import JSONResponse
from payer_website_autofiller.db.models import Job


class RequestCreatedResponse(JSONResponse):
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


class JobRequestedResponse(JSONResponse):
    def __init__(
        self,
        job: Job,
    ):
        super().__init__(
            status_code=status.HTTP_200_OK,
            content={
                "status": status.HTTP_200_OK,
                "message": "Request found",
                "job_id": job.job_id,
                "job_status": job.status,
            },
        )


class JobDeletedResponse(JSONResponse):
    def __init__(
        self,
        job: Job,
    ):
        super().__init__(
            status_code=status.HTTP_200_OK,
            content={
                "status": status.HTTP_200_OK,
                "message": "Request Deleted",
                "job_id": job.job_id,
                "job_status": job.status,
            },
        )


class RequestNotFound(JSONResponse):
    def __init__(self, job_id):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Request Not Found",
                "job_id": job_id,
            },
        )


class RequestAlreadySubmittedResponse(JSONResponse):
    def __init__(
        self,
        job: Job,
    ):
        # Insert db get method here
        super().__init__(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                "status": status.HTTP_202_ACCEPTED,
                "message": "This request already exists",
                "job_id": job.job_id,
                "job_status": job.status,
                # ...
            },
        )


class PrefectDeploymentErrorResponse(JSONResponse):
    def __init__(self, job_id):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": status.HTTP_503_SERVICE_UNAVAILABLE,
                "message": "Prefect deployment dispatch failed",
                "job_id": job_id,
            },
        )


class EndpointNotValidResponse(JSONResponse):
    def __init__(self, endpoint_url):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": status.HTTP_404_NOT_FOUND,
                "message": f"Route '{endpoint_url}' not supported",
            },
        )


class InternalServerErrorResponse(JSONResponse):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": (
                    "An unexpected error occurred. Please try again later."
                ),
            },
        )
