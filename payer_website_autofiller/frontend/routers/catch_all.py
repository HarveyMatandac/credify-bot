"""Router for catch_all endpoint"""

import enum
from fastapi import APIRouter, HTTPException

router = APIRouter()
router.prefix = "/api/bots"


class SupportedPayer(str, enum.Enum):
    """Enum for available supported payers"""

    HUMANA = "humana"
    SAMPLE_PAYER = "sample_payer"


@router.post("/{payer}/{provider_type}")
async def catch_all(payer: SupportedPayer, provider_type):
    """Catch_all for unsupported endpoints"""

    # Endpoint URL for raised exception detail
    endpoint_url = f"{router.prefix}/{payer.value}/{provider_type}"

    # Raise error not found http exception
    raise HTTPException(
        status_code=404,
        detail=f"Route '{endpoint_url}' not supported",
    )
