import schedule
import time
from api_configs import API_CONFIGS
from monitor import check_api
from alert import send_slack_alert
from db import get_recent_metrics
from alerts import check_and_alert_latency

def schedule_jobs():
    for api_config in API_CONFIGS:
        interval = api_config.get('interval_seconds', 300)
        # Make validation checks for each API
        schedule.every(interval).seconds.do(check_api, api_config)
        schedule.every(interval).seconds.do(check_and_alert_latency, api_name=api_config['api_name'])


if __name__ == "__main__":
    schedule_jobs()
    print("Starting API monitoring loop...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Sleep for a minute