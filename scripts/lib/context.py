from dataclasses import dataclass
from typing import Callable, Generic, Protocol, Self, TypeVar

T = TypeVar("T")
R = TypeVar("R", bound="HasSuccess")


class HasSuccess(Protocol):
    success: bool


@dataclass
class Context(Generic[T, R]):
    data: T
    result: R

    def bind(self, func: Callable[[Self], Self]) -> Self:
        if not self.result.success:
            return self
        return func(self)

    def map(self, func: Callable[[Self], Self]) -> Self:
        return func(self)
