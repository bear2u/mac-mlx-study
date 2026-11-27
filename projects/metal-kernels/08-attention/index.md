---
title: "08 · Causal Attention 조립과 정답 검증"
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 08 · Causal Attention 조립과 정답 검증

마지막 실습에서는 6·7단계의 **직접 작성한 두 Metal 커널**로 단일 헤드의 causal self-attention을 만듭니다. 입력 Q, K, V는 모두 (토큰 수, 헤드 차원)의 float32 행렬입니다. t번째 출력은 0번부터 t번까지의 V만 섞어야 합니다.

## 1. 점수, 마스크, 가중 합 연결

`attention_lab.py`로 저장합니다. 첫 번째 행렬 곱은 각 질문과 키의 유사도를 계산하고 두 번째는 확률로 값 벡터를 섞습니다. 마지막 출력은 다시 (토큰 수, 헤드 차원)이 됩니다.

```python
import numpy as np
from compare import mx, compare
from softmax_lab import softmax
from matmul_lab import matmul

def attention(q, k, v, allowed):
    d = q.shape[1]
    scores = matmul(q, k.T) * (d ** -0.5)
    masked = mx.where(allowed, scores, -float("inf"))
    return matmul(softmax(masked), v)

def builtin(q, k, v):
    # MLX 내장 연산의 입력 차원은 (배치, 헤드, 토큰, 헤드 차원)
    return mx.fast.scaled_dot_product_attention(
        q[None, None], k[None, None], v[None, None],
        scale=q.shape[1] ** -0.5, mask="causal",
    )[0, 0]

def causal_mask(n):
    positions = mx.arange(n)
    return positions[:, None] >= positions[None, :]

if __name__ == "__main__":
    n, d = 3, 32
    q = k = mx.zeros((n, d))
    v = mx.broadcast_to(mx.array([[2.], [4.], [9.]]), (n, d))
    out = attention(q, k, v, causal_mask(n))
    print("손계산 결과", out[:, 0].tolist())
    assert mx.allclose(out[:, 0], mx.array([2., 3., 5.])).item()

    mx.random.seed(9)
    for n in (8, 33):
        q, k, v = [mx.random.normal((n, d)) for _ in range(3)]
        allowed = causal_mask(n)
        mx.eval(q, k, v, allowed)
        qq, kk, vv = [np.asarray(x, dtype=np.float64) for x in (q, k, v)]
        scores = (qq @ kk.T) / (d ** 0.5)
        scores[np.triu_indices(n, k=1)] = -np.inf
        weights = np.exp(scores - scores.max(axis=1, keepdims=True))
        weights /= weights.sum(axis=1, keepdims=True)
        expected = mx.array((weights @ vv).astype(np.float32))
        actual = attention(q, k, v, allowed)
        # 마지막 위치의 V만 변경해도 이전 n-1개 출력은 같아야 한다.
        v2 = mx.concatenate([v[:-1], v[-1:] + 40], axis=0)
        changed = attention(q, k, v2, allowed)
        assert mx.allclose(actual[:-1], changed[:-1]).item()
        print("토큰 수", n)
        compare("직접 조립", lambda: attention(q, k, v, allowed), expected)
        compare("MLX 내장", lambda: builtin(q, k, v), expected, atol=0.01)
```

## 2. 미래 정보가 섞이는지 확인

`python attention_lab.py`를 실행합니다. Q와 K가 0인 예에서는 허용되는 점수가 전부 같으므로 균등하게 섞입니다. 첫 토큰은 2만 보고, 둘째 토큰은 (2+4)/2, 셋째 토큰은 (2+4+9)/3을 봅니다. 7단계처럼 CPU float64로 마스크와 가중합을 독립 계산합니다. 이 입력에서 내장 GPU 경로의 정확도 차이를 관찰하기 위해 내장 연산의 절대 오차 한계를 0.01로 둡니다. 첫 출력까지 5가 나오면 미래 위치도 허용한 것입니다. 행을 질의, 열을 키로 해석했는지 확인합니다.

## 3. 성능 보고서 마무리

`report.md`에 n=8과 33의 직접 조립·내장 시간, 최대 절대 오차를 추가합니다. 조립 구현은 토큰 수 × 토큰 수 크기의 점수와 확률 배열을 중간에 계산합니다. n을 두 배로 키우면 해당 배열의 원소 수와 실측 시간이 각각 어떻게 달라지는지 예측하고 재측정하세요. 내장 함수는 구현 경로에 따라 연산들을 결합할 수 있습니다. 이번 입력 크기에서 얻은 속도 차이를 실제 모델 전체에서 확인하려면 그 모델의 배치, 헤드 수, 컨텍스트 길이 조건도 재현해야 합니다. [MLX Scaled Dot Product Attention](https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.fast.scaled_dot_product_attention.html)

Source: https://bear2u.github.io/mac-mlx-study/projects/metal-kernels/08-attention/index.mdx
