from pymongo import MongoClient
import requests
import json
import os
from dotenv import load_dotenv
import re

print("AI Worker Started...")

# Load environment variables
load_dotenv()

# Environment Variables
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_URL = os.getenv("OLLAMA_URL")

print("Connecting MongoDB...")

# MongoDB Connection
client = MongoClient(MONGODB_URI)

db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Find unprocessed articles
articles = list(collection.find({
    "processed": False
}))

print(f"Found {len(articles)} unprocessed articles")

for article in articles:

    print("\n--------------------------------")
    print("Processing:", article.get("title"))

    prompt = f"""
Analyze this IT news article.

Possible Categories:
- AI
- Cybersecurity
- Data Science
- Cloud Computing
- DevOps
- Blockchain

Return ONLY valid JSON:

{{
  "category": "",
  "summary": "",
  "tags": []
}}

Title:
{article.get('title')}

Description:
{article.get('description')}
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        print("Ollama Response Status:", response.status_code)

        result = response.json()["response"]

        print("\nRaw AI Response:")
        print(result)

        # Extract JSON object only
        match = re.search(r'\{.*\}', result, re.DOTALL)
        
        if not match:
            raise Exception("No JSON found in AI response")
        
        cleaned = match.group(0)
        
        ai = json.loads(cleaned)
        
        collection.update_one(
            {"_id": article["_id"]},
            {
                "$set": {
                    "category": ai.get("category"),
                    "summary": ai.get("summary"),
                    "tags": ai.get("tags"),
                    "processed": True
                }
            }
        )

        print("\nUpdated MongoDB Successfully!")

    except Exception as e:

        print("\nERROR:")
        print(e)