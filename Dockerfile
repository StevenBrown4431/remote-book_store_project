FROM python:3.13-slim

ENV DATABASE_NAME="book_store"
ENV DATABASE_HOST="postgres:password@book_store_db"

WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app files
COPY . .

CMD ["python", "app.py"]