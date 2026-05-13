from typing import Annotated, Literal, Dict, Any, Optional
from pydantic import BaseModel, Field, EmailStr, field_validator
from payer_website_autofiller.core import const

payer_list = const.SAMPLE_PAYER_LIST


class ProviderInfo(BaseModel):
    provider_name: str
    practice_tin: Annotated[str, Field(min_length=9, max_length=12)]
    practice_npi: Annotated[str, Field(min_length=10, max_length=10)]
    provider_npi: Annotated[str, Field(min_length=10, max_length=10)]
    contact_name: str
    contact_email: EmailStr
    telehealth_only: Literal["Yes", "No"] = "No"


class PayerInfo(BaseModel):
    payer: str
    state: str

    @field_validator("payer")
    @classmethod
    def validate_payer(cls, v: str):
        if v not in payer_list:
            raise ValueError("Payer given is not valid")
        return v


class DataPayload(PayerInfo):
    fill_values: ProviderInfo
    request_type: Dict[str, Any] | None = None

    model_config = {"extra": "allow"}


class ValidationRequest(BaseModel):
    data: DataPayload


# Success model
class SuccessResponse(BaseModel):
    status: str
    message: str


# Error models
# Pede enums dito para mas mahigpit error type
class ErrorDetails(BaseModel):
    error_type: str
    details: str


class AutomationResponse(SuccessResponse):
    error: Optional[ErrorDetails] = None
