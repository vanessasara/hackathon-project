"""
Recurrence calculation utilities for recurring tasks.

Part B: Advanced Features - Recurring Tasks

This module handles calculating the next occurrence date for recurring tasks
based on various recurrence patterns.
"""

import re
from datetime import datetime, timedelta
from typing import Optional, Tuple


# Recurrence rule patterns
RECURRENCE_PATTERNS = {
    "daily": "Daily recurrence - same time every day",
    "weekly": "Weekly recurrence - same day and time every week",
    "monthly": "Monthly recurrence - same day of month",
    "weekdays": "Weekday recurrence - Monday through Friday",
}


def parse_recurrence_rule(rule: str) -> Tuple[str, Optional[str]]:
    """
    Parse a recurrence rule string into type and optional cron expression.

    Args:
        rule: Recurrence rule string (e.g., "daily", "weekly", "cron:0 9 * * 1")

    Returns:
        Tuple of (rule_type, cron_expression or None)

    Raises:
        ValueError: If the rule format is invalid
    """
    if not rule:
        raise ValueError("Recurrence rule cannot be empty")

    rule = rule.strip().lower()

    # Check for simple patterns
    if rule in RECURRENCE_PATTERNS:
        return (rule, None)

    # Check for cron pattern
    if rule.startswith("cron:"):
        cron_expr = rule[5:].strip()
        if not cron_expr:
            raise ValueError("Cron expression cannot be empty")
        # Basic validation: should have 5 space-separated fields
        parts = cron_expr.split()
        if len(parts) != 5:
            raise ValueError(f"Invalid cron expression: expected 5 fields, got {len(parts)}")
        return ("cron", cron_expr)

    raise ValueError(f"Unknown recurrence rule: {rule}")


def calculate_next_occurrence(
    current_date: datetime,
    recurrence_rule: str,
    recurrence_end: Optional[datetime] = None,
) -> Optional[datetime]:
    """
    Calculate the next occurrence date for a recurring task.

    Args:
        current_date: The current/completed task's date
        recurrence_rule: The recurrence pattern (daily, weekly, monthly, weekdays, cron:...)
        recurrence_end: Optional end date for the recurring series

    Returns:
        The next occurrence datetime, or None if the series has ended

    Raises:
        ValueError: If the recurrence rule is invalid
    """
    rule_type, cron_expr = parse_recurrence_rule(recurrence_rule)

    next_date: Optional[datetime] = None

    if rule_type == "daily":
        next_date = current_date + timedelta(days=1)

    elif rule_type == "weekly":
        next_date = current_date + timedelta(weeks=1)

    elif rule_type == "monthly":
        next_date = _add_months(current_date, 1)

    elif rule_type == "weekdays":
        next_date = _next_weekday(current_date)

    elif rule_type == "cron" and cron_expr:
        next_date = _next_cron_occurrence(current_date, cron_expr)

    # Check if next occurrence is past the end date
    if next_date and recurrence_end and next_date > recurrence_end:
        return None

    return next_date


def _add_months(dt: datetime, months: int) -> datetime:
    """
    Add months to a datetime, handling month-end edge cases.

    Args:
        dt: The starting datetime
        months: Number of months to add

    Returns:
        New datetime with months added
    """
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1

    # Handle day overflow (e.g., Jan 31 + 1 month = Feb 28)
    import calendar

    max_day = calendar.monthrange(year, month)[1]
    day = min(dt.day, max_day)

    return dt.replace(year=year, month=month, day=day)


def _next_weekday(dt: datetime) -> datetime:
    """
    Get the next weekday (Monday-Friday) after the given date.

    Args:
        dt: The starting datetime

    Returns:
        Next weekday datetime
    """
    next_day = dt + timedelta(days=1)

    # 0 = Monday, 4 = Friday, 5 = Saturday, 6 = Sunday
    while next_day.weekday() > 4:  # Skip Saturday and Sunday
        next_day += timedelta(days=1)

    return next_day


def _next_cron_occurrence(dt: datetime, cron_expr: str) -> Optional[datetime]:
    """
    Calculate the next occurrence based on a cron expression.

    Supports a simplified subset of cron:
    - minute (0-59)
    - hour (0-23)
    - day of month (1-31)
    - month (1-12)
    - day of week (0-6, 0=Sunday)

    Args:
        dt: The starting datetime
        cron_expr: Cron expression (5 fields)

    Returns:
        Next matching datetime, or None if no match within 1 year
    """
    parts = cron_expr.split()
    if len(parts) != 5:
        return None

    minute, hour, day, month, dow = parts

    # Start from the next minute
    candidate = dt.replace(second=0, microsecond=0) + timedelta(minutes=1)
    max_iterations = 525600  # 1 year in minutes

    for _ in range(max_iterations):
        if _matches_cron(candidate, minute, hour, day, month, dow):
            return candidate
        candidate += timedelta(minutes=1)

    return None  # No match within 1 year


def _matches_cron(
    dt: datetime, minute: str, hour: str, day: str, month: str, dow: str
) -> bool:
    """
    Check if a datetime matches a cron expression.

    Args:
        dt: Datetime to check
        minute, hour, day, month, dow: Cron field values

    Returns:
        True if the datetime matches all cron fields
    """
    # Convert Sunday from 0 to 7 for Python's weekday() (0=Monday)
    python_dow = (dt.weekday() + 1) % 7  # 0=Sunday in cron

    return (
        _matches_field(dt.minute, minute)
        and _matches_field(dt.hour, hour)
        and _matches_field(dt.day, day)
        and _matches_field(dt.month, month)
        and _matches_field(python_dow, dow)
    )


def _matches_field(value: int, pattern: str) -> bool:
    """
    Check if a value matches a cron field pattern.

    Supports:
    - * (any value)
    - single number (e.g., "5")
    - list (e.g., "1,3,5")
    - range (e.g., "1-5")
    - step (e.g., "*/15")

    Args:
        value: The actual value to check
        pattern: The cron pattern

    Returns:
        True if value matches pattern
    """
    if pattern == "*":
        return True

    # Handle step pattern (*/n)
    if pattern.startswith("*/"):
        try:
            step = int(pattern[2:])
            return value % step == 0
        except ValueError:
            return False

    # Handle list pattern (1,2,3)
    if "," in pattern:
        values = [int(v) for v in pattern.split(",")]
        return value in values

    # Handle range pattern (1-5)
    if "-" in pattern:
        parts = pattern.split("-")
        if len(parts) == 2:
            try:
                start, end = int(parts[0]), int(parts[1])
                return start <= value <= end
            except ValueError:
                return False

    # Handle single value
    try:
        return value == int(pattern)
    except ValueError:
        return False


def is_valid_recurrence_rule(rule: str) -> bool:
    """
    Validate a recurrence rule string.

    Args:
        rule: The recurrence rule to validate

    Returns:
        True if the rule is valid, False otherwise
    """
    try:
        parse_recurrence_rule(rule)
        return True
    except ValueError:
        return False
