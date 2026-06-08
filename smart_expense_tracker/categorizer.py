"""Rule-based categorization for transaction descriptions."""

from __future__ import annotations

from collections.abc import Mapping

DEFAULT_RULES: dict[str, tuple[str, ...]] = {
    "Housing": ("rent", "mortgage", "landlord", "apartment"),
    "Groceries": ("grocery", "supermarket", "whole foods", "aldi", "costco"),
    "Dining": ("restaurant", "cafe", "coffee", "pizza", "burger", "doordash"),
    "Transportation": ("uber", "lyft", "fuel", "gas", "metro", "parking"),
    "Utilities": ("electric", "water", "internet", "phone", "utility"),
    "Entertainment": ("netflix", "spotify", "cinema", "movie", "game"),
    "Healthcare": ("pharmacy", "doctor", "hospital", "clinic", "dental"),
    "Salary": ("salary", "payroll", "direct deposit", "wages"),
    "Savings": ("savings", "investment", "brokerage", "ira"),
}


def categorize(description: str, rules: Mapping[str, tuple[str, ...]] | None = None) -> str:
    """Return a category based on keywords in the description."""

    active_rules = rules or DEFAULT_RULES
    normalized = description.lower()
    for category, keywords in active_rules.items():
        if any(keyword in normalized for keyword in keywords):
            return category
    return "Other"
