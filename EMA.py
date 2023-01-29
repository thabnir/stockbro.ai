import pandas as pd

from app import get_trend_data, get_stock_data, get_correlation


def EMA(word, ticker, start, end):

    # Get the data
    trend_data = get_trend_data(word, start + ' ' + end)
    stock_data = get_stock_data(ticker, start, end)

    correlation, net_data = get_correlation(trend_data[word], stock_data['Close'])
    print(net_data.head())
    if pd.isna(correlation):
        correlation = 'Not enough data'

    #Exponential moving average
    ema = net_data[word].ewm(com=0.5).mean()
    net_data['ema'] = ema
    
    return net_data
