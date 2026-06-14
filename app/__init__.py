from fastapi import FastAPI, HTTPException, Request
import psutil
import time
import redis
import os

app = FastAPI(
    title="Secure Infrastructure API",
    version="1.0.0"
)

# Подключаемся к Redis (берем имя хоста из переменных окружения Docker)
redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

START_TIME = time.time()

# Лимит: максимум 5 запросов в минуту с одного IP
REQUEST_LIMIT = 5
TIME_WINDOW = 60

@app.get("/")
def read_root():
    return {"status": "online", "message": "Secure API is running"}

@app.get("/api/stats")
def get_system_stats(request: Request):
    # Получаем IP-адрес пользователя
    client_ip = request.client.host
    redis_key = f"rate_limit:{client_ip}"
    
    # Считаем, сколько запросов уже сделал этот IP
    current_requests = r.get(redis_key)
    
    if current_requests and int(current_requests) >= REQUEST_LIMIT:
        # Если превысил лимит — жестко отшибаем с ошибкой 429
        raise HTTPException(
            status_code=429, 
            detail="Too Many Requests! You are rate limited. Wait a minute."
        )
    
    # Если лимит не превышен, увеличиваем счетчик запросов
    pipe = r.pipeline()
    pipe.incr(redis_key)
    # Если это первый запрос, ставим ему срок жизни в 60 секунд
    if not current_requests:
        pipe.expire(redis_key, TIME_WINDOW)
    pipe.execute()

    # Отдаем наши метрики
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