from dotenv import load_dotenv
import os

load_dotenv()

PORT = int(os.getenv('PORT'))