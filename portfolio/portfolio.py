# function to perform portfolio analysis (historical, present plus future analysis)
# portfolio_df contains:stock names, outstanding holding of each stock (e.g. 10 stocks of GOOG, 13 stocks of FB etc)
# user_df contains : user name, user password, available fund to trade

def perform_portfolio_analysis(user_df, portfolio_df):
    
    # get the list of all stock names in the user portfolio and also add SPY in it
    tickers = portfolio_df['ticker'].tolist()
    tickers.append('SPY')
    
    # use yahoo finance to retrieve 5 yrs of price data
    
    # use pct_change to convert into returns
    
    # once u have returns - u can calculate beta (risk free return / std dev), std, cumulative returns (cumprod), variance/covariance(.var() and .cov(),
    # sharpe ratio, sortino ratio
    # monte carlo output from liset's function
    
    
    
    # put all these results in dataframe(s) in a format agreed with Esteban
    # call Report function from Esteban's file
    
    return True