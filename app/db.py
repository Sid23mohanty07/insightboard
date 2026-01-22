from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["insightboard"]

jobs_collection = db["jobs"]
graphs_collection = db["dependency_graphs"]
