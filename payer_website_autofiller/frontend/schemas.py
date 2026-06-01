"""Module containing all schemas"""

from typing import Annotated, Literal, Dict, Any
from pydantic import BaseModel, Field, EmailStr, field_validator
from payer_website_autofiller.core import const

payer_list = const.SAMPLE_PAYER_LIST


class ProviderInfo(BaseModel):
    """Provider basic info"""

    provider_name: str
    practice_tin: Annotated[str, Field(min_length=9, max_length=12)]
    practice_npi: Annotated[str, Field(min_length=10, max_length=10)]
    provider_npi: Annotated[str, Field(min_length=10, max_length=10)]
    contact_name: str
    contact_email: EmailStr
    telehealth_only: Literal["Yes", "No"] = "No"


class PayerInfo(BaseModel):
    """Payer information"""

    payer: str
    state: str

    @field_validator("payer")
    @classmethod
    def _validate_payer(cls, v: str):
        if v not in payer_list:
            raise ValueError("Payer given is not valid")
        return v


class DataPayload(PayerInfo):
    """Payload schema"""

    fill_values: ProviderInfo
    request_type: Dict[str, Any] | None = None

    model_config = {"extra": "allow"}


class ValidationRequest(BaseModel):
    """JSON data schema"""

    data: DataPayload


# Success model
class SuccessResponse(BaseModel):
    """Success response schema"""

    status: str
    message: str


# Error models
class ErrorDetails(BaseModel):
    """Error details schema"""

    error_type: str
    details: str


class AutomationResponse(SuccessResponse):
    """Automation response schema with error details"""

    details: ErrorDetails | str | None = None
