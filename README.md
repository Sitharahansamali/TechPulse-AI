# TechPulse AI

TechPulse AI is an AI-powered technology news aggregation platform that automatically collects the latest IT news, categorizes articles using Llama3 via Ollama, stores them in MongoDB, and displays them through a modern Streamlit dashboard.

---

## Features

- Automated tech news collection using NewsAPI
- n8n workflow automation
- AI-powered article categorization using Llama3
- MongoDB database integration
- Duplicate article prevention
- FastAPI backend API
- Modern Streamlit frontend dashboard
- Category filtering
- Search functionality
- Responsive news card UI

---

## System Architecture

NewsAPI  
↓  
n8n Workflow  
↓  
MongoDB  
↓  
Python AI Worker + Ollama  
↓  
FastAPI Backend  
↓  
Streamlit Frontend  

---

## Technologies Used

- Python 3.10
- FastAPI
- Streamlit
- MongoDB Atlas
- n8n
- Ollama
- Llama3
- NewsAPI

---

## Project Structure

```bash
TechPulse-AI/
│
├── ai-worker/
│   └── process_articles.py
│
├── backend/
│   └── main.py
│
├── streamlit-app/
│   └── app.py
│
├── .env
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <your-github-repo>
cd TechPulse-AI
```

---

## Backend Setup

```bash
cd backend
pip install fastapi uvicorn pymongo python-dotenv
```

Run backend:

```bash
uvicorn main:app --reload
```

---

## AI Worker Setup

Install requirements:

```bash
pip install pymongo requests python-dotenv
```

Run Ollama:

```bash
ollama run llama3
```

Run AI worker:

```bash
python ai-worker/process_articles.py
```

---

## Streamlit Frontend Setup

```bash
cd streamlit-app
pip install streamlit requests python-dotenv streamlit-option-menu
```

Run frontend:

```bash
streamlit run app.py
```

---

## MongoDB Configuration

Create a unique index for duplicate prevention:

Field:

```text
url
```

Type:

```text
Ascending (1)
```

Enable:

```text
Unique
```

---

## API Endpoints

### Get All Articles

```http
GET /articles
```

### Get Articles by Category

```http
GET /articles/{category}
```

### Search Articles

```http
GET /search?q=keyword
```

---

## Environment Variables

### Backend `.env`

```env
MONGODB_URI=your_mongodb_uri
DB_NAME=techpulse_ai
COLLECTION_NAME=articles
```

### Streamlit `.env`

```env
BACKEND_URL=http://127.0.0.1:8000
```

---

## Duplicate Prevention

TechPulse AI prevents duplicate articles using:

- n8n Remove Duplicates node
- MongoDB unique URL index

---

## Future Improvements

- User authentication
- AI chatbot integration
- Trending analytics
- Sentiment analysis
- Bookmarking system
- Admin dashboard
- Cloud deployment

---

## Author

Sithara Hansamali
