import os
from dotenv import load_dotenv
from linkedin_api import Linkedin

load_dotenv()

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

def get_user_info(profile_url):
    # Extract the vanity name from the URL
    vanity_name = profile_url.split('/')[-1]
    
    # Authenticate with LinkedIn
    api = Linkedin(email, password)
    
    # Get the user's profile information
    user_info = api.get_profile(vanity_name)
    
    # Print the user's profile information
    print("\n")
    for key, value in user_info.items():
        print(f"{key}: {value}")
        print("\n")

# Ask the end user for the profile URL
profile_url = input("Enter the LinkedIn profile URL: ")
get_user_info(profile_url)