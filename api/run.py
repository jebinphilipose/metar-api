from api import create_app
from dotenv import load_dotenv

# Export environment variables from .env file
load_dotenv('../.env')

app = create_app()
