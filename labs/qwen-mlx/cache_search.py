from pathlib import Path

from huggingface_hub import snapshot_download
import tiktoken

for name, repo, patterns in [
    ("dense", "Qdrant/paraphrase-multilingual-MiniLM-L12-v2-onnx-Q",
     ["*.json", "model_optimized.onnx", "*.txt", "tokenizer.model"]),
    ("sparse", "Qdrant/bm25", ["*.json", "*.txt"]),
]:
    snapshot_download(repo, local_dir=Path("models") / name, allow_patterns=patterns)
print("토큰 인코딩 확인", tiktoken.get_encoding("cl100k_base").n_vocab)
