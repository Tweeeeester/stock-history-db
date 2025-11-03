# stock-history-db

## .env 
### STOCK_HISTORY_PERIOD
This variable represennts the minimum period of historical data that should be gathered.
These are the period options:
- Day: "1d", "5d", "30d"
- Month: "1mo", "6mo"
- Year: "1y", "5y"

### STOCK_HISTORY_TICKERS
A string containing all stock ticker to gather the history of.
Each ticker should be separated in the string by a comma.
For example, to gather the data for Apply, Costco, and NVIDIA use "AAPL,COST,NVDA"