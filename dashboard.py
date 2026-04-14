import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.title("Stock Dashboard")

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

# SINGLE STOCK MODE

if mode == "Single Stock":
    stock_option = st.selectbox(
        "Select a Stock",
        ("RELIANCE.NS", "TCS.NS", "INFY.NS")
    )

    stock = yf.Ticker(stock_option)
    data = stock.history(period=period, interval=interval)

    fig, ax = plt.subplots()

    ax.plot(data.index, data['Close'], linewidth=2)

    ax.set_title(f"{stock_option} Price Chart", fontsize=14)
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")

    ax.grid(True)

    st.pyplot(fig)

    # Stock Info
    st.subheader("Stock Info")

    st.write("Latest Price:", data['Close'].iloc[-1])
    st.write("Highest Price:", data['High'].max())
    st.write("Lowest Price:", data['Low'].min())

# COMPARE MODE

else:
    stocks = st.multiselect(
        "Select Stocks to Compare",
        ["RELIANCE.NS", "TCS.NS", "INFY.NS"]
    )

    if stocks:
        fig, ax = plt.subplots()

        for stock_name in stocks:
            stock = yf.Ticker(stock_name)
            data = stock.history(period=period, interval=interval)
            ax.plot(data.index, data['Close'], label=stock_name, linewidth=2)

        ax.set_title("Stock Comparison", fontsize=14)
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")

        ax.grid(True)
        ax.legend()

        st.pyplot(fig)