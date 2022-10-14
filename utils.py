import yfinance as yf
from finta import TA
import pandas as pd
from questionary import Validator, ValidationError, prompt
import matplotlib.pyplot as plt
import sqlalchemy as sql

plt.style.use('fivethirtyeight')

# class definition to retrieve price data for particular ticker
class Database():
    def __init__(self, tickers, start_date, end_date):
        self.tickers = tickers
        data = yf.download(tickers, start=start_date, end=end_date)
        self.df = pd.DataFrame(data)
        self.df['Date'] = pd.to_datetime(self.df.index)
        pd.set_option('display.max_columns', None)
        
    def quote(self):
        return self.df
    
# class definition to validate user name
class NameValidator(Validator):
    def validate(self, document):
        if len(document.text) == 0:
            raise ValidationError(
                message="Please enter a value",
                cursor_position=len(document.text),
            )
        elif len(document.text)> 8:
            raise ValidationError(
                message="Please enter a value that has length shorter than 8",
                cursor_position=len(document.text),
            )

# create database engine
def get_db_engine():
    # Create a database connection string
    db_connection_string = 'sqlite:///./resources/app.db'
    
    # Create a database engine
    db_engine = sql.create_engine(db_connection_string)
    
    return db_engine

# initiate database tables
def initiate_database_tables(db_engine):
    create_user_table = """
           CREATE TABLE user (
            user_name VAR PRIMARY KEY,
            user_password VAR,
            user_available_to_trade DOUBLE
        )
        """
    db_engine.execute(create_user_table)
        
    create_portfolio_table = """
        CREATE TABLE portfolio (
            id INT IDENTITY(1,1) PRIMARY KEY,
            ticker VAR,
            number_of_shares DOUBLE,
            user_name VAR,
            FOREIGN KEY (user_name) REFERENCES user(user_name)
        )
        """
    db_engine.execute(create_portfolio_table)
        
    return True