"""Command-line interface for Smart Expense Tracker."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import detect_unusual_expenses, monthly_cash_flow, spending_by_category, summarize
from .importer import load_transactions
from .report import build_markdown_report, money


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""

    parser = argparse.ArgumentParser(
        prog="smart-expense-tracker",
        description="Analyze personal finance transactions from a CSV file.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    summary = subparsers.add_parser("summary", help="Print a financial summary.")
    summary.add_argument("csv_file", help="Path to the transaction CSV file.")

    categories = subparsers.add_parser("categories", help="Print spending by category.")
    categories.add_argument("csv_file", help="Path to the transaction CSV file.")

    monthly = subparsers.add_parser("monthly", help="Print monthly cash flow.")
    monthly.add_argument("csv_file", help="Path to the transaction CSV file.")

    unusual = subparsers.add_parser("unusual", help="Print unusual expense transactions.")
    unusual.add_argument("csv_file", help="Path to the transaction CSV file.")
    unusual.add_argument(
        "--multiplier",
        type=float,
        default=2.0,
        help="Threshold multiplier above category average.",
    )

    report = subparsers.add_parser("report", help="Generate a Markdown report.")
    report.add_argument("csv_file", help="Path to the transaction CSV file.")
    report.add_argument(
        "--output", "-o", default="expense_report.md", help="Output Markdown file path."
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""

    args = build_parser().parse_args(argv)
    transactions = load_transactions(args.csv_file)

    if args.command == "summary":
        summary = summarize(transactions)
        print(f"Transactions: {summary['transaction_count']}")
        print(f"Income: {money(summary['total_income'])}")
        print(f"Expenses: {money(summary['total_expenses'])}")
        print(f"Net cash flow: {money(summary['net_cash_flow'])}")
        print(f"Savings rate: {summary['savings_rate_percent']}%")
        return 0

    if args.command == "categories":
        for category, amount in spending_by_category(transactions).items():
            print(f"{category}: {money(amount)}")
        return 0

    if args.command == "monthly":
        for month, amount in monthly_cash_flow(transactions).items():
            print(f"{month}: {money(amount)}")
        return 0

    if args.command == "unusual":
        unusual_transactions = detect_unusual_expenses(transactions, multiplier=args.multiplier)
        if not unusual_transactions:
            print("No unusual expenses detected.")
            return 0
        for tx in unusual_transactions:
            print(
                f"{tx.date.isoformat()} | {tx.category} | "
                f"{tx.description} | {money(-tx.amount)}"
            )
        return 0

    if args.command == "report":
        output = Path(args.output)
        output.write_text(build_markdown_report(transactions), encoding="utf-8")
        print(f"Report written to {output}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
