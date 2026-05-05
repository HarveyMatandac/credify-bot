from prefect.types.entrypoint import EntrypointType
from payer_website_autofiller.frontend.routers.hmnbhos import (
    handlers as run_bot,
)


def dataloader():
    run_bot.serve(
        "dataloader",
        entrypoint_type=EntrypointType.MODULE_PATH,
        print_starting_message=False,
    )


dataloader()
