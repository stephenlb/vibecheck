# VibeCheck

No AI training - Classify any text in +100 Languages.
Dynamic Classifiaction of text in +100 langauges.
Detect positivity, negativity, priase, nsfw.

## Installation and Running

```shell
## Login to HG beacuse of license
hg auth login
## UV
uv install -r requirements.txt 
## OR PIP
pip install -r requirements.txt
docker build . -t vibecheck
```

## TODO

 - ✅ simplify ( and it works )
 - ✅ Add FastAPI ( turn this into an API )
 - Dockerizer
 - Yaml definitions

## Architecture

'happy joy awesome' => embeddinggemma => baseline vectors (use for distance comparison)
text input => embeddinggemma => vectors - basline = some value

## Datasets

 - positive phrases
 - negative phrases

## Why Gemma Emedding

 - Multi-lingual

