import pandas as pd
import yfinance as yf
import numpy as np
import questionary as qs
from MCForecastTools import MCSimulation
from portfolio.portfolio import perform_analysis
from report.report import prepare_stock_report

# function to perform stock analysis (historical, present plus future analysis)
# user_df contains : user name, user password, available fund to trade
# portfolio_df  contains : tickers, number of shares for each ticker
# user_stock variable is stock tickername that user wishes to perform analysis for
# user_stock_weight variable is potential weigth in the portfolio user wishes to analyse
def perform_stock_analysis(user_df, portfolio_df):
    print('you are herer...')
    while True:
        try:
            user_stock = qs.text(
                    "Please enter the stock you would like to analyze"
            ).ask().upper()
            
            ticker = yf.Ticker(user_stock)
            if (ticker.info['regularMarketPrice'] == None):
                raise NameError("You did not input a correct stock ticker! Try again.")
            break
        except Exception as ex:
            print(ex)
            
    while True:
        try:
            user_stock_weight = float(qs.text(
                "Please enter the potential weight you have in mind for this stock in your portfolio"
            ).ask())
            if(user_stock_weight>1):
                raise NameError("Stock's weight can not be greater than 1")
            break
        except Exception as ex:
            print(ex)
    
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

