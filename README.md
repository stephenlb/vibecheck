# VibeCheck

Classify any text into custom categories using embedding similarity.
No AI training required.
Supports 100+ languages via Google's EmbeddingGemma model.

## How It Works

VibeCheck uses sentence embeddings to classify text against keyword-defined categories. Each classification in `config.yaml` has a set of representative keywords that get encoded into a baseline embedding vector. Input text is then encoded and compared against each baseline using cosine similarity, producing a score from 0 to 1 per category.

```
keywords ("happy joyful wonderful") → EmbeddingGemma → baseline vector
input text ("great day!")           → EmbeddingGemma → input vector
cosine_similarity(input, baseline)  → 0.72 (positivity score)
```

## Built-in Classifications

| Category | Description |
|---|---|
| praises | Compliments and recognition |
| positivity | Happy, optimistic language |
| negativity | Sad, critical, or pessimistic language |
| bullying | Insults and personal attacks |
| sarcasm | Ironic or mocking remarks |
| gratitude | Thankfulness and appreciation |
| encouragement | Motivational and supportive language |
| humor | Jokes and comedic language |
| frustration | Annoyance and exasperation |
| curiosity | Questions and interest |
| toxicity | Hate speech and threats |

## Installation

```shell
# Login to Hugging Face (required for model license)
huggingface-cli login

# Install dependencies with pip
pip install -r requirements.txt

# Or with uv
uv pip install -r requirements.txt
```

## Usage

### Run as API server

```shell
uvicorn main:app
```

Then send a POST request with plain text in the body:

```shell
curl -X POST http://localhost:8000 -d "you did a great job"
```

Response:

```json
{
  "praises": 0.68,
  "positivity": 0.33,
  "negativity": 0.18,
  "bullying": 0.17,
  "sarcasm": 0.39,
  "gratitude": 0.44,
  "encouragement": 0.45,
  "humor": 0.32,
  "frustration": 0.13,
  "curiosity": 0.24,
  "toxicity": 0.23
}
```

### Run debug test

```shell
python main.py
```

Prints classification scores for a set of sample inputs.

## Configuration

Edit `config.yaml` to customize the model and classifications:

```yaml
model: "google/embeddinggemma-300m"
classifications:
  - name: praises
    keywords: "great job, well done, excellent work, proud of you"
  - name: my_custom_category
    keywords: "keyword1, keyword2, phrase one, phrase two"
```

- **model**: Any [Sentence Transformers](https://www.sbert.net/) compatible model.
- **classifications**: Add, remove, or edit categories. Each entry needs a `name` and a `keywords` string of representative words/phrases.

## Why EmbeddingGemma

- Supports 100+ languages out of the box
- No fine-tuning or training data needed
- Small model (300M parameters) runs locally
