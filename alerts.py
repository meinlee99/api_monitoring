import os
import logging
import requests
import sentry_sdk
from db import get_recent_metrics
from unittest.mock import patch
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
if not SLACK_TOKEN:
    raise ValueError("SLACK_TOKEN environment variable is not set")

BETTERSTACK_WEBHOOK_URL = "https://betterstack.com/api/v1/alerts"  # replace with actual endpoint

client = WebClient(token=SLACK_TOKEN)



@patch('alerts.get_recent_metrics', return_value=[
    ("example_api", 200, 1500, False, "Timeout error", "2023-10-01 12:00:00")
])
def check_and_alert_latency(mock_get_recent_metrics, api_name, latency_threshold=1000, error_rate_threshold=0.05, minutes=5):
    """
    Check recent metrics (within the last 5 minutes)
    for the given API and send an alert if error rate or high latency is detected.

    Currently, this function alerts via Slack channels.
    """
    # print(f"Checking latency for API: {api_name}")
    # Fetch recent metric from Postgres
    metrics = get_recent_metrics(api_name, minutes=minutes)
    if not metrics:
        return

    # Filter metrics for errors and high latency
    # Assuming metrics is a list of tuples:
    # # api_name, status_code, latency_ms, success, error_message, created_at
    for metric in metrics:
        try:
            if not metric[3]:  # If success is False
                error_message = f"API {metric[0]} failed with status {metric[1]}: {metric[4]}"
                client.chat_postMessage(channel='alerts', text=error_message)
                logging.info(f"Sent response alert for {metric[0]}: {error_message}")

            if metric[2] > latency_threshold:  # If latency exceeds threshold
                latency_message = f"API {metric[0]} latency high: {metric[2]}ms"
                client.chat_postMessage(channel='alerts', text=latency_message)
                logging.info(f"Sent latency alert for {metric[0]}: {latency_message}")
        except SlackApiError as e:
            logging.error(f"Slack API error: {e.response['error']}")
            sentry_sdk.capture_exception(e)


def betterstack_alert(message: str):
    try:
        payload = {
            "title": "API Monitoring Alert",
            "description": message,
            "severity": "error"
        }
        headers = {"Content-Type": "application/json"}
        # TODO: Verify payload structure with BetterStack API documentation
        resp = requests.post(BETTERSTACK_WEBHOOK_URL, json=payload, headers=headers, timeout=5)
        if resp.status_code != 200:
            print(f"[BetterStack Alert Failed] Status: {resp.status_code}, Response: {resp.text}")
    except Exception as e:
        print(f"[BetterStack Alert Exception] {str(e)}")



if __name__ == "__main__":
    # Mock get_recent_metrics to return your test data
    with patch('__main__.get_recent_metrics', return_value=[
        ("example_api", 200, 1500, False, "Timeout error", "2023-10-01 12:00:00")
    ]):
        check_and_alert_latency("example_api", latency_threshold=1000, error_rate_threshold=0.05, minutes=5)
        logging.info("Alert check completed.")

    
    # Test metric: (api_name, status_code, latency_ms, success, error_message, created_at)
    # metrics = [("example_api", 200, 1500, False, "Timeout error", "2023-10-01 12:00:00")]
