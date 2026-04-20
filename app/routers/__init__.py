"""init module for routers folder"""

from app.routers.hmnbhos import router as hmnbhos_router


# initialize list of all imported routers
all_routers = [hmnbhos_router]
