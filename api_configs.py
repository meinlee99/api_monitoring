API_CONFIGS = [
    {
        "api_name": "GitHub",
        "url": "https://api.github.com",
        "method": "GET",
        "headers": {
            "User-Agent": "PostmanMonitoringBot"
        },
        "expected_status_codes": [200],
        "interval_seconds": 300,  # run every 5 minutes
        "max_retries": 1
    },
    {
        "api_name": "OpenWeather",
        "url": "https://api.openweathermap.org/data/2.5/weather?q=London&appid=your_api_key",
        "method": "GET",
        "headers": {},
        "expected_status_codes": [200],
        "interval_seconds": 600  # run every 10 minutes
    },
    {
        "api_name": "Twilio",
        "url": "https://api.twilio.com/2010-04-01/Accounts.json",
        "method": "GET",
        "headers": {
            "Authorization": "Basic your_twilio_auth"
        },
        "expected_status_codes": [200],
        "interval_seconds": 900  # run every 15 minutes
    },
    {
        "api_name": "Slack",
        "url": "https://slack.com/api/auth.test",
        "method": "POST",
        "headers": {
            "Authorization": "Bearer xoxb-your-slack-token"
        },
        "expected_status_codes": [200],
        "interval_seconds": 300
    }
]