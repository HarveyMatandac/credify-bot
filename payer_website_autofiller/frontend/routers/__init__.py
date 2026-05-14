"""init module for routers folder"""

from payer_website_autofiller.frontend.routers.humana import (
    router as humana_router,
)

# To be removed
from payer_website_autofiller.frontend.routers.sample_payer import (
    router as sample_payer_router,
)

# initialize list of all imported routers
all_routers = [
    humana_router,
    sample_payer_router,
]
