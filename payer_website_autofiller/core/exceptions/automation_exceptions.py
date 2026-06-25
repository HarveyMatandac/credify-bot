"""Module for automation related custom exceptions"""

from fastapi import status


class AutomationError(Exception):
    """Base class for all automation-related errors

    Args:
        Exception (_type_): Exception Base Class
    """

    def __init__(
        self,
        message: str,
        automation_name: str,
        step: str | None = None,
        context: dict | None = None,
    ):

        # Copy inherited parameters
        super().__init__(message)

        self.automation_name = automation_name
        self.step = step
        self.context = context or {}

    # Modify inherited __str__ function
    def __str__(self):
        # Call parent __str__ object
        base_err_message = super().__str__()

        if self.step:
            return (
                f"{base_err_message} (automation={self.automation_name}, "
                f"step={self.step})"
            )

        return base_err_message

    def to_dict(self):
        """Function of AutomationError to return a dictionary"""
        return {
            "error": str(self),
            "step": self.step,
            "context": self.context,
        }


class NavigationError(AutomationError):
    """Automation error subclass for URL not found"""

    def __init__(
        self,
        url: str,
        automation_name: str,
        step: str | None = None,
    ):
        super().__init__(
            message=f"Failed to navigate to url {url}",
            automation_name=automation_name,
            step=step,
            context={"url": url},
        )


class LocatorNotFoundError(AutomationError):
    """A locator matched zero (or ambiguous) elements — the page layout changed."""

    def __init__(
        self,
        automation_name,
        step=None,
    ):
        super().__init__(
            message="Element was not found on the page",
            automation_name=automation_name,
            step=step,
        )


class PlaywrightTimeoutError(AutomationError):
    """Expected element never appeared / became interactable within the timeout."""

    def __init__(
        self,
        automation_name,
        step=None,
    ):
        super().__init__(
            message="Element did not appear or become interactable in time",
            automation_name=automation_name,
            step=step,
        )


class DataExtractionError(AutomationError):
    """Raised when a required field is missing from the payload."""

    def __init__(
        self,
        field,
        automation_name,
        step=None,
    ):
        super().__init__(
            message=f"Required field '{field}' is missing from the payload",
            automation_name=automation_name,
            step=step,
            context={"field": field},
        )
