FROM python:3.11-alpine as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-alpine
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY . .
CMD ["python", "app.py"]