import os
import logging
import sentry_sdk
# from db import get_recent_metrics
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
if not SLACK_TOKEN:
    raise ValueError("SLACK_TOKEN environment variable is not set")

client = WebClient(token=SLACK_TOKEN)

def check_and_alert_latency(api_name, latency_threshold=1000, error_rate_threshold=0.05, minutes=5):
    """
    Check recent metrics (within the last 5 minutes)
    for the given API and send an alert if error rate or high latency is detected.

    Currently, this function alerts via Slack channels.
    """
    # Fetch recent metric from Postgres
    # metrics = get_recent_metrics(api_name, minutes=minutes)
    # if not metrics:
    #     return

    # Test metric: (api_name, status_code, latency_ms, success, error_message, created_at)
    metrics = [("example_api", 200, 1500, False, "Timeout error", "2023-10-01 12:00:00")]

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

    # errors = [m for m in metrics if not m[2]]
    # high_latency = [m for m in metrics if m[1] is not None and m[1] > latency_threshold]
    # error_rate = len(errors) / max(1, len(metrics))

    # if error_rate > error_rate_threshold or high_latency:
    #     msg = (
    #         f"ALERT: {api_name} error rate {error_rate*100:.1f}% "
    #         f"or high latency detected! "
    #         f"Errors: {len(errors)}, High latency: {len(high_latency)}"
    #     )


if __name__ == "__main__":
    check_and_alert_latency("example_api", latency_threshold=1000, error_rate_threshold=0.05, minutes=5)
    logging.info("Alert check completed.")