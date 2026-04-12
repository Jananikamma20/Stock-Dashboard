import yfinance as yf
import matplotlib.pyplot as plt

# Select stock
stock = yf.Ticker("TCS.NS")

# Get data
data = stock.history(period="1d", interval="1m")

# Plot chart
plt.figure()
plt.plot(data.index, data['Close'], linestyle='-', marker='')
plt.grid()

# Labels
plt.title("Stock Price Chart - RELIANCE")
plt.xlabel("Time")
plt.ylabel("Price")

# Show graph
plt.show()