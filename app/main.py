from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from prometheus_fastapi_instrumentator import Instrumentator
import psutil
import time
import redis
import os

app = FastAPI(title="Secure Infrastructure API", version="1.0.0")

# Настраиваем Prometheus Instrumentator
# Он автоматически создаст эндпоинт /metrics и будет считать скорость ответов
Instrumentator().instrument(app).expose(app)

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

START_TIME = time.time()
REQUEST_LIMIT = 5
TIME_WINDOW = 60

@app.get("/", response_class=HTMLResponse)
def read_root():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/api/stats")
def get_system_stats(request: Request):
    client_ip = request.client.host
    redis_key = f"rate_limit:{client_ip}"
    
    current_requests = r.get(redis_key)
    
    if current_requests and int(current_requests) >= REQUEST_LIMIT:
        raise HTTPException(
            status_code=429, 
            detail="Too Many Requests! You are rate limited. Wait a minute."
        )
    
    pipe = r.pipeline()
    pipe.incr(redis_key)
    if not current_requests:
        pipe.expire(redis_key, TIME_WINDOW)
    pipe.execute()

    cpu_usage = psutil.cpu_percent(interval=None)
    memory_info = psutil.virtual_memory()
    
    return {
        "status": "healthy",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "metrics": {
            "cpu_usage_percent": cpu_usage,
            "memory_usage_percent": memory_info.percent
        }
    }