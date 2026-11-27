---
title: "01 · 같은 원본 모델 확보하기"
description: "Qwen 원본 한 벌과 내려받은 버전 번호를 고정합니다. 이후 모든 변환은 이 가중치에서 출발합니다."
sidebar:
  order: 1
---

Qwen 원본 한 벌과 내려받은 버전 번호를 고정합니다. 이후 모든 변환은 이 가중치에서 출발합니다.

## 준비

Apple Silicon 맥과 arm64용 Python 3.11 이상을 준비하세요. 첫 실습에는 0.5B 모델을 씁니다. 원본·변환본·다운로드 캐시를 함께 둘 여유가 있는지 먼저 확인하세요.

```sh
mkdir -p ~/mac-inference-lab/quantization
cd ~/mac-inference-lab/quantization
uname -m
df -h .
python3 -m venv .venv
source .venv/bin/activate
python -m pip install mlx-lm huggingface_hub
python -m pip freeze > requirements-lock.txt
```

## 원본과 버전 기록

아래 블록을 터미널에서 통째로 실행하세요. 공개 저장소의 현재 커밋을 확인한 뒤 해당 커밋의 파일을 내려받습니다. 다음에 재현할 때는 생성된 source.json의 revision을 사용하세요.

```sh
python - <<'PYCODE'
from huggingface_hub import model_info, snapshot_download
from pathlib import Path
import json
repo = "Qwen/Qwen2.5-0.5B-Instruct"
revision = model_info(repo).sha
path = snapshot_download(repo, revision=revision, allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model", "*.jinja"])
Path("source.json").write_text(json.dumps(dict(repo=repo, revision=revision, path=path), indent=2))
print(revision, path)
PYCODE
```

**확인** · `cat source.json`에서 revision과 로컬 경로를 확인합니다. 새 터미널을 열면 이 과의 cd와 source 명령을 다시 실행하세요. 다음 과에서는 source.json에서 경로를 읽습니다.

**막힐 때** · uname 결과가 x86_64이면 Apple Silicon 기본 터미널과 arm64 Python으로 가상환경을 새로 만드세요. 다운로드 도중 연결이 끊기면 같은 revision을 지정해 다시 받으세요. [원본 모델 카드](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct)
