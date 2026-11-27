---
title: "07 · 직사각형 행렬 곱을 Metal로 작성"
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 07 · 직사각형 행렬 곱을 Metal로 작성

**이번 결과물은** `M × K`와 `K × N` 두 행렬을 받아 `M × N`을 반환하는 함수입니다. 출력 원소 하나를 스레드 하나에 배정합니다. 6단계의 `compare.py`가 있는 폴더에서 시작하세요.

## 1. 출력 인덱스에서 입력 위치 찾기

A의 r행과 B의 c열을 곱해 더하면 C의 (r, c)가 됩니다. 예를 들어 A의 첫 행이 [1, 2, 3]이고 B의 첫 열이 [1, 0, 1]이면 C의 첫 값은 4입니다. CPU float64 기준을 계산하려고 가상환경에서 `python -m pip install numpy`를 실행한 뒤 아래를 `matmul_lab.py`로 저장합니다.

```python
import numpy as np
from compare import mx, compare

kernel = mx.fast.metal_kernel(
    name="lab_matmul", input_names=["lhs", "rhs"], output_names=["out"],
    ensure_row_contiguous=True,
    source="""
    uint c = thread_position_in_grid.x, r = thread_position_in_grid.y;
    uint k = lhs_shape[1], n = rhs_shape[1];
    float sum = 0;
    for (uint i = 0; i < k; ++i)
        sum = metal::fma(lhs[r * k + i], rhs[i * n + c], sum);
    out[r * n + c] = sum;
    """,
)

def matmul(a, b):
    m, k = a.shape
    kb, n = b.shape
    assert min(m, k, n) > 0 and k == kb
    assert a.dtype == b.dtype == mx.float32
    return kernel(inputs=[a, b], grid=(n, m, 1),
                  threadgroup=(min(8, n), min(8, m), 1),
                  output_shapes=[(m, n)], output_dtypes=[mx.float32])[0]

if __name__ == "__main__":
    a = mx.array([[1., 2., 3.], [4., 5., 6.]])
    b = mx.array([[1., 0.], [0., 1.], [1., 1.]])
    print(matmul(a, b).tolist())
    mx.random.seed(8)
    for m, k, n in [(3, 5, 2), (33, 65, 17)]:
        a = mx.random.normal((m, k))
        b = mx.random.normal((k, n))
        aa = np.asarray(a, dtype=np.float64)
        bb = np.asarray(b, dtype=np.float64)
        expected = mx.array((aa @ bb).astype(np.float32))
        print((m, k, n))
        compare("직접 구현", lambda: matmul(a, b), expected)
        compare("MLX", lambda: a @ b, expected, atol=0.05)
```

## 2. 결과와 메모리 접근 해석

`python matmul_lab.py`를 실행하세요. 첫 출력은 `[[4.0, 5.0], [10.0, 11.0]]`입니다. 두 비교 입력은 모두 M, K, N이 달라 행과 열 인덱스를 뒤바꾼 실수를 잡을 수 있습니다. CPU float64로 계산한 기준값에 두 구현을 각각 대조합니다. 이 작은 난수 예제의 MLX GPU 내장 경로는 칩에 따라 곱셈 정밀도 차이가 관찰되어 내장 연산에 별도 절대 오차 한계 0.05를 둡니다. 출력된 오차와 입력 크기를 함께 기록하세요. 첫 행만 맞으면 A의 시작 위치 `r * k`, 첫 열만 맞으면 B의 열 간격 `i * n + c`를 다시 그려 보세요.

## 3. 다음 실험 정하기

32·64·128 정사각형 입력을 하나씩 추가하고 두 구현의 중앙값을 기록합니다. 이 커널에서 같은 행렬 원소를 몇 스레드가 다시 읽는지 세어 보세요. 5단계의 Instruments 추적으로 어느 크기부터 GPU 실행 구간이 길어지는지 비교할 수 있습니다. 8단계에서 전치한 K를 넣을 때는 MLX가 행 우선 입력을 준비하도록 지정한 옵션이 사용됩니다. [MLX 사용자 정의 Metal 커널](https://ml-explore.github.io/mlx/build/html/dev/custom_metal_kernels.html)

Source: https://bear2u.github.io/mac-mlx-study/projects/metal-kernels/07-matmul/index.mdx
