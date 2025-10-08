import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID', 0))
MAX_WARNS = int(os.getenv('MAX_WARNS', 3))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file")

if OWNER_ID == 0:
    raise ValueError("OWNER_ID not found in .env file")
