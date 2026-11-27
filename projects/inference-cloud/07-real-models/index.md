---
title: "07 · 실제 MLX 모델 연결과 최종 인수 실험"
description: "시험 서버를 로컬 LLM 두 개로 교체하고 실제 사용량을 확인합니다."
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 07 · 실제 MLX 모델 연결과 최종 인수 실험

## 엔진 하나부터 교체하기

연습용 엔진을 종료하고 터미널 A의 같은 가상환경에서 실행합니다. 모델을 처음 내려받을 때는 인터넷 연결과 디스크 공간이 필요합니다.

```sh
source engine.env
python -m pip install -U mlx-lm
mlx_lm.server --model "$MODEL_SMALL" --host 127.0.0.1 --port 8091
```

터미널 B에서 6단계의 정상 요청을 보내세요. 자유로운 문장과 실제 token usage가 나타나야 합니다. 오래된 엔진에서 usage를 보내지 않으면 DB에 NULL로 남습니다. `python -m pip show mlx-lm`으로 버전을 적고 서버가 include_usage를 지원하는지 확인하세요. [MLX-LM 서버 구현](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/server.py)

## 두 번째 모델로 라우팅하기

메모리 여유를 확인한 뒤 새 터미널 D에서 실행합니다.

```sh
cd ~/mac-inference-lab/cloud
source .venv/bin/activate
source engine.env
mlx_lm.server --model "$MODEL_LARGE" --host 127.0.0.1 --port 8092
```

6단계의 curl 본문에서 model을 deep으로 바꾸고 같은 질문을 보냅니다. 게이트웨이의 /usage에서 모델 별칭을, 엔진 터미널에서 실제 요청 도착을 대조합니다. 두 모델이 한꺼번에 메모리에 들어가지 않으면 한 엔진을 끈 뒤 다른 엔진을 시험하고 순차 실험이라고 기록하세요.

## 실험을 마치는 기준

| 검증 항목 | 남길 증거 |
| --- | --- |
| 인증과 격리 | Alice 요청이 Bob의 사용 기록에서 보이지 않음 |
| 모델 선택 | 같은 질문을 보낸 두 별칭과 해당 엔진의 요청 로그 |
| 스트리밍 | 첫 내용, 마지막 DONE, 응답 헤더의 요청 ID |
| 대기열 | 네 요청의 상태 코드, 대기 시간, 완료 건수 |
| 취소·복구 | 중단 요청 상태와 직후 정상 요청의 완료 기록 |

가상환경에서 `python -m pip freeze > requirements.lock.txt`로 버전을 남기세요. 각 터미널의 프로세스를 Ctrl+C로 종료하고, 다시 시작할 때는 엔진부터 띄운 뒤 게이트웨이를 실행합니다. DB를 그대로 두면 키와 사용 기록을 이어 쓸 수 있습니다.

Source: https://bear2u.github.io/mac-mlx-study/projects/inference-cloud/07-real-models/index.mdx
