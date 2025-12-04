from abc import ABC, abstractmethod
from datetime import timedelta
from django.utils.timezone import now


class SalesReportStrategy(ABC):
    """Strategy interface for calculating sales report date ranges."""

    @abstractmethod
    def get_date_range(self):
        """Return a tuple of (start_date, end_date) for the report."""
        raise NotImplementedError


class TodaySalesStrategy(SalesReportStrategy):
    def get_date_range(self):
        start_date = now().replace(hour=0, minute=0, second=0, microsecond=0)
        return start_date, now()


class LastWeekSalesStrategy(SalesReportStrategy):
    def get_date_range(self):
        end_date = now()
        start_date = end_date - timedelta(days=7)
        return start_date, end_date


class LastMonthSalesStrategy(SalesReportStrategy):
    def get_date_range(self):
        end_date = now()
        start_date = end_date - timedelta(days=30)
        return start_date, end_date


SALES_REPORT_STRATEGIES = {
    "today": TodaySalesStrategy(),
    "last_week": LastWeekSalesStrategy(),
    "last_month": LastMonthSalesStrategy(),
}
