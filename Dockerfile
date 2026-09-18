
FROM python:3.10-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*
COPY --from=builder /root/.local /root/.local
COPY . /app
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
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


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
