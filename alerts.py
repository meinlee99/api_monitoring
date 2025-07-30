from db import get_recent_metrics
# from alert import send_slack_alert

SLACK_WEBHOOK = "https://hooks.slack.com/services/your/webhook/url"

def alert_if_needed(api_name, latency_threshold=1000, error_rate_threshold=0.05, minutes=5):
    metrics = get_recent_metrics(api_name, minutes=minutes)
    if not metrics:
        return

    errors = [m for m in metrics if not m[2]]
    high_latency = [m for m in metrics if m[1] is not None and m[1] > latency_threshold]
    error_rate = len(errors) / max(1, len(metrics))

    if error_rate > error_rate_threshold or high_latency:
        msg = (
            f"ALERT: {api_name} error rate {error_rate*100:.1f}% "
            f"or high latency detected! "
            f"Errors: {len(errors)}, High latency: {len(high_latency)}"
        )