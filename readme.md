# API Monitoring & Alerting System

## Overview

This repository provides a robust system for monitoring the health, latency, and error rates of critical third-party APIs. It enables real-time alerting, historical analysis, and proactive insights to ensure high reliability and fast incident response for your integrations.

---

## Technical Deep Dive 

Please refer to these slides for trade-off discussions, deep dives, and other technical details:  
  [API Monitoring System Design Slides](https://docs.google.com/presentation/d/1VURI8Zrqo3bxWt_HUR5Os0NilRA0m89MdG6VaxTkDTU/edit?usp=sharing)

---

## Goals

- User Friendly
- Build Trust
- Guarantee Efficiency
- Drive Refinements

---

## Pain Points
- Unhandled API failures flows downstream to users, degrade the user experience and reduce customer satisfaction

- Slow third-party API responses causes latency and impact overall application performance

---

## Key Use Cases

### 🛠️ 1. Remediation

- **Faster Incident Response:**  
  Alerts internal teams before users notice outages, reducing Mean Time To Recovery (MTTR).
- **Faster Root Cause Analysis (RCA):**  
  Historical logs and metrics help determine if issues stem from external dependencies or internal code.


### 🛡️ 2. Preventative

- **Proactive Insights:**  
  Catch issues before they become outages (e.g., 10% failure rate warning).
  Detect expiring auth tokens, degraded vendor performance, or sudden latency spikes.
- **Alerting & Early Detection:**  
  Use thresholds and error patterns to alert developers early.
  Set smart alerts to minimize noise and maximize impact.
- **Increased Reliability & Uptime:**  
  Early detection of slow or failing APIs ensures stable integrations and builds customer trust.


### 🚀 3. Enhancements

- **Visibility & Observability:**  
  Centralized dashboard shows uptime history, average response times, and failure patterns per API.
- **API Optimization:**  
  Identify APIs that consistently underperform.
  Flag vendors with poor API SLAs to reconsider, renegotiate, or replace.

---

## Phase 1: How It Works

- **API Health Checks:**  
  Scheduled jobs send requests to configured APIs, logging response codes, latency, and errors.
- **Alerting Engine:**  
  Monitors recent metrics and triggers alerts (Slack, Email, PagerDuty) if thresholds are breached.
- **Error Monitoring:**  
  Integrates with Sentry for runtime error capture.
- **Data Storage:**  
  Metrics are logged to PostgreSQL for historical analysis and dashboarding.
---

## Alerting Channels

- **Slack:** Engineering channel for real-time notifications.
- **Email:** Wider ops or platform teams.
- **PagerDuty:** For critical APIs.
- **(Optional) SMS/Phone:** For P0 events.

---

## Phase 2: Future Improvements

- Add support for more alerting channels.
- Enhance proactive checks (e.g., token expiry, rate limit headers).
- Auto-remediation services for common failure types
- Add vendor performance analytics
- Authentication & Security

---

## Getting Started

1. **Clone the repository:**
   ```
   git clone https://github.com/your-username/api_monitoring.git
   cd api_monitoring
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Configure your APIs:**  
   Edit `api_configs.py` to add or update APIs to monitor.

4. **Set up PostgreSQL:**  
   Ensure your database is running and update connection details in `db.py`.

5. **Run the scheduler:**
   ```
   python scheduler.py
   ```

---

## Contributing

Feel free to open issues or submit pull requests for improvements and new features!

---