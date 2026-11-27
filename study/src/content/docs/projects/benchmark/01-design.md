---
title: "01 · 실험 폴더와 비교 조건 만들기"
sidebar:
  order: 1
---

**이번 단계에서 만들 것**은 측정 환경을 기록한 `environment.txt`와 세 엔진이 함께 읽는 질문 파일입니다. 마지막 단계에서는 이 파일로 얻은 실측 결과를 웹에서 비교합니다.

## 실험할 질문

맥 한 대에서 같은 한국어 질문 네 개를 처리합니다. 하나씩 보낼 때와 네 개를 동시에 보낼 때 **첫 글자를 받기까지 걸린 시간**, **네 답변 전체의 출력 토큰 처리량**, **관찰된 서버 메모리**를 비교합니다. 짧은 답변도 실제 생성한 토큰 수로 계산합니다.

## 폴더 준비

Apple Silicon 맥, Homebrew, Python 3.10 이상, 모델을 받을 인터넷 연결을 준비합니다. vLLM-Metal의 macOS 요구 버전도 확인합니다. 터미널 한 개는 서버용, 다른 한 개는 측정용으로 씁니다. [vLLM-Metal 설치 조건](https://github.com/vllm-project/vllm-metal#requirements)

```sh
mkdir -p ~/mac-inference-lab/benchmark/results
cd ~/mac-inference-lab/benchmark
python3 --version
python3 -m venv .venv
source .venv/bin/activate
{ uname -m; sw_vers; sysctl -n machdep.cpu.brand_string hw.memsize; python -V; } > environment.txt
cat environment.txt
```

첫 줄이 arm64인지 확인합니다. 마지막에서 두 번째 숫자는 메모리 바이트 수입니다. Rosetta 터미널에서 x86_64가 보이면 기본 터미널로 다시 시작합니다.

## 질문 세트 고정

다음 블록을 **실습 폴더 안에서** 실행합니다. 이후 모든 터미널에서 같은 폴더를 사용합니다.

```sh
cat > prompts.txt <<'TEXT'
KV 캐시가 무엇인지 한국어 두 문장으로 설명해줘.
언어 모델 양자화의 장단점을 하나씩 적어줘.
첫 토큰 시간이 무엇인지 예를 들어 설명해줘.
통합 메모리와 모델 크기의 관계를 두 문장으로 설명해줘.
TEXT
wc -l prompts.txt
shasum -a 256 prompts.txt
```

질문 수는 4입니다. 해시값은 질문이 같았는지 확인하는 실험 식별자로 쓰입니다. 샘플링 온도는 0, 요청당 출력 상한은 64토큰, 준비 실행 후 조건별 반복은 세 번으로 고정합니다. 서버 기본 캐시를 사용하므로 **동일 질문이 반복되는 환경**의 성능을 측정합니다.

## 완료 확인

Qwen2.5-7B-Instruct를 공통 원본으로 사용합니다. MLX용 4비트와 GGUF Q4_K_M은 서로 다른 변환입니다. 서버 설정, 모델 파일 형식, 캐시 동작이 관찰 결과에 함께 반영됩니다. 다음 단계에서 동일한 모델 계열의 서버 세 종류를 준비합니다.
