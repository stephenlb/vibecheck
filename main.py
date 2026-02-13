import json
from fastapi import FastAPI, Request
from sentence_transformers import SentenceTransformer
import yaml

## Load config
config = None
with open('config.yaml', 'r') as file:
    try:
        config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)

## Load model
model = SentenceTransformer(config['model'])

## Initial vectors for each classification
classifications = {}
for classification in config['classifications']:
    name = classification['name']
    keywords = [classification['keywords']]
    classifications[name] = model.encode(keywords)

app = FastAPI()

## POST Endpoint
@app.post("/")
async def index(request: Request):
    body = await request.body()
    sentance = body.decode("utf-8")
    return classify(sentance)

## Clasification function
def classify(sentance: str) -> dict:
    response = {}
    for name, baseline in classifications.items():
        response[name] = vibe(baseline, sentance)
    return response

    

## Classification function
def vibe(baseline, sentance: str) -> float:
    embedding = model.encode([sentance])
    similar = model.similarity(embedding, baseline)
    return float(similar.detach().cpu().numpy()[0][0])

## TODO REMOVE this is just for debugging...
print("bad", classify("bad, you did badly"))
print("bad in Lithuanian", classify("blogai, blogai padarei"))
print("good", classify("good, good job!"))
print("well", classify("you did well"))
print("poor", classify("you did poorly"))
print("emoji 🎉", classify("🎉"))
print("emoji 😞", classify("😞"))
