import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st.markdown(
    "<h1 style='text-align: center; color: #00FFAA;'>📊 Stock Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown("### Analyze stock trends and compare performance easily")
st.markdown("🟢 Live Market Data")


st.sidebar.title("📊 Dashboard Controls")
st.sidebar.markdown("Customize your analysis")
refresh_rate = st.sidebar.slider("Refresh Interval (seconds)", 2, 10, 5)

st.caption(f"🔄 Auto-refreshing every {refresh_rate} seconds")

st_autorefresh(interval=refresh_rate * 1000, key="datarefresh")

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

    if not data.empty:

        latest_price = data['Close'].iloc[-1]
        prev_price = data['Close'].iloc[-2]

        change = latest_price - prev_price
        percent = (change / prev_price) * 100

        col1, col2, col3 = st.columns(3)

        col1.metric("💰 Current Price", round(latest_price, 2), f"{round(percent,2)}%")
        col2.metric("📈 High", round(data['High'].max(), 2))
        col3.metric("📉 Low", round(data['Low'].min(), 2))

        price_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
        percent_change = (price_change / data['Close'].iloc[-2]) * 100

        st.metric(
            label="📊 Price Change",
            value=f"{round(price_change,2)}",
            delta=f"{round(percent_change,2)}%"
        )

    if data.empty:
        st.warning("No data available. Try different settings.")
    else:
        data['MA_20'] = data['Close'].rolling(window=20).mean()
        data['Returns'] = data['Close'].pct_change()

        st.markdown("---")
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name='Close Price'
        ))

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['MA_20'],
            mode='lines',
            name='Moving Avg (20)'
        ))
        fig.update_layout(
            title=f"{stock_option} Price Chart",
            xaxis_title="Time",
            yaxis_title="Price",
            hovermode='x unified',
            template="plotly_dark",
            margin=dict(l=10, r=10, t=40, b=10)
        )

        st.plotly_chart(fig, width='stretch')

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
    st.subheader("📊 Compare Multiple Stocks")
    if selected_names:

        fig = go.Figure()

        for name in selected_names:
            stock = yf.Ticker(stocks_list[name])
            data = stock.history(period=period, interval=interval)

            if data.empty:
                st.warning(f"No data for {name}")
                continue

            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name=name
            ))

        fig.update_layout(
            title="Stock Comparison",
            xaxis_title="Time",
            yaxis_title="Price",
            hovermode='x unified',
            template="plotly_dark"
        )
        st.plotly_chart(fig, width='stretch')