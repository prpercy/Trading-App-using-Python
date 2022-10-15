# function to perform portfolio analysis (historical, present plus future analysis)
# portfolio_df contains:stock names, outstanding holding of each stock (e.g. 10 stocks of GOOG, 13 stocks of FB etc)
# user_df contains : user name, user password, available fund to trade

import pandas as pd
import yfinance as yf
import numpy as np

def perform_portfolio_analysis(user_df, portfolio_df):
    
    # get the list of all stock names in the user portfolio and also add SPY in it
    tickers = portfolio_df['ticker'].tolist()
    tickers.append('SPY')
    portfolio_dic = dict()
    for ticker in portfolio_df['ticker'].tolist():
        portfolio_dic[ticker.upper()] = portfolio_df[portfolio_df['ticker']==ticker]['number_of_shares'].iloc[0]

    # use yahoo finance to retrieve 5 yrs of price data
    portfolio = yf.Tickers(tickers)
    portfolio_history_df = portfolio.history(period = "5y")
    prices_df = portfolio_history_df["Close"]
    prices_df['PORTFOLIO'] = (prices_df[portfolio_df['ticker'].tolist()].mul(portfolio_dic)).sum(axis=1)
    
    

    # use pct_change to convert into returns
    returns_df = prices_df.pct_change().dropna()
    
    print(prices_df.head())
    print(returns_df.tail())
    
    std_devs = returns_df.std()
    
    number_of_trading_days = 252
    annualized_std_devs = std_devs*np.sqrt(number_of_trading_days)
    
    print(std_devs)
    print(annualized_std_devs)
    
    rolling_std_60d = returns_df.rolling(window=60).std().dropna()

    
    # once u have returns - u can calculate beta (risk free return / std dev), std, cumulative returns (cumprod), variance/covariance(.var() and .cov(),
    # sharpe ratio, sortino ratio
    # monte carlo output from liset's function
    
    
    
    # put all these results in dataframe(s) in a format agreed with Esteban
    # call Report function from Esteban's file
    
    return True