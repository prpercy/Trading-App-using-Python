import pandas as pd
import yfinance as yf
import numpy as np
from MCForecastTools import MCSimulation
from portfolio.portfolio import perform_analysis
from report.report import prepare_stock_report

# function to perform stock analysis (historical, present plus future analysis)
# user_df contains : user name, user password, available fund to trade
# portfolio_df  contains : tickers, number of shares for each ticker
# user_stock variable is stock tickername that user wishes to perform analysis for
# user_stock_weight variable is potential weigth in the portfolio user wishes to analyse
def perform_stock_analysis(user_stock, user_stock_weight, portfolio_df, user_df):
    
    # prepare stock list for which we wish to retrieve data
    if user_stock in portfolio_df['ticker'].tolist():
        print('This stock is already in your portfolio!')
        tickers = []
    else:
        tickers = [user_stock]
        
    
    tickers.extend(portfolio_df['ticker'].tolist())
    # add S&P 500 ticker to the list for analysis purpose
    tickers.append('SPY')
    
    # call perform analysis function that provides all the results in a dictionary
    results_dict = perform_analysis(user_stock,user_stock_weight, tickers, user_df, portfolio_df, 'stock')
    
    # prepare the stock analysis report
    prepare_stock_report(results_dict)
    
    return True

