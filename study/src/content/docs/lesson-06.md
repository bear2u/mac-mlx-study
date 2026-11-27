---
title: "06 · KV 캐시의 메모리 비용"
description: "대화가 길어지면 어떤 데이터가 쌓일까?"
sidebar:
  order: 6
---

**대화가 길어지면 어떤 데이터가 쌓일까?**

Attention은 이전 토큰의 Key와 Value를 다시 참조합니다. 레이어마다 이를 보관하면 매 단계에서 앞부분을 다시 계산하는 일을 줄일 수 있습니다. 일반적인 전체 길이 캐시의 크기는 토큰 수에 비례합니다.

## 직접 해보기

다음 식으로 단일 요청의 캐시 크기를 계산해 보세요. K와 V 두 배열이 있어 계수가 2입니다.

```python
for tokens in [1024, 4096, 8192]:
    size = 2 * 32 * 8 * 128 * tokens * 2
    print(tokens, size / 1024**2, "MiB")
```

예시 모델은 32개 레이어, KV 헤드 8개, 헤드 차원 128, 원소당 2바이트를 가정합니다. 실제 모델 설정의 num_hidden_layers, num_key_value_heads와 head_dim을 찾아 대입하세요. head_dim이 없으면 이 모델에서는 hidden_size를 num_attention_heads로 나눕니다.

## 실험 노트

예시에서 1,024토큰은 128MiB입니다. 4,096토큰의 결과와 3과에서 본 전체 최대 메모리가 왜 다른지 설명합니다.

[공식 참고 자료](https://github.com/ml-explore/mlx-lm)
