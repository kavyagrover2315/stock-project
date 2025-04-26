import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 🛑 Page configuration
st.set_page_config(page_title="Stock Insight", layout="centered")

# 📋 App title
st.title("📈 Stock Insight")
st.write("Analyze your favorite stock with powerful charts, technical indicators, and predictions 🚀")

# 📥 Input
stock_input = st.text_input('Enter Stock Symbol (example: AAPL, TSLA, RELIANCE.NS)', 'AAPL').upper()

# 📅 Date range
start_date = st.date_input('Start Date', pd.to_datetime('2020-01-01'))
end_date = st.date_input('End Date', pd.to_datetime('2025-01-01'))

if stock_input:
    try:
        data = yf.download(stock_input, start=start_date, end=end_date)

        if data.empty:
            st.warning("No data found for this stock symbol.")
        else:
            st.success(f"Showing data for {stock_input}")

            st.subheader("📄 Last 15 Days of Data")
            st.dataframe(data.tail(15))  # ⬅️ Showing last 15 days instead of 5

            st.divider()

            # 📈 Closing Price Chart
            st.subheader("📈 Closing Price Over Time")
            fig, ax = plt.subplots()
            ax.plot(data.index, data['Close'], color='blue', label='Closing Price')
            ax.set_xlabel("Date")
            ax.set_ylabel("Price ($)")
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

            st.divider()

            # 📊 Volume Chart
            st.subheader("📊 Volume Traded")
            st.bar_chart(data['Volume'])

            st.divider()

            # 📈 Moving Averages
            st.subheader("📈 20-Day Simple and Exponential Moving Averages")
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()

            fig_ma, ax_ma = plt.subplots()
            ax_ma.plot(data.index, data['Close'], label='Closing Price', color='blue')
            ax_ma.plot(data.index, data['SMA_20'], label='20-day SMA', color='green')
            ax_ma.plot(data.index, data['EMA_20'], label='20-day EMA', color='red')
            ax_ma.set_xlabel("Date")
            ax_ma.set_ylabel("Price ($)")
            ax_ma.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig_ma)

            st.divider()

            # 📈 High and Low Price Chart (Instead of Candlestick)
            st.subheader("📈 High and Low Prices Over Time")
            fig_hl, ax_hl = plt.subplots()
            ax_hl.plot(data.index, data['High'], label='High Price', color='green')
            ax_hl.plot(data.index, data['Low'], label='Low Price', color='red')
            ax_hl.set_xlabel("Date")
            ax_hl.set_ylabel("Price ($)")
            ax_hl.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig_hl)

            st.divider()

            # 🔮 Simple Prediction (based on EMA)
            st.subheader("🔮 Simple Prediction")

            try:
                current_price = float(data['Close'].iloc[-1])
                ema_price = float(data['EMA_20'].iloc[-1])

                st.markdown(f"**Current Price:** ${current_price:.2f}")
                st.markdown(f"**20-Day EMA:** ${ema_price:.2f}")

                if current_price > ema_price:
                    st.success(f"📈 {stock_input} is showing an upward trend based on EMA.")
                else:
                    st.error(f"📉 {stock_input} is showing a downward trend based on EMA.")

            except Exception as e:
                st.error(f"Prediction error: {str(e)}")

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
else:
    st.info("Please enter a stock symbol to proceed.")
