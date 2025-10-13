FROM python:3.12-slim-bullseye
WORKDIR /app
COPY ../requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["python", "main.py"]
