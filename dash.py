import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.title("Stock Dashboard")
st.markdown("### Analyze stock trends and compare performance easily")

st.sidebar.header("Filters")

period = st.sidebar.selectbox(
    "Select Period",
    ["1d", "5d", "1mo", "3mo", "6mo", "1y"]
)

interval = st.sidebar.selectbox(
    "Select Interval",
    ["1m", "5m", "15m", "1h", "1d"]
)

mode = st.radio("Select Mode", ["Single Stock", "Compare Stocks"])

stocks_list = {
        "Reliance": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "Infosys": "INFY.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "ICICI Bank": "ICICIBANK.NS"
}

# SINGLE STOCK MODE

if mode == "Single Stock":

    stock_name = st.selectbox("Select a Stock", list(stocks_list.keys()))
    stock_option = stocks_list[stock_name]

    stock = yf.Ticker(stock_option)
    data = stock.history(period=period, interval=interval)
    data['MA_20'] = data['Close'].rolling(window=20).mean()
    data['Returns'] = data['Close'].pct_change()

    fig, ax = plt.subplots()

    ax.plot(data.index, data['Close'], label="Close Price", linewidth=2)
    ax.plot(data.index, data['MA_20'], label="Moving Avg (20)", linewidth=2)

    ax.set_title(f"{stock_option} Price Chart", fontsize=14)
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")

    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    st.subheader("Recent Data")
    st.dataframe(data.tail())

    # Stock Info
    st.subheader("Stock Info")

    latest_return = data['Returns'].iloc[-1] * 100 
    st.write("Latest Price:", data['Close'].iloc[-1])
    st.write("Highest Price:", data['High'].max())
    st.write("Lowest Price:", data['Low'].min())
    if latest_return > 0:
        st.success(f"Latest Return: {round(latest_return, 2)}% 📈")
    else:
        st.error(f"Latest Return: {round(latest_return, 2)}% 📉")

# COMPARE MODE

else:
    selected_names = st.multiselect(
        "Select Stocks to Compare",
        list(stocks_list.keys())
    )

    if selected_names:
        fig, ax = plt.subplots()

        for name in selected_names:
            stock = yf.Ticker(stocks_list[name])
            data = stock.history(period=period, interval=interval)
            if data.empty:
                st.warning("No data available. Try different settings.")
            ax.plot(data.index, data['Close'], label=name, linewidth=2)

        ax.set_title("Stock Comparison", fontsize=14)
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")

        ax.grid(True)
        ax.legend()

        st.pyplot(fig)