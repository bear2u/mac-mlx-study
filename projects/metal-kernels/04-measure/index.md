---
title: "04 · 실행 시간과 정확도를 같은 표에 기록"
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 04 · 실행 시간과 정확도를 같은 표에 기록

**준비** · `python check.py`의 모든 단언이 통과한 상태에서 시작합니다. 한 토큰 처리에 가까운 한 행과 여러 행을 묶은 입력에서 각각 어떤 구현이 유리한지 측정합니다.

## 1. 같은 데이터로 네 구현 비교하기

`bench.py`를 아래 내용으로 저장합니다. 최초 컴파일과 입력 난수 생성은 측정에서 분리합니다. 반복마다 새 결과를 `mx.eval`로 평가해 CPU가 계산을 예약한 시점만 재는 일을 피합니다. 시간에는 Python 호출과 결과 동기화도 포함됩니다.

```python
import csv
from statistics import median
from time import perf_counter_ns
from baseline import EPS, mx, reference
from kernels import serial, parallel

def builtin(x, w):
    return mx.fast.rms_norm(x, w, EPS)

mx.random.seed(7)
with open("timings.csv", "w", newline="") as output:
    table = csv.writer(output)
    table.writerow(["rows", "cols", "method", "median_us", "max_abs_error"])
    for rows, cols in [(1, 4096), (128, 4096), (128, 4097)]:
        x, w = mx.random.normal((rows, cols)), mx.random.normal((cols,))
        expected = reference(x, w)
        mx.eval(x, w, expected)
        for fn in (reference, serial, parallel, builtin):
            result = fn(x, w)
            mx.eval(result)
            error = mx.max(mx.abs(expected - result)).item()
            assert mx.allclose(result, expected, rtol=1e-4, atol=1e-5).item()
            times = []
            for repeat in range(31):
                start = perf_counter_ns()
                mx.eval(fn(x, w))
                times.append((perf_counter_ns() - start) / 1000)
            table.writerow([rows, cols, fn.__name__, median(times), error])
```

## 2. 결과 해석하기

```sh
python bench.py
column -s, -t timings.csv
```

헤더 아래에 12개 행이 생깁니다. 같은 입력의 serial 중앙값을 parallel 중앙값으로 나눈 배율을 적어 보세요. 1보다 작다면 그 입력에서는 추가 스레드의 동기화 비용을 조사합니다. 작은 시간 차이는 다른 앱의 GPU 사용을 줄인 뒤 전체 실행을 세 번 반복해 방향이 유지되는지 확인하세요.

Source: https://bear2u.github.io/mac-mlx-study/projects/metal-kernels/04-measure/index.mdx
