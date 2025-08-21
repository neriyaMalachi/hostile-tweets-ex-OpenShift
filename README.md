# Malicious Text Feature Engineering System

Pipeline מלא: שליפה מ-MongoDB Atlas → עיבוד טקסטים (rarest word, sentiment, weapons) → FastAPI GET JSON.

## ריצה מקומית

```bash
# Python 3.11+
pip install -r requirements.txt

# משתנים (דוגמאות)
set MONGO_URI=mongodb+srv://IRGC:iraniraniran@iranmaldb.gurutam.mongodb.net/
set MONGO_DB_NAME=IranMalDB
set MONGO_COLLECTION=tweets

uvicorn app.main:app --reload
# http://127.0.0.1:8000/health
# http://127.0.0.1:8000/processed
