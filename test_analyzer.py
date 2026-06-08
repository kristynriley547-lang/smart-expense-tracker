from datetime import date
from decimal import Decimal

from smart_expense_tracker.analyzer import (
    detect_unusual_expenses,
    monthly_cash_flow,
    spending_by_category,
    summarize,
)
from smart_expense_tracker.models import Transaction


def sample_transactions():
    return [
        Transaction(date(2026, 1, 1), "Salary", Decimal("3000.00"), "Salary"),
        Transaction(date(2026, 1, 2), "Rent", Decimal("-1200.00"), "Housing"),
        Transaction(date(2026, 1, 5), "Coffee", Decimal("-5.00"), "Dining"),
        Transaction(date(2026, 1, 6), "Restaurant", Decimal("-45.00"), "Dining"),
        Transaction(date(2026, 2, 1), "Salary", Decimal("3000.00"), "Salary"),
        Transaction(date(2026, 2, 4), "Large Dinner", Decimal("-180.00"), "Dining"),
    ]


def test_summarize_returns_expected_totals():
    result = summarize(sample_transactions())

    assert result["transaction_count"] == 6
    assert result["total_income"] == Decimal("6000.00")
    assert result["total_expenses"] == Decimal("1430.00")
    assert result["net_cash_flow"] == Decimal("4570.00")
    assert result["savings_rate_percent"] == Decimal("76.17")


def test_spending_by_category_groups_only_expenses():
    result = spending_by_category(sample_transactions())

    assert result["Housing"] == Decimal("1200.00")
    assert result["Dining"] == Decimal("230.00")
    assert "Salary" not in result


def test_monthly_cash_flow_groups_by_month():
    result = monthly_cash_flow(sample_transactions())

    assert result == {"2026-01": Decimal("1750.00"), "2026-02": Decimal("2820.00")}


def test_detect_unusual_expenses_flags_large_category_outlier():
    result = detect_unusual_expenses(sample_transactions(), multiplier=1.5)

    assert len(result) == 1
    assert result[0].description == "Large Dinner"
