from google.genai import Client
from dotenv import load_dotenv
import os
from pathlib import Path

# load .env from project folder
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

print("GOOGLE_API_KEY present:", bool(os.getenv("GOOGLE_API_KEY")))

client = Client(api_key=os.getenv("GOOGLE_API_KEY"))
for m in client.models.list():
    print(m.name)