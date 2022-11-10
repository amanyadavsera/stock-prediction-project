import datetime as dt
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import mpld3
import streamlit.components.v1 as components
from keras.models import load_model
import streamlit as st

st.set_page_config(layout="wide")


def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: linear-gradient( rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0.85) ), url('https://i.imgur.com/kn89PXn.jpg');
             background-attachment: fixed;
             background-size: cover;
            }}
         </style>
         """,
        unsafe_allow_html=True
    )


# comment this out to remove the background image
add_bg_from_url()

with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.markdown('<p class="disclaimer">DISCLAIMER: This is a novice machine learning project solely intended for educational and informational purposes. The aim of this project is to demonstrate how machine learning can be potentially used in the finance sector. The predictions made through this model are not intended as, and should not be understood or construed as, financial advice. If anyone chooses to do so, the creators of this project should not be held liable for any potential loss or damage caused directly or indirectly through this project. Trading or investing is associated with a high level of risk and one should seek professional help and/or conduct his/her own research before making financial decisions.</p>', unsafe_allow_html=True)
st.markdown('<p class="top-header">stock trend forecasting</p>',
            unsafe_allow_html=True)

st.markdown('<p class="top-subheader">this web-based ML application makes a naive attempt to predict the closing prices of several stocks.</p>', unsafe_allow_html=True)

tickersSeries = pd.read_html(
    'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']
tickersList = tickersSeries.to_list()
tickersList.insert(0, '')


st.markdown('<p class="ticker-definition">"Ticker symbols are arrangements of symbols or characters that are generally English letters representing specific assets or securities listed on a stock exchange or traded publicly."</p>', unsafe_allow_html=True)
st.markdown('<p class="source">source - cleartax.in</p>',
            unsafe_allow_html=True)

st.markdown('<p class="selectBoxText">please select a stock ticker</p>',
            unsafe_allow_html=True)
stockTicker = st.selectbox("", options=tickersList)


selectionText = f"""<p class="selected">you have selected {stockTicker}</p>"""
warningText = f"""<p class="warning">no ticker is selected yet.</p>"""

startDate = dt.date(1960, 1, 1)
endDate = dt.date(1960, 1, 1)

if stockTicker == '':
    st.markdown(warningText, unsafe_allow_html=True)
else:
    st.markdown(selectionText, unsafe_allow_html=True)

    # taking the date inputs
    st.markdown('<p class="provide-date content">in order to fetch data to train the model you need to provide a certain range of dates</p>', unsafe_allow_html=True)
    startDate = st.date_input("provide the start date", min_value=dt.date(
        1960, 1, 1), max_value=dt.date.today(), key="startDate")
    endDate = st.date_input("provide the end date", min_value=dt.date(
        1960, 1, 1), max_value=dt.date.today(), key="endDate")

# ------------- input is done here ---------------------------

if stockTicker != '':
    rawStockData = yf.download(tickers=stockTicker, start=startDate, end=endDate)
    #rawStockData.reset_index(inplace=True)

    #rawStockData['Date'] = rawStockData['Date'].dt.normalize()

    text = f"""<p class="overview content">→ this is an overview of the data for the {stockTicker} stock from {startDate} to {endDate}</p>"""
    st.markdown(text, unsafe_allow_html=True)
    st.dataframe(data=rawStockData, width=1000)

    # plotting the closing price
    fig = plt.figure(figsize=(18, 8))
    plt.title('closing price history')
    plt.plot(rawStockData['Close'], linewidth=1, color='green')
    plt.xlabel('Date', fontsize=16)
    plt.ylabel(f'closing price USD for {stockTicker}', fontsize=16)
    st.pyplot(fig)

    # moving average
    st.markdown('<p class="moving-average content">Stock price behaviour</p>', unsafe_allow_html=True)
    st.markdown('<p class="moving-average-desc content">Moving averages are trend indicators of price behaviour over some time. This average is used to study price behaviour over the long term.</p>', unsafe_allow_html=True)
    st.markdown('<p class="moving-average-desc content">Traders and market analysts commonly use several periods in creating moving averages to plot their charts. For identifying significant, long-term support and resistance levels and overall trends, the 50-day, 100-day and 200-day moving averages are the most common. Based on historical statistics, these longer-term moving averages are considered more reliable trend indicators and less susceptible to temporary fluctuations in price. </p>', unsafe_allow_html=True)
    st.markdown('<p class="moving-average-desc content">→ A 200-day Moving Average (MA) is simply the average closing price of a stock over the last 200 days.</p>', unsafe_allow_html=True)
    st.markdown('<p class="moving-average-desc content">→ A 50-day Moving Average (MA) is simply the average closing price of a stock over the last 50 days.</p>', unsafe_allow_html=True)
    st.markdown('<p class="moving-average-desc content">As long as the 50-day moving average of a stock price remains above the 200-day moving average, the stock is generally thought to be in a bullish trend. A crossover to the downside of the 200-day moving average is interpreted as bearish.</p>', unsafe_allow_html=True)

    # plotting the moving averages
    MA50 = rawStockData.Close.rolling(50).mean()
    MA200 = rawStockData.Close.rolling(200).mean()

    fig = plt.figure(figsize = (18, 8))
    plt.plot(rawStockData.Close, 'green')
    plt.plot(MA50, 'red')
    plt.plot(MA200, 'blue')
    st.pyplot(fig)