FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python

COPY app ./app
COPY app/data ./data

EXPOSE 8000

ENV MONGO_DB_NAME=IranMalDB \
    MONGO_COLLECTION=tweets \
    WEAPONS_FILE=/app/data/weapons.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
