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
# Default config (config.yaml)
uvicorn main:app

# Custom config
CONFIG=live-chat-moderation.yaml uvicorn main:app

# Multiple workers for more concurrency
uvicorn main:app --workers 4
```

### Run with Docker

The Docker image runs a single uvicorn worker by default.
**This is intentional.**
When deployed to Kubernetes, horizontal pod autoscaling handles concurrency by scaling replicas based on load rather than running multiple workers per container.

```shell
# Build the image
docker build -t vibecheck .

# Run with default config
docker run -p 8000:8000 -e HF_TOKEN=hf_your_token_here vibecheck

# Run with a custom config
docker run -p 8000:8000 -e HF_TOKEN=hf_your_token_here -e CONFIG=live-chat-moderation.yaml vibecheck

# Mount an external config file
docker run -p 8000:8000 -e HF_TOKEN=hf_your_token_here -e CONFIG=/data/myconfig.yaml -v ./myconfig.yaml:/data/myconfig.yaml vibecheck
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

### Benchmark

```shell
echo -n "you did a great job and I appreciate you" > /tmp/bench.txt
ab -p /tmp/bench.txt -T text/plain -n 100 -c 10 http://127.0.0.1:8000/
```

### Run tests

```shell
# Default config tests
python test.py

# Live chat moderation tests
python test-live-chat-moderation.py
```

## Minimal Config

A minimal config with just positive and negative classifications is included as `minimal.yaml`:

```shell
CONFIG=minimal.yaml uvicorn main:app
```

| Category | Description |
|---|---|
| positive | Happy, supportive, and appreciative language |
| negative | Critical, hostile, and disapproving language |

## Live Chat Moderation Config

A ready-made config for moderating live chat is included as `live-chat-moderation.yaml`:

```shell
CONFIG=live-chat-moderation.yaml uvicorn main:app
```

| Category | Description |
|---|---|
| toxicity | Death threats and violent language |
| harassment | Bullying, insults, and personal attacks |
| hate_speech | Racial, ethnic, and discriminatory slurs |
| sexual_content | Explicit or inappropriate sexual messages |
| spam | Promotional links and follow-begging |
| profanity | Swearing and vulgar language |
| self_harm | Suicidal ideation and self-injury mentions |
| doxxing | Leaking personal or private information |
| scam | Phishing and credential theft attempts |
| impersonation | Fake admins, staff, or authority figures |
| raiding | Coordinated chat attacks and brigading |
| positive | Wholesome and supportive messages |

Run the moderation test suite:

```shell
python test-live-chat-moderation.py
```

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
