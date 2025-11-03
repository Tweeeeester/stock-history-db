from datetime import datetime
from unittest.mock import patch

from stock_history_db.core.utils import MinimumDateFromPeriod


def test_MinimumDateFromPeriod() -> None:
    with patch("stock_history_db.core.utils.date") as mock_date:
        mock_date.today.return_value = datetime(year=2025, month=12, day=31).date()

        assert MinimumDateFromPeriod(period="1d")   == datetime(year=2025, month=12, day=30).date()
        assert MinimumDateFromPeriod(period="5d")   == datetime(year=2025, month=12, day=26).date()
        assert MinimumDateFromPeriod(period="1mo")  == datetime(year=2025, month=11, day=30).date()
        assert MinimumDateFromPeriod(period="5mo")  == datetime(year=2025, month=7,  day=31).date()
        assert MinimumDateFromPeriod(period="1y")   == datetime(year=2024, month=12, day=31).date()
        assert MinimumDateFromPeriod(period="5y")   == datetime(year=2020, month=12, day=31).date()
    return
