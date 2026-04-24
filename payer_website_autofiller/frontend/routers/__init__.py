"""init module for routers folder"""

from payer_website_autofiller.frontend.routers.jobs import router as job_router
from payer_website_autofiller.frontend.routers.hmnbhos import (
    router as hmnbhos_router,
)


# initialize list of all imported routers
all_routers = [
    job_router,
    hmnbhos_router,
]
