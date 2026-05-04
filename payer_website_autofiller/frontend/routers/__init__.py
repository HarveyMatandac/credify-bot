"""init module for routers folder"""

from payer_website_autofiller.frontend.routers.humana import (
    router as humana_router,
)

# initialize list of all imported routers
all_routers = [
    humana_router,
]
