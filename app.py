import fire
import questionary as qs
import sqlalchemy as sql
from user.user import load_authentication
from finta import TA

def request_user_service():
    

        
            
def run():
    """The main function for running the script."""
  
    # Run user authentication program
    user_df = load_authentication()
    
    print(user_df.head())
    # Ask what would user like to do next, namely, 
    #  (1) trade (2) update user available fund to trade (3) delete the user (4) analyse the portfolio if exists (5) generate reports
    
    request_user_service()
   
    

if __name__ == "__main__":
    fire.Fire(run)
