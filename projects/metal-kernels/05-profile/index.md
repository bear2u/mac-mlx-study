---
title: "05 · GPU 프로파일로 개선 효과 설명하기"
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 05 · GPU 프로파일로 개선 효과 설명하기

**목표** · 어떤 입력에서 커널 변경이 이득인지 실측 근거를 남깁니다. Xcode에 포함된 Instruments와 4단계의 `timings.csv`를 사용합니다.

## 1. 추적할 구간 길게 만들기

짧은 벤치마크는 프로세스에 연결하기 전에 끝날 수 있습니다. 다음을 `profile_run.py`로 저장하고 실행한 뒤 첫 입력 대기 상태로 둡니다.

```python
import os
from baseline import mx
from kernels import serial, parallel

x = mx.random.normal((128, 4096))
w = mx.ones((4096,))
mx.eval(serial(x, w), parallel(x, w))
print("Python PID", os.getpid(), flush=True)
for fn in (serial, parallel):
    input(f"{fn.__name__} 측정을 시작하려면 Enter ")
    for _ in range(1200):
        mx.eval(fn(x, w))
    print(fn.__name__, "완료", flush=True)
```

## 2. 두 구간을 대조하기

1. Xcode에서 **Open Developer Tool → Instruments**를 열고 **Metal System Trace**를 선택합니다.
2. 출력된 PID의 Python을 대상으로 기록을 시작합니다. 터미널에서 Enter를 누르고 첫 구간이 끝나면 잠시 기다린 뒤 다시 Enter를 누릅니다.
3. 두 번째 구간 종료 후 기록을 멈춥니다. 중간 공백을 기준으로 양쪽 구간을 확대해 GPU 실행 길이와 명령 사이 공백을 비교합니다. 트랙 이름은 Xcode 버전에 따라 다를 수 있습니다.
4. `rmsnorm.trace`로 저장합니다. GPU 트랙이 비면 선택한 프로세스, 추적 템플릿과 기록 시작 시각을 확인하세요.

## 3. 재현 보고서 마무리

`report.md`에 칩, macOS, MLX 버전, 자료형, 열 수, 행 수를 먼저 적습니다. `timings.csv`에서 최대 오차와 속도 차이가 가장 큰 조건을 옮기고, trace에서 그 조건을 뒷받침하는 구간을 적습니다. 이 실험은 RMSNorm 하나의 실행 시간을 측정합니다. 실제 모델의 생성 속도 개선을 주장하려면 모델 내 연산을 교체한 뒤 동일 프롬프트로 별도 측정해야 합니다.

6단계에서는 행 최대값을 먼저 빼는 Softmax를 구현하고, 큰 양수 입력에서도 확률의 합이 1인지 검사합니다. 이어서 행렬 곱 커널을 작성하고 두 연산을 연결해 causal attention을 완성합니다. [Apple Metal 개발 도구](https://developer.apple.com/metal/tools/)

Source: https://bear2u.github.io/mac-mlx-study/projects/metal-kernels/05-profile/index.mdx
