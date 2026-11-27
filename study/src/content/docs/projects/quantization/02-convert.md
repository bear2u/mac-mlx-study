---
title: "02 · 4비트와 8비트 직접 변환하기"
description: "같은 원본에서 두 개의 모델 폴더를 만들고 실제로 어떤 정밀도가 기록됐는지 검사합니다."
sidebar:
  order: 2
---

같은 원본에서 두 개의 모델 폴더를 만들고 실제로 어떤 정밀도가 기록됐는지 검사합니다.

## 먼저 바꿀 조건 정하기

Affine 양자화는 한 그룹의 가중치에 스케일과 편향을 함께 저장합니다. 그룹 크기까지 바꾸면 비트 수의 효과를 해석하기 어렵습니다. 여기서는 그룹 크기를 64로 고정합니다. 양자화하지 않는 층, 스케일, 토크나이저 때문에 파일 크기의 비율은 정확히 1 대 2가 아닐 수 있습니다.

```sh
cd ~/mac-inference-lab/quantization
source .venv/bin/activate
SOURCE=$(python -c 'import json; print(json.load(open("source.json"))["path"])')
mlx_lm.convert --help
mkdir -p models
for bits in 4 8; do
  mlx_lm.convert --hf-path "$SOURCE" --mlx-path "models/q$bits" -q --q-bits "$bits" --q-group-size 64 --q-mode affine || break
done
```

## 변환이 끝났는지 검사하기

```sh
python - <<'PYCODE'
from pathlib import Path
import json
for bits in (4, 8):
    path = Path(f"models/q{bits}")
    cfg = json.loads((path / "config.json").read_text())
    quant = cfg["quantization"]
    assert quant["bits"] == bits and quant["group_size"] == 64, quant
    weights = list(path.glob("*.safetensors"))
    assert weights
    print(path, sum(p.stat().st_size for p in weights) / 1e6, "MB", quant["bits"], "bit")
PYCODE
```

**확인** · 두 줄에 각각 4와 8이 표시되어야 합니다. MB는 디스크에 저장된 가중치의 크기입니다. 실행 중 메모리는 다음 과에서 따로 잽니다.

**2·3비트 확장** · MLX와 모델이 해당 비트 수의 affine 연산을 지원하면 같은 명령의 bits 값을 2 또는 3으로 바꾸어 별도 폴더로 변환하세요. 생성까지 성공한 조건만 결과표에 추가합니다. 특정 레이어 모양에 맞지 않는다는 오류가 나면 레이어 이름·비트 수·그룹 크기를 기록하고 기본 4·8비트 실험을 계속합니다. [MLX-LM 변환 옵션](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/convert.py)
