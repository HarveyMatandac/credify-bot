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
from patchright.sync_api import TimeoutError
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


class AutomationError(Exception):
    """Base class for all automation-related errors

    Args:
        Exception (_type_): Exception Base Class
    """

    def __init__(
        self,
        message: str,
        automation_name: str,
        step: str | None = None,
        context: dict | None = None,
    ):

        # Copy inherited parameters
        super().__init__(message)

        self.automation_name = automation_name
        self.step = step
        self.context = context or {}

    # Modify inherited __str__ function
    def __str__(self):
        # Call parent __str__ object
        base_err_message = super().__str__()

        if self.step:
            return (
                f"{base_err_message} (automation={self.automation_name}, "
                "step={self.step})"
            )

        return base_err_message

    def to_dict(self):
        """Function of AutomationError to return a dictionary"""
        return {
            "error": str(self),
            "step": self.step,
            "context": self.context,
        }


class NavigationError(AutomationError):
    """Automation error subclass for URL not found"""

    def __init__(
        self,
        url: str,
        automation_name: str,
        step: str | None = None,
    ):
        super().__init__(
            message=f"Failed to navigate to url {url}",
            automation_name=automation_name,
            step=step,
            context={"url": url},
        )


class LocatorNotFoundError(Exception):
    def __init__(self, message="Locator not found"):
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(message)


class PlaywrightTimeoutError(TimeoutError):
    def __init__(self, message="Locator did not appear within timeout"):
        self.status_code = status.HTTP_408_REQUEST_TIMEOUT
        super().__init__(message)


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
