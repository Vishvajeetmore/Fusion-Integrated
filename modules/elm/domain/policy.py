from datetime import date
from decimal import Decimal

from modules.elm.domain.entities import (
    LeaveCategory,
    LeaveRequestDateRange,
)


_CONTINUOUS_CATEGORIES = (
    LeaveCategory.EL,
    LeaveCategory.COL,
    LeaveCategory.VL,
)


def count_continuous_leave_days(
    category: LeaveCategory,
    date_range: LeaveRequestDateRange,
) -> int:
    """Count inclusive calendar days for EL, COL, or VL."""
    if not isinstance(category, LeaveCategory):
        raise TypeError("category must be a LeaveCategory")

    if not isinstance(date_range, LeaveRequestDateRange):
        raise TypeError("date_range must be a LeaveRequestDateRange")

    if type(date_range.start_date) is not date or type(date_range.end_date) is not date:
        raise TypeError("date range boundaries must be dates")

    if category not in _CONTINUOUS_CATEGORIES:
        raise ValueError(
            f"{category.value} does not use continuous leave counting"
        )

    return (date_range.end_date - date_range.start_date).days + 1


def validate_sufficient_balance(
    available_balance: int | Decimal,
    requested_days: int | Decimal,
) -> None:
    """Raise an error when requested leave exceeds the available balance."""
    values = (
        ("available_balance", available_balance),
        ("requested_days", requested_days),
    )

    for name, value in values:
        if isinstance(value, bool) or not isinstance(value, (int, Decimal)):
            raise TypeError(f"{name} must be an integer or Decimal")

        if isinstance(value, Decimal) and not value.is_finite():
            raise ValueError(f"{name} must be finite")

        if value < 0:
            raise ValueError(f"{name} cannot be negative")

    available = Decimal(available_balance)
    requested = Decimal(requested_days)

    if requested > available:
        from modules.elm.domain.errors import InsufficientBalanceError
        raise InsufficientBalanceError(available, requested)

    return None
