import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Config:
    # Read the single DATABASE_URL variable
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False