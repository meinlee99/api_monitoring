import requests
import time
import logging
import sentry_sdk
from alerts import betterstack_alert
from db import log_api_metrics

def check_api(api_config):
    logging.info(f"Checking API: {api_config['api_name']} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    api_name = api_config["api_name"]
    url = api_config["url"]
    method = api_config.get("method", "GET")
    headers = api_config.get("headers", {})
    expected_status = api_config.get("expected_status_codes", [200])
    start = time.time()
    error_message = None
    success = False
    status_code = None

    # TODO: PHASE 2: proactive_checks()
    # Sanity checks for warnings


    try:
        response = requests.request(method, url, headers=headers, timeout=10)
        elapsed_ms = int((time.time() - start) * 1000)
        status_code = response.status_code
        success = status_code in expected_status
        # Configurable
        if not success:
            error_message = f"Unexpected status: {status_code}"
            betterstack_alert(error_message)

    except Exception as e:
        elapsed_ms = int((time.time() - start) * 1000)
        error_message = str(e)
        sentry_sdk.capture_exception(e)

    inserted_ids = [123]
    # log_api_metrics(api_name, status_code, elapsed_ms, success, error_message)
    print("Returning API metrics...")
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