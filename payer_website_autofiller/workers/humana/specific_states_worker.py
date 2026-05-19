"""Worker for Humana Behavioral Health Prefect flow"""

from prefect.types.entrypoint import EntrypointType
from payer_website_autofiller.frontend.routers.humana import (
    humana_automations_flow as run_bot,
)


def _dataloader():
    run_bot.serve(
        "humana-specific-states",
        entrypoint_type=EntrypointType.MODULE_PATH,
        print_starting_message=False,
    )


if __name__ == "__main__":
    _dataloader()
