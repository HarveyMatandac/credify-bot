import pandas as pd
from pydantic import BaseModel, field_validator
from app.core import const


df = pd.read_csv(const.PAYER_LIST_FILEPATH)
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
