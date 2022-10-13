# function to perform either buy or sell transaction
# user_trade_choice = Buy or Sell
# user_df contains - user name, user password, available amount to trade, portfolio_df (portfolio details stock names, # of stocks)
import questionary as qs
import pandas as pd

def perform_trade_stock(user_trade_choice,user_df):
    
    # Ask user which stock it would like to trade
    user_stock = qs.text(
            f'Please enter the stock you would like to {user_trade_choice}'
    ).ask()
    
    # Ask user how many shares of the given stock it would like to trade
    no_of_stock = float(qs.text(
            f'Please enter the number of shares you would like to {user_trade_choice}'
    ).ask())
    
    # Get stock's current price using alpaca sdk; right now just adding dummy price of 100
    current_stock_price = 100
    
    # calculate total trade amount
    trade_amount = no_of_stock*current_stock_price
    user_available_to_trade = float(user_df['user_available_to_trade'].iloc[0])
    
    # check if user's available trade amount is greater than stock trade amount 
    pd.options.mode.chained_assignment = None
    if user_available_to_trade > trade_amount:
        user_df['user_available_to_trade'].iloc[0] = user_available_to_trade - trade_amount
        print(f'You have successfully executed order to: {user_trade_choice} {no_of_stock} {user_stock}')
    else:
        print(f'You have insufficient available amount to trade. You need more than {trade_amount} to complete this transaction')

    return user_df