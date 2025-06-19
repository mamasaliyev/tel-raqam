FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ishchi katalog
WORKDIR /app

# OS kutubxonalar (dlib uchun kerak bo‘lsa)
RUN apt-get update && apt-get install -y \
    build-essential cmake libopenblas-dev liblapack-dev libx11-dev \
    libgtk-3-dev libboost-all-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Talablar
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Loyihani nusxalash
COPY . .

# Static/media kataloglar (Docker volume overwrite qiladi baribir)
RUN mkdir -p /app/staticfiles /app/mediafiles

# Port ochish
EXPOSE 8000

# Run qilish — docker-compose orqali beriladi
