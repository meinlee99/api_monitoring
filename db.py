import psycopg2
from datetime import datetime

"""
    CREATE TABLE api_metrics (
    id SERIAL PRIMARY KEY,
    api_name TEXT,
    status_code INT,
    latency_ms INT,
    success BOOLEAN,
    error_message TEXT,
    timestamp TIMESTAMP
);
"""

def log_api_metrics(api_name, status_code, latency_ms, success, error_message):
    conn = psycopg2.connect("dbname=api_monitor user=postgres password=yourpassword")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO api_metrics (api_name, status_code, latency_ms, success, error_message, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (api_name, status_code, latency_ms, success, error_message, datetime.utcnow()))
    conn.commit()
    cur.close()
    conn.close()

def get_recent_metrics(api_name, minutes=5):
    conn = psycopg2.connect("dbname=api_monitor user=postgres password=yourpassword")
    cur = conn.cursor()
    cur.execute("""
        SELECT status_code, latency_ms, success, error_message, timestamp
        FROM api_metrics
        WHERE api_name = %s AND timestamp > NOW() - INTERVAL '%s minutes'
    """, (api_name, minutes))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results