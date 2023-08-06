import traceback
import warnings

class BackendError(RuntimeError):
    def __init__(self, *args: object, **kwargs) -> None:
        self.response = kwargs.pop("response", None)
        super().__init__(*args)