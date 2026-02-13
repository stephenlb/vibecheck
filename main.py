import json
from fastapi import FastAPI, Request
from sentence_transformers import SentenceTransformer

app = FastAPI()

@app.post("/")
async def index(request: Request):
    body = await request.body()
    text = body.decode("utf-8")
    #return text
    return vibe("good, good job!")
    #return vibe(text)

model = SentenceTransformer("google/embeddinggemma-300m")
## TODO in yaml format
praises = model.encode(["good job, amazing"])
positivity = model.encode(["happy awesome joy good excellent nice amazing"])

def vibe(sentance: str) -> float:
    embedding = model.encode([sentance])
    similar = model.similarity(embedding, positivity)
    return float(similar.detach().cpu().numpy()[0][0])

## TODO REMOVE this is just for debugging...
print("bad", vibe("bad, you did badly"))
print("bad in Lithuanian", vibe("blogai, blogai padarei"))
print("good", vibe("good, good job!"))
print("well", vibe("you did well"))
print("poor", vibe("you did poorly"))
print("emoji 🎉", vibe("🎉"))
print("emoji 😞", vibe("😞"))
