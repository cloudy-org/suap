__all__ = ()

class SuapError(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message

        super().__init__(message)

class TemplateKeysRemainingError(SuapError):
    def __init__(self, remaining_keys: set[str]):
        super().__init__(
            "There are keys defined in the template " \
                f"that were not formatted! Remaining Keys: {remaining_keys}"
        )