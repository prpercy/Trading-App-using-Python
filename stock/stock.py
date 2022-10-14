# function to perform stock analysis (historical, present plus future analysis)
# user_df contains : user name, user password, available fund to trade
# portfolio_df  contains : tickers, number of shares for each ticker
# user_stock variable is stock tickername that user wishes to perform analysis for

import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from datetime import date, timedelta

def perform_stock_analysis(user_stock, portfolio_df, user_df):
    
    #get the user_stock prices n daily returns for past 3 years using alpaca
    # similarly get details of S&P 500 and stocks in the portfolio_df
    # perform risk return calculations
    
    # prepare stock list for which we wish to retrieve data
    tickers = [user_stock]
    tickers.extend(portfolio_df['ticker'].tolist())
    tickers.append('SPY')
    
    
    
    return True

