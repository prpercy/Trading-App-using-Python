# function to perform either buy or sell transaction
# user_trade_choice = Buy or Sell
# user_df contains - user name, user password, available amount to trade
# portfolio_df (portfolio details : stock names, # of stocks)

import questionary as qs
import pandas as pd

def perform_trade_stock(user_trade_choice,user_df, portfolio_df):
    
    # Ask user which stock it would like to trade
    user_stock = qs.text(
            f'Please enter the stock you would like to {user_trade_choice}'
    ).ask()
    
    # Ask user how many shares of the given stock it would like to trade
    no_of_stock = float(qs.text(
            f'Please enter the number of shares you would like to {user_trade_choice}'
    ).ask())
    
    # Get stock's current price using alpaca sdk; right now just adding dummy price of 100
    current_stock_price = 100 # write actual code here to get current price
    
    # calculate total trade amount
    trade_amount = no_of_stock*current_stock_price
    user_available_to_trade = float(user_df['user_available_to_trade'].iloc[0])
    
    if user_trade_choice == 'Buy':
        # check if user's available trade amount is greater than stock trade amount 
        pd.options.mode.chained_assignment = None
        if user_available_to_trade >= trade_amount:
            user_df['user_available_to_trade'].iloc[0] = user_available_to_trade - trade_amount
            print(f'You have successfully executed order to: {user_trade_choice} {no_of_stock} {user_stock}')
            portfolio_df = portfolio_df.append({'ticker': user_stock, 'number_of_shares' : no_of_stock}, ignore_index=True)
            print(portfolio_df)
            
        else:
            print(f'You have insufficient available amount to trade. You need more than {trade_amount} to complete this transaction')
    else:
        # check if user portfolio has those stocks to sell at the present (no naked short permissible at this moment)
        idx = portfolio_df.index[portfolio_df['ticker'] == user_stock]
        number_of_shares = float(portfolio_df[portfolio_df['ticker'] == user_stock]['number_of_shares'])
     
        if no_of_stock >= number_of_shares:
            print(f' You sold {number_of_shares} stocks of {user_stock}')
            portfolio_df = portfolio_df.drop(idx)
            trade_amount = number_of_shares*current_stock_price
        else:
            print(f' You sold {no_of_stock} stocks of {user_stock}')
            portfolio_df.at[idx, 'number_of_shares'] = number_of_shares - no_of_stock
          
        # since its a sell. increase the available trade amount by sales proceeds
        user_df['user_available_to_trade'].iloc[0] = user_available_to_trade + trade_amount
        
     # write a code to save this portfolio_df into PORTFOLIO table  
     # currently the portfolio_df only has tickers and number of shares data..it does not have user_name...user_name can be found in user_df
     # so you have to create a new df let us say portfolio_db_df which has all 3 elements -tickers, number of shares and user name
     # then u can use dataframe.to_sql method to save it in db.
    
    return user_df, portfolio_df