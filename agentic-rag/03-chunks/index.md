---
title: "03 · 부모와 자식 청크 해부하기"
description: "한 파일에서 검색용 조각과 문맥 복원용 조각이 어떻게 연결되는지 관찰합니다."
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 03 · 부모와 자식 청크 해부하기

검색은 짧은 문장에 집중할수록 원하는 대목을 찾기 쉽습니다. 반면 “당일”이 무엇을 뜻하는지 이해하려면 주변 문장이 필요합니다. 원본은 Markdown 제목을 기준으로 큰 **부모**를 만들고 이를 작은 **자식**으로 나눕니다. 자식에는 어느 부모에서 왔는지 알려 주는 parent_id가 남습니다.

## 같은 입력으로 색인 직전 살펴보기

두 번째 터미널에서 저장소 루트로 이동해 실행하세요. 이 코드는 파일을 읽고 메모리에서 나누므로 열린 앱의 데이터베이스와 충돌하지 않습니다.

```sh
cd ~/mac-inference-lab/agentic-rag-for-dummies
PYTHONPATH=project uv run --locked python - <<'PYCODE'
from pathlib import Path
from document_chunker import DocumentChunker

path = Path("lab-input/solbit.md")
parents, children = DocumentChunker().create_chunks_single(path, source_name=path.name)
ids = {key for key, doc in parents}
assert children and all(c.metadata["parent_id"] in ids for c in children)
for key, doc in parents:
    print("부모", key, len(doc.page_content))
for child in children:
    print("자식", child.metadata["parent_id"], len(child.page_content), child.page_content[:45])
PYCODE
```

짧은 예제에서는 제목이 둘이어도 부모와 자식이 각각 하나일 수 있습니다. 기본 설정은 짧은 제목 섹션을 합칩니다. 자식 크기 500과 겹침 100의 단위는 이 분할기의 **문자**입니다.

## 길이만 바꾸는 실험

스크립트의 path를 만들기 전에 아래 코드를 넣고 입력을 lab-input/long.md로 바꾸세요. 실험 파일은 앱에 업로드하지 않아도 됩니다.

```python
original = Path("lab-input/solbit.md").read_text()
Path("lab-input/long.md").write_text("\n\n".join(original for _ in range(20)))
```

기준 버전에서 예제 원문은 부모 1개·자식 1개, 20회 반복한 원문은 부모 1개·자식 10개가 나왔습니다. 원문을 편집했다면 수치가 달라질 수 있습니다.

**통과 기준** · 긴 입력에서 자식 수가 늘어났는지 세고, 서로 다른 자식 둘이 가리키는 부모 ID를 찾아 적습니다. 앱이 만든 실제 부모 파일은 parent_store 폴더에서 확인할 수 있습니다.

[이 단계의 원본 코드](https://github.com/GiovanniPasq/agentic-rag-for-dummies/blob/c1b339b54f0927bd0b469fcce70f3cd5de4e918d/project/document_chunker.py)

Source: https://bear2u.github.io/mac-mlx-study/agentic-rag/03-chunks/index.mdx
