"""Application main function"""

from fastapi import FastAPI
from payer_website_autofiller.frontend.routers import all_routers

app = FastAPI()

for router in all_routers:
    payer_name = router.base_path.strip("/")

    app.include_router(
        router,
        prefix=f"/api/bots{router.base_path}",
        tags=[payer_name.title() + " bots"],
    )
