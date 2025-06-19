# Python imageni tanlash
FROM python:3.13

# Ishchi katalog
WORKDIR /app

# Talablarni o‘rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Django kodini joylash
COPY . .

# Django uchun port
EXPOSE 8000

# Serverni ishga tushurish
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
