import time
from sqlalchemy import text
from app.database import engine
from app.nlp.nlp_to_sql import generate_sql
from app.analytics.stats import log_query

def is_safe(sql):
    forbidden = ["DELETE", "DROP", "UPDATE", "INSERT"]
    return not any(word in sql.upper() for word in forbidden)

def process_query(question):
    start = time.time()

    sql = generate_sql(question)

    if not is_safe(sql):
        return {"error": "Unsafe query"}

    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql)).fetchall()

        exec_time = time.time() - start

        log_query(question, exec_time)

        return {
            "sql": sql,
            "result": [dict(row._mapping) for row in result],
            "execution_time": exec_time
        }

    except Exception as e:
        return {"error": str(e)}