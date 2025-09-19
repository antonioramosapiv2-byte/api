import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")


def connect():
    return create_client(url, key)
