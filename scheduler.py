import schedule
import time
from api_configs import API_CONFIGS
from monitor import check_api
from alert import send_slack_alert
from db import get_recent_metrics

SLACK_WEBHOOK = "https://hooks.slack.com/services/your/webhook/url"

def alert_if_needed(api_name):
    metrics = get_recent_metrics(api_name, minutes=5)
    errors = [m for m in metrics if not m[2]]
    high_latency = [m for m in metrics if m[1] > 1000]
    error_rate = len(errors) / max(1, len(metrics))
    if error_rate > 0.05 or high_latency:
        msg = f"ALERT: {api_name} error rate {error_rate*100:.1f}% or high latency detected!"
        send_slack_alert(msg, SLACK_WEBHOOK)

def schedule_jobs():
    for api_config in API_CONFIGS:
        interval = api_config.get('interval_seconds', 300)
        schedule.every(interval).seconds.do(check_api, api_config)
        schedule.every(interval).seconds.do(alert_if_needed, api_config["api_name"])

if __name__ == "__main__":
    schedule_jobs()
    print("Starting API monitoring loop...")
    while True:
        schedule.run_pending()
        time.sleep(1)