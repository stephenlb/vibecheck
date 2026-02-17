FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV HF_TOKEN=""
ENV CONFIG="config.yaml"

CMD uvicorn main:app --host 0.0.0.0 --port 8000 -- --config $CONFIG
