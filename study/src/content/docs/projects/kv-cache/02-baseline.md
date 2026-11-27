---
title: "02 · 캐시 없이 첫 토큰 시간 재기"
description: "문서와 질문 전체를 읽는 기준 실행을 만듭니다. 뒤에서 같은 입력 토큰으로 캐시 경로와 비교합니다."
sidebar:
  order: 2
---

문서와 질문 전체를 읽는 기준 실행을 만듭니다. 뒤에서 같은 입력 토큰으로 캐시 경로와 비교합니다.

## 템플릿과 측정 함수

실습 폴더에 `common.py`로 저장하세요. 모델 로딩은 타이머 밖에 둡니다. 이 과정에서 TTFT는 토큰 ID가 처음 반환될 때까지의 시간입니다. 화면에 글자가 보일 때까지, 또는 네트워크를 포함한 서버 지연과는 측정 경계가 다릅니다.

```python
import json
from pathlib import Path
from time import perf_counter
from mlx_lm import load, stream_generate
from mlx_lm.sample_utils import make_sampler

spec = json.loads(Path("model.json").read_text())
system = "문서에 근거해서 짧게 대답하세요."

def inputs(tok, doc, question):
    messages = [{"role":"system", "content":system},
                {"role":"user", "content":"자료\n" + doc + "\n질문\n" + question}]
    rendered = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    return tok.encode(rendered, add_special_tokens=False)

def answer(model, tok, ids, cache=None):
    start = perf_counter()
    tokens, text = [], []
    for step in stream_generate(model, tok, prompt=ids, prompt_cache=cache,
                                sampler=make_sampler(temp=0.0), max_tokens=24):
        if not tokens:
            first_at = perf_counter()
        tokens.append(step.token)
        text.append(step.text)
    return dict(first_at=first_at, ttft=first_at-start, tokens=tokens, text="".join(text))

if __name__ == "__main__":
    model, tok = load(spec["path"])
    doc = Path("document.txt").read_text()
    question = "1번 서랍의 종이 색은?"
    ids = inputs(tok, doc, question)
    answer(model, tok, ids)
    result = answer(model, tok, ids)
    print(len(ids), "입력 토큰", round(result["ttft"], 3), "초", result["text"])
```

## 기준값 기록

`python common.py`를 실행하세요. 같은 프로세스에서 한 차례 준비 실행을 마치고 다음 요청을 측정합니다. 첫 측정에서는 입력 토큰 수, 초 단위 TTFT, 답변을 한 줄에 남깁니다.

**확인** · 모델이 틀린 답을 주더라도 실제 출력은 보존하세요. 캐시 검증의 첫 질문은 “캐시를 사용해도 같은 모델의 답이 유지되는가?”입니다. 사실 정답 여부도 따로 기록합니다.

**막힐 때** · model.json 파일 오류가 나면 현재 폴더에서 `pwd`와 `ls`를 확인합니다. 입력 길이 오류가 나면 prepare.py의 문서 생성 범위를 줄인 뒤 전체 실험의 문서 길이를 같이 바꾸세요. [MLX-LM 스트리밍 생성](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/generate.py)
