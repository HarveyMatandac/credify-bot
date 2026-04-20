from typing import Annotated, Literal, Dict, Any
import pandas as pd
from fastapi import FastAPI
from app.bots.hmnbhos.handler import Automation
from app.routers import all_routers
from app.schemas.base import ValidationRequest


app = FastAPI()

# for router in all_routers:
#     app.include_router(
#         router, prefix=f"/api/bots{router.base_path}", tags=["bots"]
#     )


@app.post("/api")
def fetch_items(payload: ValidationRequest):
    handler = Automation(payload.model_dump())
    handler_response = handler.start()

    return {"status": "accepted", "result": handler_response}
