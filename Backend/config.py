import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL')
    # DATABASE_USER = os.getenv('DATABASE_USER')
    # DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')