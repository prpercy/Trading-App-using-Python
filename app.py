import fire
import questionary as qs
import sqlalchemy as sql
from user.user import load_authentication, load_user_options, execute_user_choice

            
def run():
    """The main function for running the script."""
  
    # Run user authentication program
    user_df = load_authentication()
    
    print(user_df.head())
    
    while True:
        # present user choices after successful login
        # Ask what would user like to do next, namely, 
        # (1) Update available amount for trading (2) Stock Analysis (3) Portfolio Analysis (4) Trade Stocks 
        # (5) Delete User (6) Exit the application
        user_choice = load_user_options()
        
        # execute user choice
        execute_user_choice(user_df, user_choice)
        
        # only exit this loop when user wants to get out of application and chooses explicitly to do so.


if __name__ == "__main__":
    fire.Fire(run)