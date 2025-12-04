from abc import ABC, abstractmethod
from datetime import timedelta
from django.utils.timezone import now


# Strategy pattern applied to sales report date-range selection via interchangeable classes for daily, weekly,
# monthly, yearly, and custom ranges.SalesReportView now delegates range calculation to the strategy registry,
# simplifying validation and adding extensibility for new periods.
# Each strategy encapsulates its own
# validation/parsing (including ISO week handling), keeping the view lean and cohesive.

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
