---
title: "02 · 세 추론 서버를 같은 주소에서 실행하기"
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 02 · 세 추론 서버를 같은 주소에서 실행하기

**목표**는 세 서버를 차례로 띄우고 같은 API 경로로 답을 받는 것입니다. 먼저 MLX 하나로 3~5단계를 끝낸 뒤 여기로 돌아와 나머지 서버를 각각 측정하세요. 아래 명령은 모두 **서버 터미널**에서 실행합니다.

## MLX-LM 설치와 시작

이후 메모리 측정을 위해 서버를 백그라운드로 띄우고 셸이 알려 주는 PID를 저장합니다. 로그는 작업 폴더에 남습니다.

```sh
cd ~/mac-inference-lab/benchmark
source .venv/bin/activate
python -m pip install mlx-lm
python -m pip freeze > mlx-packages.txt
mlx_lm.server --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --host 127.0.0.1 --port 8091 > mlx.log 2>&1 &
echo $! > server.pid
```

처음에는 모델 다운로드가 필요합니다. `tail -f mlx.log`로 로그를 보고 Ctrl+C로 로그 보기만 종료하세요. [MLX-LM 공식 저장소](https://github.com/ml-explore/mlx-lm)

## 준비 상태 확인과 엔진 교체

```sh
curl -fsS http://127.0.0.1:8091/v1/models | python -m json.tool
ps -p "$(cat server.pid)" -o pid,command
```

모델 목록 또는 해당 서버의 모델 정보가 보이고 PID의 명령이 방금 시작한 엔진인지 확인합니다. 연결이 거절되면 로그에서 다운로드와 초기화를 기다립니다. 포트 점유 오류가 보이면 `lsof -nP -iTCP:8091 -sTCP:LISTEN`으로 어떤 서버가 열려 있는지 확인하세요. 각 엔진의 5단계까지 측정한 후, 위에서 확인한 자신의 서버를 `kill "$(cat server.pid)"`로 종료합니다. 포트가 비고 이전 엔진이 메모리를 반납한 뒤 다음 엔진을 시작합니다.

## llama.cpp 설치와 시작

```sh
brew install llama.cpp
brew list --versions llama.cpp >> environment.txt
llama-server -hf Qwen/Qwen2.5-7B-Instruct-GGUF:Q4_K_M \
  --alias qwen-lab --host 127.0.0.1 --port 8091 \
  -c 8192 -np 4 > llama.log 2>&1 &
echo $! > server.pid
```

네 개의 동시 슬롯을 요청합니다. 로그에서 Metal 장치, 실제 컨텍스트 크기와 GGUF 파일명을 적으세요. 이 서버에서 요청할 모델 이름은 별칭 `qwen-lab`입니다. [llama.cpp 서버 옵션](https://github.com/ggml-org/llama.cpp/tree/master/tools/server) · [Qwen 공식 GGUF](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF)

## vLLM-Metal 설치와 시작

```sh
brew tap vllm-project/vllm-metal https://github.com/vllm-project/vllm-metal
brew install vllm-project/vllm-metal/vllm-metal
brew list --versions vllm-metal >> environment.txt
vllm serve mlx-community/Qwen2.5-7B-Instruct-4bit \
  --host 127.0.0.1 --port 8091 --max-model-len 2048 \
  --max-num-seqs 4 > vllm.log 2>&1 &
echo $! > server.pid
```

지원표에서 Qwen2.5의 MLX 경로와 모델 ID를 확인하세요. 메모리 부족으로 준비 단계가 실패하면 실행 중인 이전 서버를 확인합니다. 설정을 낮춰 다시 측정한 경우에는 변경한 값을 결과에 같이 남기세요. [지원 모델](https://github.com/vllm-project/vllm-metal/blob/main/docs/supported_models.md) · [공식 설치](https://github.com/vllm-project/vllm-metal#installation)

## 실험 기록

각 로그에서 모델 버전 또는 캐시 리비전, 양자화, 커맨드라인과 슬롯 설정을 기록합니다. 측정 중에는 서버 터미널을 열어 둡니다. 다음 단계는 다른 터미널에서 진행합니다.

Source: https://bear2u.github.io/mac-mlx-study/projects/benchmark/02-servers/index.mdx
