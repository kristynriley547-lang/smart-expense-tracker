"""Markdown report generation."""

from __future__ import annotations

from decimal import Decimal

from .analyzer import detect_unusual_expenses, monthly_cash_flow, spending_by_category, summarize
from .models import Transaction


def money(value: Decimal) -> str:
    """Format a Decimal as currency."""

    return f"${value:,.2f}"


def build_markdown_report(transactions: list[Transaction]) -> str:
    """Build a Markdown financial report."""

    summary = summarize(transactions)
    categories = spending_by_category(transactions)
    months = monthly_cash_flow(transactions)
    unusual = detect_unusual_expenses(transactions)

    lines = [
        "# Smart Expense Tracker Report",
        "",
        "## Executive Summary",
        "",
        f"The dataset contains **{summary['transaction_count']} transactions**.",
        (
            f"Total income is **{money(summary['total_income'])}**, "
            f"total expenses are **{money(summary['total_expenses'])}**, "
            f"and net cash flow is **{money(summary['net_cash_flow'])}**."
        ),
        f"The calculated savings rate is **{summary['savings_rate_percent']}%**.",
        "",
        "## Spending by Category",
        "",
        "| Category | Amount |",
        "|---|---:|",
    ]

    for category, amount in categories.items():
        lines.append(f"| {category} | {money(amount)} |")

    lines.extend(["", "## Monthly Cash Flow", "", "| Month | Net Cash Flow |", "|---|---:|"])
    for month, amount in months.items():
        lines.append(f"| {month} | {money(amount)} |")

    lines.extend(["", "## Unusual Expenses", ""])
    if unusual:
        lines.extend(["| Date | Description | Category | Amount |", "|---|---|---|---:|"])
        for tx in unusual:
            lines.append(
                f"| {tx.date.isoformat()} | {tx.description} | "
                f"{tx.category} | {money(-tx.amount)} |"
            )
    else:
        lines.append("No unusual expenses were detected using the default threshold.")

    lines.extend([
        "",
        "## Notes",
        "",
        (
            "This report is generated locally from a CSV file. "
            "It does not upload or transmit your financial data."
        ),
    ])
    return "\n".join(lines) + "\n"
