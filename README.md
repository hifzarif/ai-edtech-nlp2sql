AI-Powered NLP to SQL Backend for EdTech
  Overview

This project is a backend service that converts natural language queries into SQL statements and retrieves results from an EdTech database.

It enables non-technical users to interact with structured data using plain English.

Objective

To build an AI-powered system where users can ask questions like:

“How many students enrolled in Python courses in 2024?”

…and receive accurate results without writing SQL.

 Tech Stack
Backend: FastAPI
Database: SQLite
ORM: SQLAlchemy
NLP Engine: Rule-based (extendable to LLM)
Testing: Pytest
Containerization: Docker
Deployment: Kubernetes (Pod YAML)

 Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/hifzarif/ai-edtech-nlp2sql.git
cd ai-edtech-nlp2sql
2️⃣ Create Virtual Environment
python -m venv .venv
.\.venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Seed Database
python seed.py
5️⃣ Run Server
uvicorn app.main:app --reload


API Documentation

Open Swagger UI:

http://127.0.0.1:8000/docs

 
 API Examples
POST /query

Request:

{
  "question": "How many students enrolled in Python courses?"
}

Response:

{
  "sql": "SELECT COUNT(*) as count FROM enrollments ...",
  "result": [{"count": 10}],
  "execution_time": 0.01
}

 GET /stats

Response:

{
  "total_queries": 5,
  "common_keywords": [["students", 3], ["python", 2]],
  "slowest_query": {
    "q": "Show all students",
    "time": 0.02
  }
}


 NLP to SQL Approach
🔹 Current Implementation (Rule-Based)

The system converts natural language into SQL using keyword-based logic:

Detects intent using phrases like:
“how many” → COUNT queries
“show/list” → SELECT queries
Maps keywords (students, courses, enrollments) to tables
Uses conditional logic to construct SQL queries
🔹 Example Mapping
Input Question	Generated SQL
"Show all students"	SELECT * FROM students
"List all courses"	SELECT * FROM courses
"How many Python students?"	COUNT + JOIN query
🔹 Safety Mechanism

To prevent harmful queries:

Only SELECT queries are allowed
The system blocks:
DELETE
UPDATE
DROP
INSERT
🔹 Future Improvements
Integrate LLM (OpenAI / LangChain) for dynamic query generation
Add schema-aware prompting
Improve handling of complex queries (filters, dates, joins)
📊 Analytics

The /stats endpoint tracks:

Total number of queries
Frequently used keywords
Slowest query execution time


Testing

Run tests using:

python -m pytest

Docker Setup
Build Image
docker build -t ai-edtech .
Run Container
docker run -p 8000:8000 ai-edtech

 Kubernetes Deployment
kubectl apply -f k8s-pod.yaml

Limitations
Rule-based NLP cannot handle complex or ambiguous queries
Limited understanding of context and synonyms
No authentication or user roles implemented
Analytics data is stored in-memory (not persistent)

Future Enhancements
LLM-based NLP to SQL conversion
Query caching (Redis)
Role-based access control
Cloud deployment (AWS / Render)

Author

Hifza Arif
