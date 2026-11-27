---
title: "01 · 맥에 실습 환경 준비하기"
description: "Ollama와 Python을 따로 점검하고 원본 앱의 버전을 고정합니다."
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 01 · 맥에 실습 환경 준비하기

**이번 실습의 질문**은 “건조함을 언제 반납하지?”입니다. 모델이 미리 알 수 없는 가상의 장비 규칙을 문서에 적어 두고, 나중에 모델이 어느 문장을 찾아 답했는지 확인합니다. 전체 앱은 내 맥에서 실행합니다. GitHub Pages는 강의를 읽는 곳입니다.

## 터미널과 모델 준비

Apple Silicon 맥에서 터미널을 열고 아래 두 명령을 실행하세요. 첫 결과는 arm64, 두 번째는 Git 버전이어야 합니다. Git 설치 창이 뜨면 명령행 도구 설치를 마칩니다.

```sh
uname -m
git --version
```

[Ollama macOS 앱](https://ollama.com/download/mac)을 설치해 실행한 뒤 새 터미널에서 확인합니다. 앱이 이미 실행 중이면 그 앱이 모델 서버 역할을 합니다. 모델을 처음 받을 때만큼은 다운로드 시간과 디스크 여유를 확보하세요.

```sh
ollama --version
curl -fsS http://localhost:11434/api/tags
ollama pull granite4.1:8b
ollama run granite4.1:8b "준비됐으면 준비라고 답해줘."
```

11434 연결이 거부되면 Ollama 앱을 먼저 엽니다. 명령이 없으면 앱의 CLI 설치 안내를 확인하고 터미널을 다시 엽니다. 작은 모델로 바꿀 수도 있지만 이 과정에서는 도구 호출 동작을 비교하기 위해 원본의 8B 모델을 사용합니다.

## 강의와 같은 버전 받기

```sh
mkdir -p ~/mac-inference-lab
cd ~/mac-inference-lab
git clone https://github.com/GiovanniPasq/agentic-rag-for-dummies.git
cd agentic-rag-for-dummies
git checkout --detach c1b339b54f0927bd0b469fcce70f3cd5de4e918d
git rev-parse --short HEAD
```

다음 단계부터는 이 저장소의 최상위 폴더에서 명령을 실행합니다. Python 환경 관리에는 uv를 씁니다. Homebrew를 쓰는 경우 아래 명령으로 설치할 수 있습니다. 다른 설치 방식은 [uv 설치 문서](https://docs.astral.sh/uv/getting-started/installation/)에 있습니다.

```sh
brew install uv
uv python install 3.12
uv sync --locked --python 3.12
uv run --locked python -V
```

**통과 기준** · Ollama 단독 질문에 답이 오고 Python 3.12가 출력됩니다. 텍스트 생성은 네이티브 Ollama가 맡습니다. 임베딩 및 검색은 Python 프로세스에서 실행되며, 별도의 Qdrant 서버나 클라우드 API 키는 필요하지 않습니다.

[이 단계의 원본 코드](https://github.com/GiovanniPasq/agentic-rag-for-dummies/blob/c1b339b54f0927bd0b469fcce70f3cd5de4e918d/pyproject.toml)

Source: https://bear2u.github.io/mac-mlx-study/agentic-rag/01-mac/index.mdx
