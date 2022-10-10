# Add user use cases related program logic in this file

# import Pandas, SQL, Questionary libraries to work with this file
import sqlalchemy as sql
import pandas as pd
import questionary as qs
from questionary import Validator, ValidationError, prompt

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

# function to request user to input user name and password
def request_user_credentials():
    user_name = qs.text(
        "Please enter your username",
        validate=NameValidator
    ).ask()
  
    user_password = qs.text(
        "Please enter your password"
    ).ask()
    user_df = pd.DataFrame({'user_name' : user_name, 'user_password': user_password}, index=[0])
    return user_df

# Define function to initiate the user authentication module (Sign up, sign in etc)
def load_authentication():
    print('.....inside load authentication......')
     # Create a database connection string
    db_connection_string = 'sqlite:///./resources/app.db'
    
    # Create a database engine
    db_engine = sql.create_engine(db_connection_string)
    
    # Check if user table already exists; if not, create one
    if len(db_engine.table_names()) == 0:
        create_user_table = """
        CREATE TABLE user (
            user_name VAR PRIMARY KEY,
            user_password VAR,
            user_available_to_trade DOUBLE
        )
        """
        db_engine.execute(create_user_table)
    
      
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
                user_available_to_trade = qs.text("Please enter amount you rish to trade with").ask()
                user_df['user_available_to_trade'] = user_available_to_trade
                # add user details into the database
                user_df = create_user(user_df,db_engine)
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
                user_df = sign_in_user(user_df,db_engine)
                break
            except Exception as ex:
                print(ex)
        
    print('.....End of load authentication......')
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
    elif user_db_df['user_name'].iloc[0] == user_df['user_name'].iloc[0]:
        print('Login unsuccessful')
        print('Incorrect user password. Please enter correct password.')
        raise Exception('xyz', 'abc')
    else:
        print('Login unsuccessful')
        print('Incorrect user name. Please enter correct user name or sign up.')
    return user_db_df

# function to update user details into the database in user table
def update_user_fund(user_df):
    return True

# function to delete user from the database (from user table)
def delete_user(user_df):
    return True