"""FastAPI Exceptions Modules"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from patchright.sync_api import TimeoutError as PlaywrightTimeoutError
from payer_website_autofiller.frontend.schemas import (
    ErrorDetails,
    AutomationResponse,
)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(PlaywrightTimeoutError)
    async def timeout_handler(request: Request, exc: PlaywrightTimeoutError):
        return JSONResponse(
            status_code=408,
            content=AutomationResponse(
                status="error",
                message="Locator(s) was not detected",
                error=ErrorDetails(
                    error_type="Timeout Error", details=str(exc)
                ),
            ).model_dump(),
        )

    @app.exception_handler(IntegrityError)
    async def integrity_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=409,
            content=AutomationResponse(
                status="error",
                message="duplicate entry",
                error=ErrorDetails(
                    error_type="Automation Error", details=str(exc)
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
                error=ErrorDetails(
                    error_type="Automation Error", details=str(exc)
                ),
            ).model_dump(),
        )
