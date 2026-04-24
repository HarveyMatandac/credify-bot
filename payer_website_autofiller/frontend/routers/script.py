from payer_website_autofiller.frontend.routers.hmnbhos import handlers
import asyncio


async def main():
    await handlers.adeploy(name="test")


asyncio.run(main())
