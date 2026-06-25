"""Module for app related custom exceptions"""

# pylint: disable=W0613


class FlowRunIsNoneError(Exception):
    def __init__(self, job_id):
        self.job_id = job_id


class EndpointNotValidError(Exception):
    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url


class JobNotFoundException(Exception):
    """Exception for if job is not found in database"""

    def __init__(self, job_id: str):
        self.job_id = job_id
