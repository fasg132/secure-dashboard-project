# Базовый образ с Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё содержимое папки app внутрь контейнера
COPY ./app /app/app

# Открываем порт 8000, который будет слушать приложение
EXPOSE 8000

# Команда для запуска FastAPI внутри контейнера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]