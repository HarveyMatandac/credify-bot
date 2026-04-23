"""init module for routers folder"""

from app.routers.jobs import router as jobs_router
from app.routers.hmnbhos import router as hmnbhos_router


# initialize list of all imported routers
all_routers = [
    jobs_router,
    hmnbhos_router,
]
