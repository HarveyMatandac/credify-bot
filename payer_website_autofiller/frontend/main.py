"""Application main function"""

from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from payer_website_autofiller.core.exceptions import register_exception_handlers
from payer_website_autofiller.frontend.routers import all_routers
from payer_website_autofiller.db.database import Base, engine

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

# Register FastAPI exceptions for all routes
register_exception_handlers(app)


# Loop all routers of router folder
for router in all_routers:
    base_path = router.base_path  # type: ignore[attr-defined]
    payer_name = base_path.strip("/")

    app.include_router(
        router,
        prefix=f"/api/bots{base_path}",
        tags=[payer_name.title() + " bots"],
    )
