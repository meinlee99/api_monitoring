from unittest.mock import patch
import schedule
import time
from api_configs import API_CONFIGS
from run_check import check_api
from alerts import check_and_alert_latency


def mock_log_api_metrics(*args, **kwargs):
    # Simulate returning a fake inserted ID
    return [123]

def mock_get_recent_metrics(api_name, minutes=5, min_latency_ms=0):
    # Simulate returning a fake metric tuple
    return [("mock_api", 500, 1500, False, "Timeout error", "2023-10-01 12:00:00")]

def schedule_jobs():
    test_api_config = {
        "api_name": "mock_api",
        "url": "https://api.mock.com",
        "method": "GET",
        "headers": {
            "User-Agent": "PostmanMonitoringBot"
        },
        "expected_status_codes": [200],
        "interval_seconds": 5,  # run every 5 seconds
        "max_retries": 1
    }

     # Patch API_CONFIGS to include only the test API
    with patch('__main__.API_CONFIGS', [test_api_config]), \
         patch('db.log_api_metrics', mock_log_api_metrics):
        for api_config in API_CONFIGS:
            interval = api_config.get('interval_seconds', 300)
            schedule.every(interval).seconds.do(check_api, api_config)
            print(api_config['api_name'])
            schedule.every(interval).seconds.do(check_and_alert_latency, api_name=api_config['api_name'])


    # for api_config in API_CONFIGS:
    #     interval = api_config.get('interval_seconds', 300)
    #     # Make validation checks for each API
    #     schedule.every(interval).seconds.do(check_api, api_config)
    #     schedule.every(interval).seconds.do(check_and_alert_latency, api_name=api_config['api_name'])


if __name__ == "__main__":
    schedule_jobs()
    print("Starting API monitoring loop...")
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for a minute

