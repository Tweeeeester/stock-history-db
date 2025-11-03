import os
import psycopg

from datetime import date
from psycopg import sql
from typing import Any, Dict, List, Tuple


CONNECTION = psycopg.Connection[Tuple[Any, ...]]


def EnsureStockHistoryTableExists(conn: CONNECTION, table: str) -> None:
    cursor = conn.cursor()

    SQL_STATEMENT = """
        CREATE TABLE IF NOT EXISTS {table} (
            ticker VARCHAR(6) NOT NULL,
            date date NOT NULL,
            open float,
            high float,
            low float,
            close float,
            volume int,
            dividends float,
            stock_splits float,
            PRIMARY KEY (ticker, date)
        )
    """

    SQL_STATEMENT = sql.SQL(SQL_STATEMENT).format(table=sql.Identifier(table))

    try:
        cursor.execute(SQL_STATEMENT)
        conn.commit()  # Crucial for applying changes

    except psycopg.Error as e:
        print(f"Error creating table: {e}")
        conn.rollback() # Rollback in case of error
    finally:
        cursor.close()
    return

def InsertStockHistoryData(conn: CONNECTION, table: str, ticker:str, stock_history_data: List[Dict[str, Any]]) -> int:
    cursor = conn.cursor()

    SQL_STATEMENT = """
        INSERT INTO {table} ("ticker", "date", "open", "high", "low", "close", "volume", "dividends", "stock_splits")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT ("ticker", "date") DO NOTHING;
    """
    rows_affected = 0
    SQL_STATEMENT = sql.SQL(SQL_STATEMENT).format(table=sql.Identifier(table))
    try:
        for data in stock_history_data:
            cursor.execute(SQL_STATEMENT, (ticker, data["Date"], data["Open"], data["High"], data["Low"], data["Close"], data["Volume"], data["Dividends"], data["Stock Splits"]))
            rows_affected += cursor.rowcount
            conn.commit()  # Crucial for applying changes
    except psycopg.Error as e:
        print(f"Error in InsertStockHistoryData: {e}")
        conn.rollback()  # Rollback in case of error
    finally:
        cursor.close()
    return rows_affected

def GetConnectionString() -> str:
    host = os.getenv("POSTGRES_HOST")
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    return  f"host={host} dbname={dbname} user={user} password={password}"

def GetStoredTickerHistoryRange(conn: CONNECTION, table: str, ticker: str) -> Tuple[date, date]:
    cursor = conn.cursor()
    oldest_date = None
    newest_date = None
    SQL_STATEMENT = """
        SELECT ticker,
           MIN(date) AS oldest_date,
           MAX(date) AS newest_date
        FROM {table}
        WHERE ticker = %s
        GROUP BY ticker
    """

    SQL_STATEMENT = sql.SQL(SQL_STATEMENT).format(table=sql.Identifier(table))

    try:
        cursor.execute(SQL_STATEMENT, (ticker,))
        for row in cursor.fetchall():
            oldest_date = row[1]
            newest_date = row[2]

    except psycopg.Error as e:
        print(f"Error in GetStoredTickerHistoryRange: {e}")
        conn.rollback() # Rollback in case of error
    finally:
        cursor.close()
    return oldest_date, newest_date
