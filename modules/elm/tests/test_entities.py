import unittest
from datetime import date

from modules.elm.domain.entities import (
    LeaveCategory,
    LeaveRequest,
    LeaveRequestDateRange,
)
from modules.elm.domain.errors import (
    ELMDomainError,
    InvalidDateRangeError,
    IneligibleCategoryError,
    InsufficientBalanceError,
    OverlappingLeaveError,
    InvalidWorkflowTransitionError,
)


class TestLeaveCategory(unittest.TestCase):
    def test_exact_supported_categories(self):
        self.assertEqual(
            [(category.name, category.value) for category in LeaveCategory],
            [
                ("CL", "CL"),
                ("RH", "RH"),
                ("SCL", "SCL"),
                ("EL", "EL"),
                ("COL", "COL"),
                ("VL", "VL"),
            ],
        )


class TestLeaveRequestDateRange(unittest.TestCase):
    def test_valid_date_range(self):
        start = date(2026, 10, 1)
        end = date(2026, 10, 10)

        date_range = LeaveRequestDateRange(start, end)

        self.assertEqual(date_range.start_date, start)
        self.assertEqual(date_range.end_date, end)

    def test_reversed_date_range_is_rejected(self):
        with self.assertRaises(ValueError):
            LeaveRequestDateRange(
                date(2026, 10, 10),
                date(2026, 10, 1),
            )


class TestLeaveRequest(unittest.TestCase):
    def test_leave_request_creation(self):
        date_range = LeaveRequestDateRange(
            date(2026, 10, 1),
            date(2026, 10, 10),
        )

        request = LeaveRequest(LeaveCategory.CL, date_range)

        self.assertEqual(request.category, LeaveCategory.CL)
        self.assertEqual(request.date_range, date_range)


class TestELMDomainErrors(unittest.TestCase):
    def test_specific_errors_inherit_from_base(self):
        exception_types = [
            InvalidDateRangeError,
            IneligibleCategoryError,
            InsufficientBalanceError,
            OverlappingLeaveError,
            InvalidWorkflowTransitionError,
        ]

        for exception_type in exception_types:
            with self.subTest(exception=exception_type.__name__):
                self.assertTrue(
                    issubclass(exception_type, ELMDomainError)
                )

    def test_specific_errors_can_be_instantiated(self):
        instances = [
            InvalidDateRangeError(date(2026, 10, 10), date(2026, 10, 1)),
            IneligibleCategoryError("CL"),
            InsufficientBalanceError(2, 5),
            OverlappingLeaveError(object()),
            InvalidWorkflowTransitionError("pending", "approved"),
        ]

        for exception in instances:
            with self.subTest(exception=type(exception).__name__):
                self.assertIsInstance(exception, ELMDomainError)


if __name__ == "__main__":
    unittest.main()
