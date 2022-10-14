import yfinance as yf
from finta import TA
import pandas as pd
from questionary import Validator, ValidationError, prompt
import matplotlib.pyplot as plt

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