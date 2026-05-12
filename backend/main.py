from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

# Load .env
load_dotenv()

# Environment Variables
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# FastAPI App
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
client = MongoClient(MONGODB_URI)

db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Root Route
@app.get("/")
def home():
    return {
        "message": "TechPulse AI Backend Running"
    }

# Get All Processed Articles
@app.get("/articles")
def get_articles():

    articles = list(collection.find(
        {"processed": True},
        {"_id": 0}
    ).sort("publishedAt", -1))

    return articles

# Get Articles By Category
@app.get("/articles/{category}")
def get_category_articles(category: str):

    articles = list(collection.find(
        {
            "category": category,
            "processed": True
        },
        {"_id": 0}
    ).sort("publishedAt", -1))

    return articles

# Search Articles
@app.get("/search")
def search_articles(q: str):

    articles = list(collection.find(
        {
            "$and": [
                {"processed": True},
                {
                    "$or": [
                        {
                            "title": {
                                "$regex": q,
                                "$options": "i"
                            }
                        },
                        {
                            "description": {
                                "$regex": q,
                                "$options": "i"
                            }
                        }
                    ]
                }
            ]
        },
        {"_id": 0}
    ).sort("publishedAt", -1))

    return articles