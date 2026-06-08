"""Domain models for the Smart Expense Tracker application."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True)
class Transaction:
    """A single financial transaction.

    Positive amounts are treated as income and negative amounts are treated as
    expenses. The category field is normalized by the importer when possible.
    """

    date: date
    description: str
    amount: Decimal
    category: str

    @property
    def is_income(self) -> bool:
        """Return whether the transaction is income."""

        return self.amount > 0

    @property
    def is_expense(self) -> bool:
        """Return whether the transaction is an expense."""

        return self.amount < 0


def parse_date(value: str) -> date:
    """Parse a date string in common CSV formats.

    Supported formats are ISO date, US slash date, and European slash date.
    """

    cleaned = value.strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {value!r}")


def parse_amount(value: str) -> Decimal:
    """Parse a currency amount from a CSV cell."""

    cleaned = value.strip().replace(",", "").replace("$", "")
    if cleaned.startswith("(") and cleaned.endswith(")"):
        cleaned = f"-{cleaned[1:-1]}"
    try:
        return Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid amount: {value!r}") from exc
