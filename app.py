from typing import Annotated, Literal, Dict, Any
import pandas as pd
from fastapi import FastAPI
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator,
)

PAYER_LIST_FILEPATH = "payers_list.csv"

api = FastAPI()

df = pd.read_csv(PAYER_LIST_FILEPATH)
payer_list = df["Payers"].dropna().astype(str).unique().tolist()


class PayerInfo(BaseModel):
    payer: str
    state: str

    @field_validator("payer")
    @classmethod
    def validate_payer(cls, v: str):
        if v not in payer_list:
            raise ValueError("Payer given is not valid")
        return v


class BasicInfo(BaseModel):
    provider_name: str
    practice_tin: Annotated[str, Field(min_length=9, max_length=12)]
    practice_npi: Annotated[str, Field(min_length=10, max_length=10)]
    provider_npi: Annotated[str, Field(min_length=10, max_length=10)]
    contact_name: str
    contact_email: EmailStr
    telehealth_only: Literal["Yes", "No"] = "No"


class DataPayload(PayerInfo):
    fill_values: BasicInfo
    request_type: Dict[str, Any] | None = None

    model_config = {"extra": "allow"}


class ValidationRequest(BaseModel):
    data: DataPayload


# @api.get("/")
# def index():
#     return {"message": "Hello World"}


@api.post("/validation/")
async def fetch_items(_: ValidationRequest):
    return {"status": "ok"}
