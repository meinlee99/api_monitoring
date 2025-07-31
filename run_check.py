import requests
import time
import sentry_sdk
from db import log_api_metrics
from alert import alert_if_needed

def check_api(api_config):
    api_name = api_config["api_name"]
    url = api_config["url"]
    method = api_config.get("method", "GET")
    headers = api_config.get("headers", {})
    expected_status = api_config.get("expected_status_codes", [200])
    start = time.time()
    error_message = None
    success = False
    status_code = None

    # TODO: proactive_checks()

    try:
        response = requests.request(method, url, headers=headers, timeout=10)
        elapsed_ms = int((time.time() - start) * 1000)
        status_code = response.status_code
        success = status_code in expected_status
        if not success:
            error_message = f"Unexpected status: {status_code}"
            alert_if_needed() # TODO
    except Exception as e:
        elapsed_ms = int((time.time() - start) * 1000)
        error_message = str(e)
        sentry_sdk.capture_exception(e)
        alert_if_needed() # TODO

    inserted_ids = log_api_metrics(api_name, status_code, elapsed_ms, success, error_message)
    return {
        "api_name": api_name,
        "status_code": status_code,
        "latency_ms": elapsed_ms,
        "success": success,
        "error": error_message,
        "inserted_ids": inserted_ids
    }

def proactive_checks():
    """
    Run proactive checks for critical APIs to ensure they are functioning correctly.
    # TODO: Check if auth token expires soon or if rate limits are approaching.
    """
    # Placeholder for proactive checks logic
    # This could include checking token expiry, rate limits, etc.
    pass