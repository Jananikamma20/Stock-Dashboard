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

        delta = data['Close'].diff()

        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()

        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))

        st.markdown("---")

        fig = go.Figure()
        color = '#00FFAA' if data['Close'].iloc[-1] > data['Close'].iloc[0] else '#FF4B4B'

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color=color, width=2.5, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(0,255,170,0.08)'
        ))

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['MA_20'],
            mode='lines',
            name='Moving Avg (20)',
            line=dict(color='#FF6B3D', width=2)
        ))

        fig.update_layout(
            title=f"{stock_name} Price Trend",
            xaxis_title="Time",
            yaxis_title="Price",
            template="plotly_dark",
            hovermode='x unified',
            margin=dict(l=10, r=10, t=40, b=10),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )

        fig.update_yaxes(
            range=[
                data['Close'].min() * 0.995,
                data['Close'].max() * 1.005
            ]
        )

        st.plotly_chart(fig, use_container_width=True)

        rsi_fig = go.Figure()

        rsi_fig.add_trace(go.Scatter(
            x=data.index,
            y=data['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color='#FFD700', width=2)
        ))

        # RSI levels
        rsi_fig.add_hline(y=70, line_dash="dash", line_color="red")
        rsi_fig.add_hline(y=30, line_dash="dash", line_color="green")

        rsi_fig.update_layout(
            title="RSI Indicator",
            template="plotly_dark",
            height=250,
            margin=dict(l=10, r=10, t=30, b=10),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )

        st.plotly_chart(rsi_fig, use_container_width=True)

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