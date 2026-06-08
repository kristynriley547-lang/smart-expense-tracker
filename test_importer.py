from decimal import Decimal

import pytest

from smart_expense_tracker.importer import load_transactions
from smart_expense_tracker.models import parse_amount, parse_date


def test_parse_date_supports_common_formats():
    assert parse_date("2026-01-31").isoformat() == "2026-01-31"
    assert parse_date("01/31/2026").isoformat() == "2026-01-31"


def test_parse_amount_supports_currency_and_parentheses():
    assert parse_amount("$1,234.56") == Decimal("1234.56")
    assert parse_amount("($99.50)") == Decimal("-99.50")


def test_load_transactions_fills_missing_category(tmp_path):
    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(
        "date,description,amount\n2026-01-01,Payroll Deposit,2500\n2026-01-02,Netflix,-15.99\n",
        encoding="utf-8",
    )

    transactions = load_transactions(csv_file)

    assert transactions[0].category == "Salary"
    assert transactions[1].category == "Entertainment"


def test_load_transactions_rejects_missing_columns(tmp_path):
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text("date,amount\n2026-01-01,10\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required columns"):
        load_transactions(csv_file)
