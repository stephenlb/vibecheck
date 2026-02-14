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

## Tests
print("--- negativity ---")
print("bad", classify("bad, you did badly"))
print("bad in Lithuanian", classify("blogai, blogai padarei"))
print("poor", classify("you did poorly"))
print("terrible day", classify("this has been a terrible day"))

print("--- positivity ---")
print("good", classify("good, good job!"))
print("well", classify("you did well"))
print("beautiful day", classify("what a beautiful day it is"))

print("--- praises ---")
print("excellent work", classify("excellent work on this project"))
print("proud of you", classify("I am so proud of you"))
print("nailed it", classify("you absolutely nailed it"))

print("--- bullying ---")
print("insult", classify("you are such an idiot"))
print("exclusion", classify("nobody wants you here, go away"))
print("mockery", classify("everyone laughs at you behind your back"))

print("--- sarcasm ---")
print("oh really", classify("oh really, what a shocker"))
print("sure thing", classify("yeah right, sure thing buddy"))
print("slow clap", classify("wow, slow clap for that brilliant idea"))

print("--- gratitude ---")
print("thank you", classify("thank you so much for your help"))
print("appreciate it", classify("I really appreciate everything you have done"))
print("thanks in Spanish", classify("muchas gracias por todo"))

print("--- encouragement ---")
print("you can do it", classify("you can do it, I believe in you!"))
print("keep going", classify("don't give up, keep pushing forward"))
print("team spirit", classify("let's go team, we've got this!"))

print("--- humor ---")
print("lol", classify("lol that was hilarious"))
print("joke", classify("why did the chicken cross the road"))
print("haha", classify("haha I can't stop laughing"))

print("--- frustration ---")
print("annoyed", classify("ugh this is so annoying, nothing works"))
print("fed up", classify("I am so fed up with this nonsense"))
print("why", classify("why does this keep happening to me"))

print("--- curiosity ---")
print("how", classify("how does this work exactly?"))
print("wonder", classify("I wonder what would happen if we tried that"))
print("explain", classify("can you explain this to me?"))

print("--- toxicity ---")
print("threat", classify("I will find you and hurt you"))
print("hate", classify("I hate everyone like you"))
print("slur", classify("you disgusting piece of garbage, die"))

print("--- emoji ---")
print("emoji 🎉", classify("🎉"))
print("emoji 😞", classify("😞"))
print("emoji 😂", classify("😂😂😂"))
print("emoji ❤️", classify("❤️"))
print("emoji 🤔", classify("🤔"))

print("--- mixed signals ---")
print("sarcastic praise", classify("oh great job, really, what a genius move"))
print("backhanded compliment", classify("well you tried your best I guess"))
print("polite frustration", classify("with all due respect, this is unacceptable"))
print("encouraging criticism", classify("you made a mistake but I know you can fix it"))
