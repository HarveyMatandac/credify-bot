"""Common automation module"""

from prefect import flow, task


@task
def run_automation(automation_obj):
    with automation_obj.start():
        pass


@flow
def handler_flow(payload, automation_class):
    run_automation(automation_class(payload))
