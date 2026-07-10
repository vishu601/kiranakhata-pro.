# 1. Python ka official lightweight image use kar rahe hain
FROM python:3.11-slim

# 2. Server ke andar ek directory bana rahe hain jahan code rahega
WORKDIR /app

# 3. Kuch zaroori system packages install kar rahe hain postgres ke liye
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# 4. requirements.txt file ko container mein copy kar rahe hain
COPY requirements.txt /app/

# 5. Saari Python libraries install kar rahe hain
RUN pip install --no-cache-dir -r requirements.txt

# 6. Poora project ka code container ke andar copy kar rahe hain
COPY . /app/

# 7. Django server start karne ki command
# Purani CMD line ko hata kar ye daal do
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
