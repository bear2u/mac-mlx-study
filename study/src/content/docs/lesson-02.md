---
title: "02 · 다음 토큰이 정해지는 과정"
description: "모델이 문장을 어디에서 끊어 읽을까?"
sidebar:
  order: 2
---

**모델이 문장을 어디에서 끊어 읽을까?**

토크나이저는 문자열을 정수 ID의 열로 바꿉니다. Transformer의 causal attention은 현재 위치까지의 토큰을 참고하고, 최종 층은 다음 토큰 후보마다 점수를 냅니다. 선택한 ID를 입력 뒤에 붙이면 한 번의 생성 단계가 끝납니다.

## 직접 해보기

1과의 가상환경에서 아래 코드를 실행한 뒤 문장 앞에 공백을 넣거나 숫자를 바꾸어 보세요.

```python
import os
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained(os.environ["MODEL"])
for sentence in ["맥에서 추론하기", " 맥에서 추론하기", "맥에서 2026번"]:
    ids = tok.encode(sentence, add_special_tokens=False)
    print(sentence, ids, len(ids), tok.decode(ids))
```

## 실험 노트

문자 수와 토큰 수를 나란히 적습니다. 같은 단어도 주변 문자에 따라 묶이는 방식이 달라지는지 실제 ID를 근거로 설명하세요.

[공식 참고 자료](https://huggingface.co/docs/transformers/main_classes/tokenizer)
