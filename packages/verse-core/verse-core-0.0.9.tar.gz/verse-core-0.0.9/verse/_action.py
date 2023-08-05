from typing import Any


class Action:
    def __init__(self, name: str, **kwargs: Any):
        self.name = name
        self.args = locals()["kwargs"]

    def __str__(self) -> str:
        _str = f"ACTION {self.name}"
        for key, value in self.args:
            _str = f" {key.upper()}"
        return _str

    def _serialize(self, value) -> str:
        return ""
