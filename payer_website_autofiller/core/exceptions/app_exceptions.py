"""Module for app related custom exceptions"""

# pylint: disable=W0613

from fastapi import HTTPException, status


class AppError(HTTPException):
    """Base class for all app related errors"""

    def __init__(self, status_code, detail):
        super().__init__(
            status_code=status_code,
            detail=detail,
        )


class JobNotFoundException(Exception):
    """Exception for if job is not found in database"""

    def __init__(self, job_id: str):
        self.job_id = job_id


class RequestDuplicateEntryError(HTTPException):
    """_summary_

    Args:
        HTTPException (_type_): _description_
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "Existing Request",
                "message": "Revise payload required",
            },
        )


class FlowRunIsNoneError(AppError):
    def __init__(self, job_id):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "Prefect deployment dispatch failed",
                "job": job_id,
            },
        )


class EndpointNotValidError(HTTPException):
    def __init__(self, endpoint_url):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": f"Route '{endpoint_url}' not supported",
                "message": "Input correct endpoint url",
            },
        )
