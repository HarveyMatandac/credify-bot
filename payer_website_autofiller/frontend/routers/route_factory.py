"""Module containing route factory for common provider automations"""

from prefect.deployments import run_deployment
from payer_website_autofiller.frontend.schemas import ValidationRequest


def make_handler(automation_class):
    async def _run_handler(payload: ValidationRequest):
        await run_deployment(
            name="dataloader",
            parameters={
                "payload": payload,
                "automation_class": automation_class,
            },
        )

        return {"status": "accepted"}

    return _run_handler
