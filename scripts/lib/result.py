from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Result(Generic[T]):
    success: bool
    data: T | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, msg: str) -> "Result[T]":
        self.errors.append(msg)
        self.success = False
        return self

    def add_warning(self, msg: str) -> "Result[T]":
        self.warnings.append(msg)
        return self
