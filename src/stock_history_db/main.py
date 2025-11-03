import os
import psycopg
import yfinance as yf
from datetime import datetime
from dotenv import load_dotenv

from stock_history_db.core.postgres_utils import EnsureStockHistoryTableExists
from stock_history_db.core.postgres_utils import InsertStockHistoryData
from stock_history_db.core.postgres_utils import GetConnectionString
from stock_history_db.core.postgres_utils import GetStoredTickerHistoryRange
from stock_history_db.core.utils import MinimumDateFromPeriod


if __name__ == "__main__":
    load_dotenv()

    table = os.getenv("STOCK_HISTORY_TABLE")
    period = os.getenv("STOCK_HISTORY_PERIOD")
    tickers = [ticker.strip() for ticker in os.getenv("STOCK_HISTORY_TICKERS").split(",")]

    with psycopg.connect(GetConnectionString()) as conn:
        EnsureStockHistoryTableExists(conn=conn, table=table)
        minimum_date = MinimumDateFromPeriod(period=period)

        for ticker in tickers:
            # Determine dates for Data Request
            # noinspection PyRedeclaration
            target_date = minimum_date
            oldest_date, newest_date = GetStoredTickerHistoryRange(conn=conn, table=table, ticker=ticker)

            if not (oldest_date and newest_date):
                oldest_date = datetime.today().date()

            if oldest_date < target_date: # MinimumDateFromPeriod is more recent than oldest date in db
                target_date = newest_date

            if target_date == datetime.today().date(): # No data to gather
                continue

            # Get Data
            stock_history_data = yf.Ticker(ticker).history(start=target_date, end=datetime.today().date())
            stock_history_data = stock_history_data.reset_index().to_dict(orient='records')

            # Update Table
            rows_affected = InsertStockHistoryData(conn=conn, table=table, ticker=ticker, stock_history_data=stock_history_data)

            print(f"{ticker:<8} +{rows_affected:<3} from {target_date.strftime('%Y-%m-%d')}")

