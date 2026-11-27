---
title: "06 · 모델 하나를 두 맥에 분할하고 비교"
sidebar:
  order: 6
---

**목표** · 5단계에서 확인한 두 프로세스가 같은 토큰 한 개를 함께 계산하게 합니다. Qwen3의 텐서 분할은 각 레이어의 attention·MLP 행렬을 두 장비에 나누고 중간 결과를 통신합니다. 모델 파일은 두 장비에 모두 캐시될 수 있습니다. 파일 크기와 실행 중 메모리를 구분해 기록하세요.

## 1. 단일·분산 공용 측정 파일 만들기

A의 실습 폴더에 `shard.py`를 저장합니다. 단일 프로세스이면 보통 방식으로, 분산 그룹이면 tensor_group을 지정해 모델을 로드합니다. 모든 rank가 생성 루프를 실행해야 동일한 순서로 통신합니다.

```python
import socket
from time import perf_counter
import mlx.core as mx
from mlx_lm import load, stream_generate
from mlx_lm.utils import sharded_load
from mlx_lm.sample_utils import make_sampler

repo = "mlx-community/Qwen3-0.6B-4bit"
group = mx.distributed.init()
if group.size() == 1:
    model, tok = load(repo)
else:
    model, tok = sharded_load(repo, tensor_group=group)
print(socket.gethostname(), "rank", group.rank(), "그룹 크기", group.size(),
      "로드 후 MLX GB", round(mx.get_active_memory() / 1e9, 3), flush=True)
prompt = tok.apply_chat_template(
    [{"role": "user", "content": "달과 지구의 차이를 한 문장으로 설명해줘. /no_think"}],
    tokenize=False, add_generation_prompt=True,
)
for run in range(4):
    start = perf_counter()
    ttft = None
    pieces = []
    for item in stream_generate(model, tok, prompt, sampler=make_sampler(temp=0.0),
                                max_tokens=64):
        if ttft is None:
            ttft = perf_counter() - start
        pieces.append(item.text)
    if group.rank() == 0:
        print(run, "첫 생성 이벤트(초)", ttft, "전체(초)", perf_counter() - start,
              "출력 토큰", item.generation_tokens, "본문", "".join(pieces), flush=True)
print(socket.gethostname(), "최대 MLX GB", round(mx.get_peak_memory() / 1e9, 3))
```

## 2. 같은 파일을 두 방식으로 실행하기

```sh
cd /Users/Shared/mac-inference-lab
source venv/bin/activate
scp shard.py "$BOOK_SSH":/Users/Shared/mac-inference-lab/
python shard.py | tee single.txt
mlx.launch --backend ring --hostfile hosts.json --   /Users/Shared/mac-inference-lab/venv/bin/python /Users/Shared/mac-inference-lab/shard.py | tee split.txt
```

단일 로그는 그룹 크기 1, 분산 로그는 서로 다른 호스트에 그룹 크기 2가 나와야 합니다. `sharded_load`가 텐서 병렬 미지원 오류를 내면 설치된 mlx-lm의 Qwen3 구현과 버전이 두 장비에서 일치하는지 확인합니다. 5단계의 합산 검사를 다시 돌리면 모델 로딩 문제와 네트워크 문제를 구분할 수 있습니다.

## 3. 결과표 완성하기

각 로그의 0번 실행은 준비 실행입니다. 나머지 세 번의 중앙값을 사용합니다. 첫 생성 이벤트 시간은 모델을 로드한 후부터 재므로 웹 서버의 사용자 TTFT와 별도 열에 둡니다. MLX 메모리는 장비 전체 메모리와도 구별하세요.

| 구성 | 측정할 작업 | 결과 |
| --- | --- | --- |
| 맥 한 대 | 요청 네 개 처리량 / 모델 한 개 생성 지연 | 4단계 직접 호출 / single.txt |
| 두 대에 모델 복제 | 요청 네 개 처리량 / 한 대 중단 시 성공 수 | 4단계 라우터 실험 |
| 두 대에 텐서 분할 | 단일 생성 지연 / 각 rank의 메모리 | split.txt |

마지막으로 “이 모델에서 요청이 많을 때는 ___, 장비당 메모리가 제약일 때는 ___을 선택한다”를 측정값으로 완성합니다. 두 대의 속도·메모리가 서로 다르거나 통신 시간이 길면 모델 분할 후 생성 지연이 늘 수 있습니다. [MLX-LM 분할 로딩 구현](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/utils.py) · [Qwen3 텐서 분할 구현](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/models/qwen3.py)
