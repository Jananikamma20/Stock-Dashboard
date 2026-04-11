import yfinance as yf

stock = yf.Ticker("AAPL")

data = stock.history(period="1d", interval="1m")

print(data.head())