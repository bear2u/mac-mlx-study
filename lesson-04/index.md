---
title: "04 · 4비트와 8비트 비교하기"
description: "메모리를 줄이면 내 과제의 정답률은 얼마나 달라질까?"
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 04 · 4비트와 8비트 비교하기

**메모리를 줄이면 내 과제의 정답률은 얼마나 달라질까?**

양자화는 가중치를 적은 비트로 표현합니다. 70억 개를 4비트로 저장하면 가중치만 약 3.5GB입니다. 실제 최대 메모리에는 양자화 부가 정보, 캐시, 연산 공간도 들어갑니다.

## 직접 해보기

같은 모델의 두 양자화판에 아래 질문을 실행하세요. 메모리 여유를 확인한 뒤 한 번에 하나씩 실행합니다.

```sh
for bits in 4 8; do
  mlx_lm.generate --model "mlx-community/Qwen2.5-7B-Instruct-${bits}bit" --prompt "상자 17개에 연필이 6자루씩 있다. 총 몇 자루인가? 숫자만 써." --max-tokens 32 --temp 0
done
```

정답 102와 비교합니다. 직접 채점할 수 있는 계산·문서 발췌 질문 9개를 더 준비해 같은 순서로 테스트하세요.

## 실험 노트

각 모델의 정답 수/10, 생성 속도, 최대 메모리를 표로 작성하세요. 두 모델이 모두 맞힌 문제와 한 모델만 틀린 문제를 따로 살펴봅니다.

[공식 참고 자료](https://github.com/ml-explore/mlx-lm)

Source: https://bear2u.github.io/mac-mlx-study/lesson-04/index.mdx
