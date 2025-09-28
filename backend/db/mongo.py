from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pymongo.server_api import ServerApi

load_dotenv()


client = MongoClient(os.getenv("MONGO_DB"), server_api=ServerApi('1'))
client.admin.command("ping")
db = client["Eirene"]