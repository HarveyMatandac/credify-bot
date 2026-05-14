"""Worker for the sample payer website form"""

from prefect.types.entrypoint import EntrypointType
from payer_website_autofiller.frontend.routers.sample_payer import (
    sample_automation_flow as run_bot,
)


def dataloader():
    run_bot.serve(
        "sample_website_deployment",
        entrypoint_type=EntrypointType.MODULE_PATH,
        print_starting_message=False,
    )


if __name__ == "__main__":
    dataloader()
