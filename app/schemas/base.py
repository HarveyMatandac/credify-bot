from typing import Dict, Any
from pydantic import BaseModel
from app.schemas.payer import PayerInfo
from app.schemas.provider import ProviderInfo


# Temporary dito muna
class DataPayload(PayerInfo):
    fill_values: ProviderInfo
    request_type: Dict[str, Any] | None = None

    model_config = {"extra": "allow"}


class ValidationRequest(BaseModel):
    data: DataPayload
