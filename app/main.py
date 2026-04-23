"""Application main function"""

from fastapi import FastAPI
from app.routers import all_routers


app = FastAPI()

for router in all_routers:
    app.include_router(
        router, prefix=f"/api/bots{router.base_path}", tags=["bots"]
    )
