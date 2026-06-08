"""Router for catch_all endpoint"""

import enum
from fastapi import APIRouter, HTTPException
from payer_website_autofiller.frontend.schemas import EndpointNotValidError

router = APIRouter()
router.prefix = "/api"


class SupportedPayer(str, enum.Enum):
    """Enum for available supported payers"""

    HUMANA = "humana"
    SAMPLE_PAYER = "sample_payer"


# Verification function
@router.post("/{payer}/{provider_type}")
async def url_format_verifier(payer: SupportedPayer, provider_type):
    """Route for checking url parameters"""

    # Endpoint URL for raised exception detail
    endpoint_url = f"{router.prefix}/{payer.value}/{provider_type}"

    # Raise error not found http exception
    raise EndpointNotValidError(endpoint_url)
