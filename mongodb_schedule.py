from dotenv import load_dotenv
import os

import pymongo
from pymongo import MongoClient


load_dotenv()
DB_URI = os.environ.get('MONGODB_URI')

client = MongoClient(DB_URI)

db = client['scheduler']
collection = db['schedules']