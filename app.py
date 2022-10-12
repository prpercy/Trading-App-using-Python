import fire
import questionary as qs
import sqlalchemy as sql
from user.user import load_authentication, load_user_options, execute_user_choice



        
            
def run():
    """The main function for running the script."""
  
    # Run user authentication program
    user_df = load_authentication()
    
    print(user_df.head())
    
    # present user choices after successful login
    user_choice = load_user_options()
    print(user_choice)
    
    execute_user_choice(user_df, user_choice)
    
    # Ask what would user like to do next, namely, 
    #  (1) trade stocks (2) update user available fund to trade (3) delete the user (4) analyse the stock or portfolio if exists
    
    #request_user_service()
   
    

if __name__ == "__main__":
    fire.Fire(run)