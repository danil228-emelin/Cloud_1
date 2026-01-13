FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВСЁ приложение
COPY . .

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 flaskuser && chown -R flaskuser:flaskuser /app
USER flaskuser

EXPOSE 5000

CMD ["python", "app.py"]