---
title: "04 · 캐시 적중·무효화·복구 구현하기"
description: "요청이 들어올 때 키와 토큰 경계를 확인하고, 캐시가 없으면 새로 만듭니다. 각 질문은 독립된 상태에서 시작합니다."
sidebar:
  order: 4
---

요청이 들어올 때 키와 토큰 경계를 확인하고, 캐시가 없으면 새로 만듭니다. 각 질문은 독립된 상태에서 시작합니다.

## 요청 처리 함수

`serve_one.py`로 저장하세요. 캐시 파일을 매번 새로 로드하는 이유는 생성 과정이 받은 캐시를 수정하기 때문입니다. 메모리에 둔 한 객체를 여러 질문이 공유하면 이전 답변의 상태가 다음 질문에 섞일 수 있습니다.

```python
import sys
from pathlib import Path
from mlx_lm import load
from mlx_lm.models.cache import load_prompt_cache
from common import inputs, answer, spec
from store import prefix_for, location, build

def request(model, tok, doc, question):
    full = inputs(tok, doc, question)
    prefix = prefix_for(tok, doc)
    path = location(prefix)
    if len(full) <= len(prefix) or full[:len(prefix)] != prefix:
        return "경계 불일치", answer(model, tok, full)
    status = "적중" if path.exists() else "새로 생성"
    if not path.exists():
        build(model, prefix, path)
    state, meta = load_prompt_cache(str(path), return_metadata=True)
    if meta.get("key") != path.stem or meta.get("tokens") != str(len(prefix)):
        raise ValueError(f"캐시 메타데이터 불일치: {path}")
    result = answer(model, tok, full[len(prefix):], state)
    return status, result

if __name__ == "__main__":
    model, tok = load(spec["path"])
    doc = Path(sys.argv[1]).read_text()
    status, result = request(model, tok, doc, sys.argv[2])
    print(status, result["text"])
```

## 한 문장만 바꾸어 무효화 검사하기

```sh
python serve_one.py document.txt '1번 서랍의 종이 색은?'
python serve_one.py document.txt '120번 서랍에는 무엇이 있나?'
sed 's/파란/노란/' document.txt > changed.txt
python serve_one.py changed.txt '1번 서랍의 종이 색은?'
python serve_one.py changed.txt '1번 서랍의 종이 색은?'
```

**확인** · 3단계 캐시가 있는 초기 문서는 적중, 처음 본 수정본은 새로 생성, 같은 수정본을 한 번 더 보내면 적중이 기대됩니다. changed.txt의 답은 같은 수정본을 캐시 없이 실행한 답과도 대조하세요.

**막힐 때** · 경계 불일치가 나오면 전체 토큰 경로가 자동으로 답합니다. 메타데이터 불일치나 파일 읽기 오류가 나면 오류에 표시된 해당 파일을 실습 폴더 밖으로 옮기고 같은 질문을 보내 다시 생성하세요. [MLX-LM 캐시 로드 API](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/models/cache.py)
