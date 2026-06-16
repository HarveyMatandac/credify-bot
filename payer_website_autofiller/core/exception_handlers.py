"""FastAPI Exceptions Modules"""

# pylint: disable=W0613

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from patchright.sync_api import TimeoutError as PlaywrightTimeoutError
from payer_website_autofiller.frontend.schemas import (
    ErrorDetails,
    AutomationResponse,
)
from payer_website_autofiller.core.exceptions import app_exceptions as app_exc


def register_exception_handlers(app: FastAPI):
    """Register all global exception handlers"""

    @app.exception_handler(PlaywrightTimeoutError)
    async def timeout_handler(request: Request, exc: PlaywrightTimeoutError):
        return JSONResponse(
            status_code=408,
            content=AutomationResponse(
                status="error",
                message="Locator(s) was not detected",
                details=ErrorDetails(
                    error_type="Timeout Error", details=str(exc)
                ),
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def generic_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=AutomationResponse(
                status="error",
                message="Automation Error Occured",
                details=ErrorDetails(
                    error_type="Automation Error", details=str(exc)
                ),
            ).model_dump(),
        )

    @app.exception_handler(app_exc.JobNotFoundException)
    async def job_not_found_handler(
        request: Request, exc: app_exc.JobNotFoundException
    ):
        return JSONResponse(
            status_code=404,
            content=AutomationResponse(
                status="error",
                message="Not found",
                details=f"Job {exc.job_id} not found",
            ).model_dump(),
        )
