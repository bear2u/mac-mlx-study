---
title: "11 · RMSNorm 연산의 정확도와 속도"
description: "작은 연산을 바꾸었을 때 같은 결과를 더 빨리 얻을까?"
sidebar:
  order: 11
---

**작은 연산을 바꾸었을 때 같은 결과를 더 빨리 얻을까?**

RMSNorm은 벡터를 제곱 평균의 제곱근으로 나누고 가중치를 곱합니다. MLX는 계산을 지연하므로 시간을 잴 때 결과가 실제로 계산되도록 평가해야 합니다.

## 직접 해보기

아래 코드를 가상환경에서 실행하세요. 먼저 기본 연산 조합과 최적화 함수의 오차를 확인한 뒤, 입력 모양을 바꿔 반복합니다.

```python
import time
import mlx.core as mx

x = mx.random.normal((128, 4096))
w = mx.ones((4096,))
def reference():
    return x * mx.rsqrt(mx.mean(x * x, axis=-1, keepdims=True) + 1e-6) * w

def optimized():
    return mx.fast.rms_norm(x, w, 1e-6)

print("최대 절대 오차", mx.max(mx.abs(reference() - optimized())).item())
for fn in (reference, optimized):
    mx.eval(fn())
    start = time.perf_counter()
    for _ in range(100):
        mx.eval(fn())
    print(fn.__name__, (time.perf_counter() - start) * 10, "ms/회")
```

## 실험 노트

128행을 1행으로 바꿨을 때의 오차와 시간도 적습니다. 개별 연산이 빨라졌을 때 전체 모델에서 얻을 개선 폭은 10과의 프로파일에서 이 연산이 차지하는 비중과 연결해 설명하세요.

[공식 참고 자료](https://ml-explore.github.io/mlx/build/html/index.html)
