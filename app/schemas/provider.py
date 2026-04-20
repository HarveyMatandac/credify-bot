from typing import Annotated, Literal
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
)


class ProviderInfo(BaseModel):
    provider_name: str
    practice_tin: Annotated[str, Field(min_length=9, max_length=12)]
    practice_npi: Annotated[str, Field(min_length=10, max_length=10)]
    provider_npi: Annotated[str, Field(min_length=10, max_length=10)]
    contact_name: str
    contact_email: EmailStr
    telehealth_only: Literal["Yes", "No"] = "No"
