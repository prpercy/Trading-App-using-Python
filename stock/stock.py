# function to perform stock analysis (historical, present plus future analysis)
# user_df contains : user name, user password, available fund to trade
# portfolio_df  contains : tickers, number of shares for each ticker
# user_stock variable is stock tickername that user wishes to perform analysis for

import pandas as pd
import yfinance as yf
import numpy as np
from MCForecastTools import MCSimulation
from portfolio.portfolio import perform_analysis
from report.report import prepare_stock_report

def perform_stock_analysis(user_stock, portfolio_df, user_df):
    
    #get the user_stock prices n daily returns for past 3 years using alpaca
    # similarly get details of S&P 500 and stocks in the portfolio_df
    # perform risk return calculations
    
    # prepare stock list for which we wish to retrieve data
    if user_stock in portfolio_df['ticker'].tolist():
        print('stock is already in portfolio')
        tickers = []
    else:
        tickers = [user_stock]
        
    
    tickers.extend(portfolio_df['ticker'].tolist())
    tickers.append('SPY')
    
    results_dict = perform_analysis(user_stock,tickers, user_df, portfolio_df, 'stock')
    
    # prepare the analysis report
    prepare_stock_report(results_dict)
    
    return True

