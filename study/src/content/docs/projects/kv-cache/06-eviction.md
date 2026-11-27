---
title: "06 · 디스크 한도와 오래된 캐시 정리하기"
description: "최근 사용 시각을 갱신하고 한도를 넘으면 가장 오래 사용하지 않은 전용 캐시 파일부터 정리합니다."
sidebar:
  order: 6
---

문서를 하나씩 바꾸면서 실험하면 예전 캐시도 디스크에 남습니다. 이 단계에서는 파일 읽기와 쓰기를 한 요청씩 실행하는 로컬 실험에 맞춰, 캐시를 다 쓴 뒤 합계 용량을 검사합니다. 최근에 요청된 캐시는 파일 수정 시각을 갱신합니다.

## 전용 파일만 다루는 정리 함수

아래 코드를 프로젝트 폴더의 `budget.py`로 저장하세요. 3단계에서 정한 파일명인 **64자리 소문자 16진수와 .safetensors 확장자**를 확인합니다. 임시 파일, 모델 가중치, 하위 디렉터리는 대상에서 제외합니다. 한도는 바이트 기준이며 0은 사용 후 전용 캐시를 하나도 남기지 않는 설정입니다.

```python
from pathlib import Path
import re

KEY_FILE = re.compile(r"[0-9a-f]{64}\.safetensors")

def enforce_budget(directory, limit_bytes):
    if limit_bytes < 0:
        raise ValueError("캐시 한도는 0 이상이어야 합니다")
    files = []
    for path in Path(directory).iterdir():
        if path.is_symlink() or not KEY_FILE.fullmatch(path.name) or not path.is_file():
            continue
        info = path.stat()
        files.append((info.st_mtime_ns, path.name, info.st_size, path))
    total = sum(size for _, _, size, _ in files)
    removed = []
    for _, _, size, path in sorted(files):
        if total <= limit_bytes:
            break
        path.unlink()
        total -= size
        removed.append(path.name)
    return total, removed
```

## 가짜 파일로 삭제 순서 확인

실제 캐시를 건드리기 전에 아래 내용을 `test_budget.py`로 저장하고 `python test_budget.py`를 실행하세요. 이름이 형식에 맞지 않는 가중치 파일과 임시 파일이 그대로 남는지도 검사합니다.

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import os
from budget import enforce_budget

with TemporaryDirectory() as temp:
    root = Path(temp)
    old = root / ("a" * 64 + ".safetensors")
    new = root / ("b" * 64 + ".safetensors")
    untouched = root / "model.safetensors"
    staged = root / ".working.safetensors"
    for file in (old, new, untouched, staged):
        file.write_bytes(b"12345678")
    os.utime(old, (1, 1))
    os.utime(new, (2, 2))
    assert enforce_budget(root, 16) == (16, [])
    assert enforce_budget(root, 8) == (8, [old.name])
    assert new.exists() and untouched.exists() and staged.exists()
    assert enforce_budget(root, 0) == (0, [new.name])
print("용량 경계와 정리 순서 통과")
```

## 요청 처리에 연결

4단계의 `serve_one.py` 상단에 `import os`와 `from budget import enforce_budget`을 추가하세요. request 함수의 마지막 `return status, result` 바로 앞에 다음 세 줄을 같은 들여쓰기로 넣습니다. 추론에 성공한 요청마다 마지막 사용 시각이 바뀌고 디스크 사용량이 한도 이내로 돌아옵니다. 무효 입력을 피하기 위해 환경변수는 0 이상의 정수로 지정하세요.

```python
    path.touch()
    limit = int(os.environ.get("KV_LIMIT_BYTES", str(512 * 1024**2)))
    enforce_budget(path.parent, limit)
```

## 한도 초과와 재생성 검증

다음 명령은 **현재 실습 폴더 cache 안에서** 한도를 0으로 설정해 이전 단계의 전용 캐시를 지웁니다. 5단계의 측정 보고서 results/times.json을 먼저 저장하세요. 다른 실험 파일을 보관하는 폴더와 분리한 상태에서 진행합니다.

```sh
python test_budget.py
KV_LIMIT_BYTES=0 python serve_one.py document.txt '1번 서랍의 종이 색은?'
KV_LIMIT_BYTES=0 python serve_one.py document.txt '1번 서랍의 종이 색은?'
python serve_one.py document.txt '1번 서랍의 종이 색은?'
python serve_one.py document.txt '1번 서랍의 종이 색은?'
```

**확인** · 두 번째 호출에서는 “새로 생성”이 표시되고 처리 후 파일이 정리됩니다. 세 번째 호출은 기본 한도로 캐시를 만들고, 파일이 기본 한도 안에 들어가면 네 번째 호출에서 “적중”이 표시됩니다. 파일 하나가 한도보다 큰 경우에는 그 파일도 정리돼 다음 요청이 다시 생성 비용을 냅니다.

**기록할 결론** · 캐시 하나의 크기, 현재 한도, 반복할 문서 수를 함께 적으세요. 자주 쓰는 문서 두 개도 담을 수 없는 한도를 선택했다면 5단계의 적중 TTFT가 실제 요청에서 얼마나 자주 실현될지 다시 따져 봅니다. 여러 프로세스가 같은 캐시를 정리하도록 확장할 때는 조회·갱신·삭제 사이에 파일이 사라지는 경우까지 별도로 다뤄야 합니다.
