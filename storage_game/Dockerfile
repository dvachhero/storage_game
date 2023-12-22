# Базовый образ
FROM python:3.11.4

# Установка рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY . /app

# Установка зависимостей
RUN pip install -r requirements.txt

# Команда для запуска сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
