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
    created_at TIMESTAMP
);
"""

def log_api_metrics(api_name, status_code, latency_ms, success, error_message):
    conn = psycopg2.connect("dbname=api_monitor user=postgres password=yourpassword")
    cur = conn.cursor()
    cur.executmany("""
        INSERT INTO api_metrics (api_name, status_code, latency_ms, success, error_message, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (api_name, status_code, latency_ms, success, error_message, datetime.utcnow()))
    inserted_ids = [row[0] for row in cur.fetchall()]
    conn.commit()
    cur.close()
    conn.close()
    return inserted_ids

def get_recent_metrics(api_name, minutes=5, latency_threshold=1000):
    conn = psycopg2.connect("dbname=api_monitor user=postgres password=yourpassword")
    cur = conn.cursor()
    cur.execute("""
        SELECT api_name, status_code, latency_ms, success, error_message, created_at
        FROM api_metrics
        WHERE api_name = %s AND timestamp > NOW() - INTERVAL '%s minutes'
        AND latency_ms >= %s
    """, (api_name, minutes))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results