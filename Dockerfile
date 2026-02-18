FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG HF_TOKEN
RUN huggingface-cli download google/embeddinggemma-300m --token $HF_TOKEN

COPY . .

EXPOSE 8000

ENV CONFIG="config.yaml"

CMD CONFIG=$CONFIG uvicorn main:app --host 0.0.0.0 --port 8000
