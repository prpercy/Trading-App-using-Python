# function to perform either buy or sell transaction
# user_trade_choice = Buy or Sell
# user_df contains - user name, user password, available amount to trade
# portfolio_df (portfolio details : stock names, # of stocks)

import questionary as qs
import pandas as pd
import yfinance as yf
import utils

def perform_trade_stock(user_trade_choice,user_df, portfolio_df):
    
    while True:
        try:
            # Ask user which stock it would like to trade
            user_stock = qs.text(
                    f'Please enter the stock you would like to {user_trade_choice}'
            ).ask()

            # Ask user how many shares of the given stock it would like to trade
            no_of_stock = float(qs.text(
                    f'Please enter the number of shares you would like to {user_trade_choice}'
            ).ask())
    
            # Get stock's current price using alpaca sdk; right now just adding dummy price of 100
            current_stock_price = yf.Ticker(user_stock).history(period='1d')['Close'][0]
            break
        except Exception as ex:
            print(f'Incorrect stock Ticker name provided as input')
            print(ex)
         
    # calculate total trade amount
    trade_amount = no_of_stock*current_stock_price
    user_available_to_trade = float(user_df['user_available_to_trade'].iloc[0])
    
    # check if user portfolio has those stocks to buy/sell at the present (no naked short permissible at this moment)
    idx = portfolio_df.index[portfolio_df['ticker'] == user_stock]
    if (idx.size == 0) & (user_trade_choice == 'Sell'):
        print(f'You can not {user_trade_choice} {user_stock} as you do not have it in your portfolio')
        return user_df, portfolio_df
    
    if user_trade_choice == 'Buy':
        # check if user's available trade amount is greater than stock trade amount 
        if user_available_to_trade >= trade_amount:
            #once trade amount is confirmed for purchase, amount will be deducted from total trading funds
            user_df['user_available_to_trade'].iloc[0] = user_available_to_trade - trade_amount
            #will return message of successful order of a 'buy' with the 'number of shares' and the 'stock ticker'
            print(f'You have successfully executed order to: {user_trade_choice} {no_of_stock} {user_stock}')
            #
            if idx.size > 0:
                number_of_shares = float(portfolio_df[portfolio_df['ticker'] == user_stock]['number_of_shares'])
                portfolio_df.at[idx, 'number_of_shares'] = number_of_shares + no_of_stock
                portfolio_sql_query = f"""
                    UPDATE portfolio
                    SET number_of_shares = {number_of_shares + no_of_stock}
                    WHERE ticker = '{user_stock}' AND user_name = '{user_df['user_name'].iloc[0]}'
                """
            else:
                portfolio_df = portfolio_df.append({'ticker': user_stock, 'number_of_shares' : no_of_stock}, ignore_index=True)
                portfolio_sql_query = f"""
                    INSERT INTO
                         portfolio (ticker, number_of_shares, user_name)
                    VALUES
                        ('{user_stock}', {no_of_stock}, '{user_df['user_name'].iloc[0]}')
                """
                
            print(portfolio_df)
        else:
            print(f'You have insufficient available amount to trade. You need more than {trade_amount} to complete this transaction')
    else:
        number_of_shares = float(portfolio_df[portfolio_df['ticker'] == user_stock]['number_of_shares'])
        if no_of_stock >= number_of_shares:
            print(f' You sold {number_of_shares} stocks of {user_stock}')
            portfolio_df = portfolio_df.drop(idx)
            trade_amount = number_of_shares*current_stock_price
            portfolio_sql_query = f"""
                DELETE FROM portfolio WHERE ticker = '{user_stock}' AND user_name = '{user_df['user_name'].iloc[0]}'
            """
        else:
            print(f' You sold {no_of_stock} stocks of {user_stock}')
            portfolio_df.at[idx, 'number_of_shares'] = number_of_shares - no_of_stock
            portfolio_sql_query = f"""
                UPDATE portfolio
                SET number_of_shares = {number_of_shares - no_of_stock}
                WHERE ticker = '{user_stock}' AND user_name = '{user_df['user_name'].iloc[0]}'
            """
          
        # since its a sell. increase the available trade amount by sales proceeds
        user_df['user_available_to_trade'].iloc[0] = user_available_to_trade + trade_amount
    
    user_sql_query = f"""
    UPDATE user 
    SET user_available_to_trade = '{user_df['user_available_to_trade'].iloc[0]}'
    WHERE user_name ='{user_df['user_name'].iloc[0]}'
    """
    db_engine = utils.get_db_engine()
    db_engine.execute(portfolio_sql_query)
    db_engine.execute(user_sql_query)
    
    return user_df, portfolio_df