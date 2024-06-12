import os
from dotenv import load_dotenv

def load_environment():
    if os.getenv('AWS_LAMBDA_FUNCTION_NAME'):
        # Running in Lambda, assume environment variables are already set
        return
    else:
        # Running locally, load environment variables from .env file
        load_dotenv()
        print("Environment variables loaded from .env file")