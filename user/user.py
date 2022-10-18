# Add user use cases related program logic in this file

# import Pandas, SQL, Questionary libraries to work with this file
import sqlalchemy as sql
import pandas as pd
import questionary as qs
import utils
from portfolio.portfolio import perform_portfolio_analysis
from stock.stock import perform_stock_analysis
from stock.trade import perform_trade_stock

#user5



# Define function to initiate the user authentication module (Sign up, sign in etc)
def load_authentication():
    print('.....Inside authentication module......')

    db_engine = utils.get_db_engine()
    
    # Check if user table already exists; if not, create one
    if len(db_engine.table_names()) == 0:
        utils.initiate_database_tables(db_engine)
     
    new_user_choices = ['Yes', 'No']
    # ask whether its a new user
    new_user = qs.select(
        "Are you a new user?",
        choices=new_user_choices
    ).ask()
    
    user_df = pd.DataFrame()
    
    if new_user == 'Yes':
        # if its a new user, start the sign up process
        print('Please sign up')
        while True:
            try:
                user_df = request_user_credentials()
                user_available_to_trade = qs.text("Please enter amount you wish to trade with").ask()
                user_df['user_available_to_trade'] = user_available_to_trade
                # add user details into the database
                user_df = create_user(user_df,db_engine)
                portfolio_df = pd.DataFrame(columns=['ticker', 'number_of_shares'])
                break
            except Exception as ex:
                print(ex)
                print(f" User name {user_df['user_name'].iloc[0]} already exists. Please enter another user name")
    else:
        # for existing user please initiate the sign in process
        print('Please sign in')
        while True:
            try:
                user_df = request_user_credentials()
                # check if user is in db..if not raise incorrect username or password error
                user_df, portfolio_df = sign_in_user(user_df,db_engine)
                break
            except Exception as ex:
                print(ex)
        
    print('.....End of authentication module......')
    return user_df, portfolio_df


# function to load user options
def load_user_options():
    signed_in_user_choices = [
        'Update available amount for trading', 
        'Trade Stocks', 
        'View current portfolio',
        'Stock Analysis',
        'Portfolio Analysis', 
        'Delete User', 
        'Exit the application'
    ]
    
    user_choice = qs.select(
        "What would you like to do?",
        choices=signed_in_user_choices
    ).ask()
       
    return user_choice




# function to load user options
def execute_user_choice(user_df, portfolio_df, user_choice):
    pd.options.mode.chained_assignment = None
    
    if user_choice == 'Update available amount for trading':
        user_funds = qs.text(
            "Please enter the amount you would like to trade"
        ).ask()
    
        user_df['user_available_to_trade'].iloc[0] = user_funds
        user_df = update_user_fund(user_df)
        print(f'User {user_df["user_name"].iloc[0]} available trade amount is updated to {user_df["user_available_to_trade"].iloc[0]}')
        print('updated the funds into database')
        
    elif user_choice == 'Stock Analysis':
        print('perform stock analysis')
        user_stock = qs.text(
            "Please enter the stock you would like to analyze"
        ).ask().upper()
        perform_stock_analysis(user_stock, portfolio_df, user_df)
        
    elif user_choice == 'Portfolio Analysis':
        print('perform portfolio analysis...')
        perform_portfolio_analysis(user_df, portfolio_df)
        
    elif user_choice == 'Trade Stocks':
        trade_stock_choices = ['Buy', 'Sell']
        user_trade_choice = qs.select(
            "What would you like to do?",
            choices=trade_stock_choices
        ).ask()
        user_df, portfolio_df = perform_trade_stock(user_trade_choice,user_df, portfolio_df)
        
    elif user_choice == 'View current portfolio':
        print(portfolio_df.to_markdown())
        print(f" Cash available to trade is {user_df['user_available_to_trade'].iloc[0]}")
        
    elif user_choice == 'Delete User':
        delete_user(user_df)
        exit()
        
    else:
        exit()
       
    return user_df, portfolio_df

# update user fund
def update_user_fund(user_df):
    
    # update user details into the database in user table
    db_engine = utils.get_db_engine()
    
    user_query = f"""
    UPDATE user 
    SET user_available_to_trade = '{user_df['user_available_to_trade'].iloc[0]}'
    WHERE user_name ='{user_df['user_name'].iloc[0]}'
    """
    db_engine.execute(user_query)
    
    return user_df


# function to request user to input user name and password
def request_user_credentials():
    user_name = qs.text(
        "Please enter your username",
        validate=utils.NameValidator
    ).ask()
  
    user_password = qs.text(
        "Please enter your password"
    ).ask()
    user_df = pd.DataFrame({'user_name' : user_name, 'user_password': user_password}, index=[0])
    return user_df



# function to inser user details into database
def create_user(user_df,db_engine):
    user_query = f"""
    INSERT INTO 
        user (user_name, user_password, user_available_to_trade)
    VALUES 
        ('{user_df['user_name'].iloc[0]}', '{user_df['user_password'].iloc[0]}', {user_df['user_available_to_trade'].iloc[0]})
    """
    db_engine.execute(user_query)
      
    return user_df

# function to read user details from database
def sign_in_user(user_df, db_engine):
    user_query = f"""
    SELECT 
        user_name, user_password, user_available_to_trade 
    FROM 
        user 
    WHERE user_name ='{user_df['user_name'].iloc[0]}'
    """
    user_db_df = pd.read_sql_query(user_query, db_engine)
     
    if user_db_df['user_password'].iloc[0] == user_df['user_password'].iloc[0]:
        print('Login successful')
        print(f'Funds available to trade for you are {user_db_df["user_available_to_trade"].iloc[0]}')
        
        # retrieve user portfolio details
        user_portfolio_query = f"""
            SELECT 
                ticker, number_of_shares 
            FROM 
                portfolio 
            WHERE user_name ='{user_df['user_name'].iloc[0]}'
        """
        portfolio_df = pd.read_sql_query(user_portfolio_query, db_engine)
        print(portfolio_df.to_markdown())
        
        
    elif user_db_df['user_name'].iloc[0] == user_df['user_name'].iloc[0]:
        print('Login unsuccessful')
        print('Incorrect user password. Please enter correct password.')
        raise Exception('xyz', 'abc')
    else:
        print('Login unsuccessful')
        print('Incorrect user name. Please enter correct user name or sign up.')
    return user_db_df, portfolio_df


# function to delete user from the database (from user table)
def delete_user(user_df):
    db_engine = utils.get_db_engine()
    
    user_query = f"""
    DELETE FROM user 
    WHERE user_name ='{user_df['user_name'].iloc[0]}'
    """
    db_engine.execute(user_query)
    
    user_portfolio_query = f"""
        DELETE FROM portfolio WHERE user_name = '{user_df['user_name'].iloc[0]}'
    """
    db_engine.execute(user_portfolio_query)
    
    print(f'User {user_df["user_name"].iloc[0]} and respective portfolio details are successfully deleted from the database.')
    return True