"""Analysis functions for financial transactions."""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal
from statistics import mean

from .models import Transaction


def summarize(transactions: list[Transaction]) -> dict[str, Decimal | int]:
    """Return a high-level financial summary."""

    income = sum((tx.amount for tx in transactions if tx.is_income), Decimal("0"))
    expenses = sum((-tx.amount for tx in transactions if tx.is_expense), Decimal("0"))
    return {
        "transaction_count": len(transactions),
        "total_income": income,
        "total_expenses": expenses,
        "net_cash_flow": income - expenses,
        "savings_rate_percent": (
            ((income - expenses) / income * 100).quantize(Decimal("0.01"))
            if income
            else Decimal("0")
        ),
    }


def spending_by_category(transactions: list[Transaction]) -> dict[str, Decimal]:
    """Return expense totals grouped by category."""

    totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    for tx in transactions:
        if tx.is_expense:
            totals[tx.category] += -tx.amount
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def monthly_cash_flow(transactions: list[Transaction]) -> dict[str, Decimal]:
    """Return net cash flow grouped by YYYY-MM."""

    totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    for tx in transactions:
        totals[tx.date.strftime("%Y-%m")] += tx.amount
    return dict(sorted(totals.items()))


def detect_unusual_expenses(
    transactions: list[Transaction], multiplier: float = 2.0
) -> list[Transaction]:
    """Detect expense transactions that are unusually large for their category."""

    expenses_by_category: dict[str, list[Decimal]] = defaultdict(list)
    for tx in transactions:
        if tx.is_expense:
            expenses_by_category[tx.category].append(-tx.amount)

    thresholds = {
        category: Decimal(str(mean(amounts))) * Decimal(str(multiplier))
        for category, amounts in expenses_by_category.items()
        if len(amounts) >= 2
    }

    unusual: list[Transaction] = []
    for tx in transactions:
        if (
            tx.is_expense
            and tx.category in thresholds
            and -tx.amount > thresholds[tx.category]
        ):
            unusual.append(tx)
    return sorted(unusual, key=lambda tx: abs(tx.amount), reverse=True)
