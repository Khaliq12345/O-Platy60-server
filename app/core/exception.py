from typing import Any


class BusinessError(Exception):
    """Base class for all business logic errors"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ItemNotFoundError(BusinessError):
    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id
        self.message = f"{name} with id {id} not found"

    def __str__(self) -> str:
        return self.message


class DatabaseError(BusinessError):
    def __init__(self, name: str, exception: Any) -> None:
        super().__init__()
        self.name = name
        self.exception = exception

    def __str__(self):
        return f"Function -> {self.name} | There's an error with database - {self.exception}"
