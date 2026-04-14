FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ca-certificates

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
