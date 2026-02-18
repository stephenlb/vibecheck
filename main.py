import os
import yaml
import numpy as np
from fastapi import FastAPI, Request
from sentence_transformers import SentenceTransformer

## Config path from environment variable (default: config.yaml)
config_path = os.environ.get('CONFIG', 'config.yaml')

## Load config
config = None
with open(config_path, 'r') as file:
    try:
        config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)

## Load model
model = SentenceTransformer(config['model'], device=config['device'])

## Initial vectors for each classification
classifications = {}
for classification in config['classifications']:
    name = classification['name']
    phrases = [p.strip() for p in classification['keywords'].split(',')]
    embeddings = model.encode(phrases)
    classifications[name] = embeddings.mean(axis=0, keepdims=True)

## Pre-stack baselines into a single matrix for vectorized similarity
class_names = list(classifications.keys())
baseline_matrix = np.vstack([classifications[n] for n in class_names])

app = FastAPI()

## POST Endpoint
@app.post("/")
async def index(request: Request):
    body = await request.body()
    sentance = body.decode("utf-8")
    return classify(sentance)

## Classification function
def classify(sentance: str) -> dict:
    embedding = model.encode([sentance])
    similarities = model.similarity(embedding, baseline_matrix)
    scores = similarities.detach().cpu().numpy()[0]
    return dict(zip(class_names, scores.tolist()))
