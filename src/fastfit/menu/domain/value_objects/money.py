from dataclasses import dataclass
from decimal import Decimal
from typing import Self

from common.domain.exceptions import InvariantViolationError


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise InvariantViolationError("Amount cannot be negative")
        if not self.currency.strip():
            raise InvariantViolationError("Currency must not be empty")

    @classmethod
    def create(cls, amount: Decimal, currency: str = "USD") -> Self:
        return cls(amount=amount, currency=currency)
