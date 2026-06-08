"""Module containing all schemas"""

from typing import Optional, Annotated, Literal, Dict, Any
from fastapi import HTTPException, status
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator,
    StringConstraints,
)
from payer_website_autofiller.core import const

payer_list = const.SAMPLE_PAYER_LIST


class EnrollmentData(BaseModel):
    type: Literal["individual", "group"]
    specialty: str
    enrollment_status: str


class NameInfo(BaseModel):
    """Provider Name Model"""

    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    suffix: Optional[str] = None


class ContactInfo(BaseModel):
    """Contact Info of provider model"""

    mobile_number: Optional[str] = None
    telephone_number: Optional[str] = None
    email: EmailStr


class IdentificationNumbers(BaseModel):
    """Model for validating Identification numbers like tin and NPI"""

    tin: Annotated[str, Field(min_length=9, max_length=12)]
    npi: Annotated[str, Field(min_length=10, max_length=10)]


class AddressInfo(BaseModel):
    unit: Optional[str] = None
    building: Optional[str] = None
    street: Optional[str] = None
    city: str
    county: Optional[str] = None
    state: Optional[str] = None
    zip_code: Annotated[str, StringConstraints(pattern=r"^\d{3,10}$")]
    country: str


class BasicInfo(BaseModel):
    """Provider basic info"""

    name: NameInfo
    contact_info: ContactInfo
    identification_numbers: IdentificationNumbers
    address: AddressInfo


class ProviderData(BaseModel):
    enrollment_data: EnrollmentData
    basic_info: BasicInfo

    model_config = {"extra": "allow"}


class Payload(BaseModel):
    provider_data: ProviderData


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


class EndpointNotValidError(HTTPException):
    def __init__(self, endpoint_url):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": f"Route '{endpoint_url}' not supported",
                "message": "Input correct endpoint url",
            },
        )


class AutomationResponse(SuccessResponse):
    """Automation response schema with error details"""

    details: ErrorDetails | str | None = None
