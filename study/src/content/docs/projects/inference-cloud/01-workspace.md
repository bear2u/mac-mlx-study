---
title: "01 · 실습 폴더와 서버 배치 준비"
description: "사용자 요청이 게이트웨이와 모델 서버를 거쳐 돌아오는 경로를 설계합니다."
sidebar:
  order: 1
---

사용자는 8090번 게이트웨이에 API 키와 질문을 보냅니다. 게이트웨이는 키를 확인하고 요청을 기다리게 한 뒤, 선택한 모델 서버에서 도착하는 답을 즉시 전달합니다. 마지막에는 요청 한 건의 상태와 사용량을 SQLite에 남깁니다.

| 프로세스 | 주소 | 역할 |
| --- | --- | --- |
| 게이트웨이 | 127.0.0.1:8090 | 인증, 대기열, 모델 선택, 스트리밍 중계 |
| fast 모델 | 127.0.0.1:8091 | 작은 모델 또는 연습용 서버 |
| deep 모델 | 127.0.0.1:8092 | 두 번째 모델 |

## 환경 만들기

Python 3.11 이상이 설치된 Apple Silicon 맥을 사용합니다. 명령은 macOS 터미널의 zsh 기준입니다. Python 버전과 아키텍처부터 확인하세요.

```sh
python3 --version
uname -m
mkdir -p ~/mac-inference-lab/cloud
cd ~/mac-inference-lab/cloud
python3 -m venv .venv
source .venv/bin/activate
python -m pip install 'fastapi>=0.115,<1' 'httpx>=0.27,<1' 'uvicorn>=0.30,<1'
python -c 'import fastapi, httpx, uvicorn; print(fastapi.__version__)'
```

명령이 버전 번호를 출력하면 기본 준비가 끝났습니다. 실습용 서버로 게이트웨이를 먼저 완성할 수 있고, 실제 모델은 7단계에서 연결합니다.

## 새 터미널 열 때마다

```sh
cd ~/mac-inference-lab/cloud
source .venv/bin/activate
```

이 경로에 이후 페이지의 파일을 저장합니다. 8090~8092 포트가 이미 사용 중이면 `lsof -nP -iTCP:8090 -sTCP:LISTEN`으로 어떤 서비스인지 확인하고, 실습 포트를 바꾼다면 서버와 호출 코드의 주소를 함께 맞추세요.
