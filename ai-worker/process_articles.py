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
        You are an AI news analyzer.
        
        Analyze the following news article carefully.
        
        Possible Categories:
        - AI
        - Cybersecurity
        - Data Science
        - Cloud Computing
        - DevOps
        - Blockchain
        - Others
        
        Rules:
        1. If the article is NOT related to IT or technology, category MUST be "Others".
        2. Generate a short professional summary in 2-3 sentences.
        3. Generate 3 to 5 related tags.
        4. Return ONLY valid JSON.
        5. Do not include markdown or explanations.
        
        Return Format:
        {{
          "category": "",
          "summary": "",
          "tags": []
        }}
        
        Article Title:
        {article.get('title', '')}
        
        Article Description:
        {article.get('description', '')}
        
        Article Content:
        {article.get('content', '')}
        """

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
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

        category = ai.get("category", "Others")
        summary = ai.get("summary", "No summary available")
        tags = ai.get("tags", [])
        
        # Ensure tags is always a list
        if not isinstance(tags, list):
            tags = []
        
        collection.update_one(
            {"_id": article["_id"]},
            {
                "$set": {
                    "category": category,
                    "summary": summary,
                    "tags": tags,
                    "processed": True
                }
            }
        )

        print("\nUpdated MongoDB Successfully!")

    except Exception as e:

        print("\nERROR:")
        print(e)