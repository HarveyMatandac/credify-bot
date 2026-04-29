"""init module for routers folder"""

from payer_website_autofiller.frontend.routers.hmnbhos import (
    router as hmnbhos_router,
)


# initialize list of all imported routers
all_routers = [
    hmnbhos_router,
]
