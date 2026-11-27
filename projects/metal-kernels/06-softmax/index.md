---
title: "06 · 큰 입력에서도 안정적인 Softmax 작성"
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 06 · 큰 입력에서도 안정적인 Softmax 작성

이번에는 토큰 점수 한 행을 확률 한 행으로 바꿉니다. 1단계에서 만든 `~/mac-inference-lab/metal`과 가상환경을 그대로 사용합니다. 이 단계에서 만드는 두 함수는 다음 두 실습에서도 사용합니다.

## 1. 검증과 시간 측정 공통화

`compare.py`로 저장합니다. GPU 계산을 동기화하는 위치는 4단계와 같습니다. 함수 하나를 21번 호출해 중앙값을 마이크로초로 출력합니다. 측정값에는 Python 호출 및 동기화 비용이 포함됩니다.

```python
from statistics import median
from time import perf_counter_ns
import mlx.core as mx

def compare(name, fn, expected, *, atol=2e-5):
    out = fn()
    mx.eval(out, expected)
    error = mx.max(mx.abs(out - expected)).item()
    assert mx.allclose(out, expected, rtol=2e-4, atol=atol).item(), (name, error)
    samples = []
    for _ in range(21):
        start = perf_counter_ns()
        mx.eval(fn())
        samples.append((perf_counter_ns() - start) / 1000)
    print(f"{name:16s} 중앙값 {median(samples):8.1f} µs  최대 절대 오차 {error:.2g}")
```

## 2. Metal에서 행 최대값과 지수 합 구하기

`softmax_lab.py`로 저장합니다. 점수에 1000이 들어오면 지수를 그대로 계산할 때 float32 범위를 넘습니다. 모든 점수에서 같은 최댓값을 빼면 분자와 분모를 같은 수로 나눈 효과가 있어 확률은 유지됩니다.

```python
from compare import mx, compare

kernel = mx.fast.metal_kernel(
    name="lab_stable_softmax", input_names=["inp"], output_names=["out"],
    source="""
    uint r = thread_position_in_grid.x;
    uint n = inp_shape[1], start = r * n;
    float maximum = inp[start];
    for (uint c = 1; c < n; ++c)
        maximum = metal::max(maximum, inp[start + c]);
    float total = 0;
    for (uint c = 0; c < n; ++c) {
        float value = metal::exp(inp[start + c] - maximum);
        out[start + c] = value;
        total += value;
    }
    for (uint c = 0; c < n; ++c)
        out[start + c] /= total;
    """,
)

def softmax(x):
    rows, cols = x.shape
    assert rows > 0 and cols > 0 and x.dtype == mx.float32
    return kernel(inputs=[x], grid=(rows, 1, 1), threadgroup=(min(32, rows), 1, 1),
                  output_shapes=[x.shape], output_dtypes=[x.dtype])[0]

if __name__ == "__main__":
    x = mx.array([[1000., 1001.], [-1000., -999.]])
    print(softmax(x).tolist())
    mx.random.seed(7)
    for shape in [(1, 3), (16, 65)]:
        x = mx.random.normal(shape)
        expected = mx.softmax(x, axis=-1)
        print(shape)
        assert mx.allclose(mx.sum(softmax(x), axis=-1), mx.ones((shape[0],))).item()
        compare("직접 구현", lambda: softmax(x), expected)
        compare("MLX", lambda: mx.softmax(x, axis=-1), expected)
```

## 3. 실행과 점검

`python softmax_lab.py`를 실행합니다. 첫 두 행은 모두 약 `[0.26894, 0.73106]`입니다. 둘 다 같은 점수 차이 1을 갖기 때문입니다. 모든 행의 확률 합과 원소별 오차 검사가 통과해야 합니다. 65열 입력은 스레드 폭의 배수가 아닌 경우입니다. 한 행 전체가 마스킹되어 점수가 모두 음의 무한대라면 이 구현의 입력 범위를 벗어납니다. 8단계에서는 각 행에 최소 한 토큰을 남깁니다. [MLX Softmax](https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.softmax.html)

Source: https://bear2u.github.io/mac-mlx-study/projects/metal-kernels/06-softmax/index.mdx
