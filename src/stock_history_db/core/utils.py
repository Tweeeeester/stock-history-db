from datetime import date
from dateutil.relativedelta import relativedelta


def MinimumDateFromPeriod(period: str) -> date:
    min_date = None
    if period == "ytd" or period == "max":
        raise NotImplemented("Periods of YTD and MAX are not yet implemented")
    elif "d" in period:
        days = int(period.split("d")[0])
        min_date = date.today() - relativedelta(days=days)
    elif "mo" in period:
        months = int(period.split("mo")[0])
        min_date = date.today() - relativedelta(months=months)
    elif "y" in period:
        years = int(period.split("y")[0])
        min_date = date.today() - relativedelta(years=years)
    if not min_date:
        raise ValueError(f"Invalid period '{period}'")

    return min_date