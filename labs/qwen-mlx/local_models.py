import os
from pathlib import Path
from urllib.request import urlopen
import json

from fastembed import TextEmbedding
from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI

MODELS = Path(__file__).resolve().parents[3] / "models"


class LocalDense(Embeddings):
    def __init__(self):
        self.model = TextEmbedding(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            specific_model_path=str(MODELS / "dense"), local_files_only=True, threads=4,
        )

    def embed_documents(self, texts):
        return [v.tolist() for v in self.model.embed(texts)]

    def embed_query(self, text):
        return next(self.model.query_embed(text)).tolist()


def chat_model():
    port = int(os.environ.get("RAG_MLX_PORT", "11343"))
    base = f"http://127.0.0.1:{port}/v1"
    with urlopen(base + "/models", timeout=15) as response:
        model = json.load(response)["data"][0]["id"]
    return ChatOpenAI(base_url=base, api_key="local", model=model, temperature=0,
                      extra_body={"reasoning_effort": "low"}, timeout=150,
                      use_responses_api=False, max_retries=0)
