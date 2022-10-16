# function to perform portfolio analysis (historical, present plus future analysis)
# portfolio_df contains:stock names, outstanding holding of each stock (e.g. 10 stocks of GOOG, 13 stocks of FB etc)
# user_df contains : user name, user password, available fund to trade

import pandas as pd
import yfinance as yf
import numpy as np
from MCForecastTools import MCSimulation
from report.report import prepare_portfolio_report

def perform_portfolio_analysis(user_df, portfolio_df):
    
    # get the list of all stock names in the user portfolio and also add SPY in it
    tickers = portfolio_df['ticker'].tolist()
    tickers.append('SPY')

    results_dict = perform_analysis(np.nan, tickers, user_df, portfolio_df, 'portfolio')
    
    # prepare the analysis report
    prepare_portfolio_report(results_dict)
    
    return True


def perform_analysis(user_stock, tickers, user_df, portfolio_df, indicator):
    
    portfolio_dic = dict()
    for ticker in portfolio_df['ticker'].tolist():
        portfolio_dic[ticker.upper()] = portfolio_df[portfolio_df['ticker']==ticker]['number_of_shares'].iloc[0]

    # use yahoo finance to retrieve 5 yrs of price data
    portfolio = yf.Tickers(tickers)
    portfolio_history_df = portfolio.history(period = "5y")
    prices_df = portfolio_history_df["Close"]
    portfolio_prices_df = prices_df[portfolio_df['ticker'].tolist()].mul(portfolio_dic)
    prices_df['PORTFOLIO'] = portfolio_prices_df.sum(axis=1)
    
    # use pct_change to convert into returns
    returns_df = prices_df.pct_change().dropna()

    
    # once u have returns - u can calculate beta (risk free return / std dev), std, cumulative returns (cumprod), 
    # variance/covariance(.var() and .cov(),
    # sharpe ratio, sortino ratio
    # monte carlo output from liset's function
    
    std_devs = returns_df.std()
    number_of_trading_days = 252
    annualized_std_devs = std_devs*np.sqrt(number_of_trading_days)
    # rolling_std_60d = returns_df.rolling(window=60).std().dropna()

    # Stock Covariance Calculation into a df
    covariance_df = returns_df.cov()
    covariance_df = covariance_df[["SPY"]]
    covariance_df.columns = ["Covariance"]

    #variance calculation
    spy_variance = returns_df['SPY'].var()

    # Beta calculation into a df
    beta_df = returns_df.cov()/spy_variance
    beta_df = beta_df[["SPY"]]
    beta_df.columns = ["Beta"]
    
    # Calculate the annual average return data for the for the portfolio and the S&P 500
    annualized_average_returns = returns_df.mean()*number_of_trading_days
    
    # Calculate the annualized Sharpe Ratios for the portfolio and the S&P 500.
    sharpe_ratios = annualized_average_returns/annualized_std_devs

    #Create df starting by correlation
    ratios_df = returns_df.corr()
    
    #drop columns for correlation against each other, leave only correlation against SPY i.e. S&P 500
    ratios_df = ratios_df[['SPY']]
    
    #rename column from SPY to Correlation
    ratios_df.rename(columns = {"SPY":"Correlation"},inplace = True) 

    #calculate additional ratios 
    ratios_df["Volatility"] = returns_df.std() * np.sqrt(252)
    ratios_df["Sharpe"] =  (returns_df.mean() * 252) / (returns_df.std() * np.sqrt(252))
    ratios_df["Sortino"] = (returns_df.mean() * 252) / (returns_df[returns_df<0].std() * np.sqrt(252))

    #add covariance and beta from calculation in cell above
    ratios_df["Covariance"] = covariance_df["Covariance"]
    ratios_df["Beta"] = beta_df["Beta"]
    

    
    # prepare for monte carlo simulation
    if indicator == 'portfolio':
        sim_input_prices_df = prices_df[portfolio_df['ticker'].tolist()]
        column_names = [(x,"close") for x in portfolio_df['ticker'].tolist()]
        # print(column_names)
        sim_input_prices_df.columns = pd.MultiIndex.from_tuples(column_names)

        # Calculate portfolio weights
        weights = ((portfolio_prices_df.iloc[-1]) / (prices_df['PORTFOLIO'].iloc[-1])).values
    else:
        # print('user stock is -->', user_stock)
        sim_input_prices_df = prices_df[[user_stock, 'PORTFOLIO']]
        column_names = [(user_stock,'close'), ('PORTFOLIO','close')]
        sim_input_prices_df.columns = pd.MultiIndex.from_tuples(column_names)

        # Calculate portfolio weights
        weights = [0.1,0.9]

    # Configure the Monte Carlo simulation to forecast 2 years cumulative returns
    # print(sim_input_prices_df.head())
    portfolio_2y_sim = MCSimulation(
        sim_input_prices_df,
        weights,
        num_simulation=100,
        num_trading_days=252*2
    )

    # run simulation
    portfolio_2y_sim.calc_cumulative_return()

    # put all these results in dictionary in a format agreed with Esteban
    # call Report function from Esteban's file

    results_dict = dict()
    results_dict['Prices'] = prices_df
    results_dict['Returns'] = returns_df
    results_dict['Ratios'] = ratios_df
    results_dict['MonteCarlo'] = portfolio_2y_sim
    
    return results_dict