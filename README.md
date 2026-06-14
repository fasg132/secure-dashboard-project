# Secure API & Infrastructure Metrics Dashboard

A production-ready microservice infrastructure built with **FastAPI**, **Nginx**, and **Redis**, featuring automated security rate-limiting and real-time observability using **Prometheus** and **Grafana**.

## Architecture & Features
- **Reverse Proxy (Nginx):** Acts as a secure gateway, hiding backend service topology and forwarding real client IPs.
- **Asynchronous Backend (FastAPI):** Collects host system metrics (CPU, RAM, Uptime) and exposes standard Prometheus telemetry.
- **Active Security Shield (Redis):** Implements an in-memory sliding window rate limiter (max 5 requests/minute per IP) to mitigate DDoS and brute-force attacks.
- **Full Observability Stack:** Prometheus scrapes telemetry every 3 seconds, visualizing system behavior and HTTP metrics inside customized Grafana dashboards.
- **SecDevOps Pipeline:** Integrated GitHub Actions with code linting (`flake8`) and automated container security vulnerability scanning (`Trivy`).

## Infrastructure Setup

To spin up the entire stack, make sure you have Docker installed and run:

```bash
docker compose up --build