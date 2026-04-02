🚀 AI-Powered NLP to SQL Backend (EdTech)
📌 Overview

This project is an AI-powered backend service that converts natural language questions into SQL queries and retrieves results from an EdTech database.

It enables non-technical users to query structured data using plain English.

🧠 Problem Statement

Users should be able to ask questions like:

“How many students enrolled in Python courses in 2024?”

Without knowing SQL.

🏗️ Tech Stack
Backend: FastAPI
Database: SQLite
ORM: SQLAlchemy
Testing: Pytest
Containerization: Docker
NLP Approach: Rule-based (extendable to LLM)

📂 Project Structure
ai-edtech-nlp2sql/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── nlp/
│   ├── services/
│   ├── analytics/
│
├── tests/
│   ├── test_api.py
│   ├── test_nlp.py
│
├── seed.py
├── Dockerfile
├── k8s-pod.yaml
└── README.md

⚙️ Setup Instructions
1️⃣ Clone repository
git clone https://github.com/hifzarif/ai-edtech-nlp2sql.git
cd ai-edtech-nlp2sql
2️⃣ Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate
3️⃣ Install dependencies
pip install -r requirements.txt
🌱 Seed Database
python seed.py
▶️ Run the Server
uvicorn app.main:app --reload
🌐 API Documentation

Open:

http://127.0.0.1:8000/docs
📥 API Endpoints
🔹 POST /query

Input:

{
  "question": "How many students enrolled in Python courses?"
}

Output:

{
  "sql": "SELECT COUNT(*) ...",
  "result": [{"count": 10}],
  "execution_time": 0.01
}
🔹 GET /stats

Returns:

Total queries
Most common keywords
Slowest query
🔐 Safety Measures
Only SELECT queries allowed
Blocks:
DELETE
UPDATE
DROP
INSERT
🧠 NLP to SQL Approach
Current Implementation:
Rule-based parsing using keyword matching
Example:
Question	SQL
"How many Python students?"	COUNT + JOIN
"Show all students"	SELECT *
Future Improvements:
LLM-based SQL generation (OpenAI / LangChain)
Schema-aware prompting
Query validation layer
🧪 Testing

Run tests:

python -m pytest
🐳 Docker Setup
Build Image:
docker build -t ai-edtech .
Run Container:
docker run -p 8000:8000 ai-edtech

☸️ Kubernetes Deployment
kubectl apply -f k8s-pod.yaml

⚠️ Limitations
Rule-based NLP is limited in understanding complex queries
No persistent analytics storage
No authentication layer

🚀 Future Enhancements
Integrate OpenAI for dynamic SQL generation
Add Redis caching
Add authentication & role-based access
Deploy on cloud (AWS / Render / Railway)


