"""CSV import utilities."""

from __future__ import annotations

import csv
from pathlib import Path

from .categorizer import categorize
from .models import Transaction, parse_amount, parse_date

REQUIRED_COLUMNS = {"date", "description", "amount"}


def load_transactions(csv_path: str | Path) -> list[Transaction]:
    """Load transactions from a CSV file.

    The CSV must include date, description, and amount columns. A category column
    is optional; missing or blank categories are filled by the categorizer.
    """

    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = {name.strip().lower() for name in (reader.fieldnames or [])}
        missing = REQUIRED_COLUMNS - fieldnames
        if missing:
            raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")

        transactions: list[Transaction] = []
        for row_number, row in enumerate(reader, start=2):
            normalized = {key.strip().lower(): (value or "").strip() for key, value in row.items()}
            description = normalized["description"]
            category = normalized.get("category") or categorize(description)
            try:
                transactions.append(
                    Transaction(
                        date=parse_date(normalized["date"]),
                        description=description,
                        amount=parse_amount(normalized["amount"]),
                        category=category,
                    )
                )
            except ValueError as exc:
                raise ValueError(f"Invalid data on row {row_number}: {exc}") from exc
    return transactions
