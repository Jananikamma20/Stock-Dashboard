import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.title("📈 Stock Dashboard")

mode = st.radio("Select Mode", ["Single Stock", "Compare Stocks"])

# SINGLE STOCK MODE

if mode == "Single Stock":
    stock_option = st.selectbox(
        "Select a Stock",
        ("RELIANCE.NS", "TCS.NS", "INFY.NS")
    )

    stock = yf.Ticker(stock_option)
    data = stock.history(period="1d", interval="5m")

    fig, ax = plt.subplots()
    ax.plot(data.index, data['Close'])

    ax.set_title(f"{stock_option} Price Chart")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")

    st.pyplot(fig)

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
            data = stock.history(period="1d", interval="5m")
            ax.plot(data.index, data['Close'], label=stock_name)

        ax.set_title("Stock Comparison")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")
        ax.legend()

        st.pyplot(fig)