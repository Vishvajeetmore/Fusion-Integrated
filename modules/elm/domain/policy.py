from datetime import date

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
