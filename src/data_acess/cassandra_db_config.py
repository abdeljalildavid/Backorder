import os
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()


# Set up connection parameters using environment variables
ASTRA_DB_CLIENT_ID = os.getenv('ASTRA_DB_CLIENT_ID')
ASTRA_DB_CLIENT_SECRET = os.getenv('ASTRA_DB_CLIENT_SECRET')
ASTRA_DB_SECURE_BUNDLE_PATH = os.getenv('ASTRA_DB_BUNDLE_PATH')
KEYSPACE = 'backorder'

print(ASTRA_DB_CLIENT_ID)