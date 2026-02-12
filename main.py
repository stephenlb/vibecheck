import torch
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("google/embeddinggemma-300m")
baselineInput = ["happy awesome joy good excellent sweet honey"]
positivity = torch.tensor(model.encode(baselineInput))

def vibe(sentance: str) -> float:
    embedding = torch.tensor(model.encode(sentance))
    cosineSim = torch.nn.functional.cosine_similarity(embedding, positivity).item()
    #torch.tensor(
    similar = model.similarity(embedding, [positivity])
    return similar.detach().cpu().numpy()[0][0]

print("bad", vibe("bad, you did badly"))
print("good", vibe("good, good job!"))
print("emoji 🎉", vibe("🎉"))
print("emoji 😞", vibe("😞"))
