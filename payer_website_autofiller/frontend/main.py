"""Application main function"""

from fastapi import FastAPI
from payer_website_autofiller.frontend.routers import all_routers

app = FastAPI()

# Loop all routers of router folder
for router in all_routers:
    base_path = router.base_path.strip("/")  # type: ignore[attr-defined]
    payer_name = base_path

    app.include_router(
        router,
        prefix=f"/api/bots{base_path}",
        tags=[payer_name.title() + " bots"],
    )
