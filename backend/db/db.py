from pymongo import MongoClient
from dotenv import load_dotenv
import os 
load_dotenv()
client = MongoClient(os.getenv("DB_URL"))
db = client["Lung_DB"]
users_collection = db["user"]
# Unique indexes
users_collection.create_index(
    "email",
    unique=True
)

users_collection.create_index(
    "username",
    unique=True
)