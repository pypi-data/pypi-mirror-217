from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic.error_wrappers import ErrorDict


class ConfigError(Exception):
    def __init__(self, errors: List["ErrorDict"]):
        self._errors = errors

    def __str__(self) -> str:
        return "Configuration Errors:\n\t" + "\n\t".join(
            self._error_msg(error) for error in self._errors
        )

    @staticmethod
    def _error_msg(error: "ErrorDict") -> str:
        return f"{error['loc'][0]}: {error['msg']}"
