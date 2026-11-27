---
title: "04 · 모델 없이 검색 근거 추적하기"
description: "하이브리드 검색이 반환한 문장과 부모 원문을 직접 비교합니다."
sidebar:
  order: 4
---

Qdrant는 문장의 의미를 나타내는 밀집 벡터와 단어 단서를 담은 희소 벡터를 함께 사용합니다. ‘자두-17’처럼 고유한 코드가 있는 질문과 ‘언제 돌려줘?’처럼 표현이 바뀌는 질문에서 어떤 근거가 나오는지 확인해 봅니다. 이 단계는 채팅 모델을 호출하지 않지만 검색용 임베딩 모델은 사용합니다.

## 도구를 독립적으로 호출하기

앱 터미널에서 Ctrl+C로 Gradio를 종료하세요. 이 프로젝트는 로컬 디스크의 Qdrant를 사용하므로 같은 저장소를 열어 두 프로세스가 동시에 접근하면 잠금 오류가 날 수 있습니다. 아래 파일을 저장소 루트의 inspect_search.py로 저장합니다.

```python
import sys
import config
from db.vector_db_manager import VectorDbManager
from rag_agent.tools import ToolFactory

db = VectorDbManager()
collection = db.get_collection(config.CHILD_COLLECTION)
tools = {t.name: t for t in ToolFactory(collection).create_tools()}
query = sys.argv[1]
hits = tools["search_child_chunks"].invoke({"query": query, "limit": 3})
print(hits)
for line in hits.splitlines():
    if line.startswith("Parent ID: "):
        key = line.partition(": ")[2]
        print(tools["retrieve_parent_chunks"].invoke({"parent_id": key}))
        break
```

```sh
PYTHONPATH=project uv run --locked python inspect_search.py '자두-17'
PYTHONPATH=project uv run --locked python inspect_search.py '파란 장비를 언제 돌려줘?'
```

**기록할 것** · 각 결과의 파일 이름, parent_id, 반환 시각이 들어 있는 문장을 적습니다. NO_RELEVANT_CHUNKS는 문턱을 넘은 결과가 없다는 뜻입니다. RETRIEVAL_ERROR는 실행 오류이므로 같은 결과로 세지 마세요. 결과가 없으면 Documents에 파일이 등록됐는지부터 확인합니다. 부모를 읽은 뒤에도 답을 찾을 수 없다면 생성 모델을 바꾸기 전에 원문부터 다시 봅니다.

[이 단계의 원본 코드](https://github.com/GiovanniPasq/agentic-rag-for-dummies/blob/c1b339b54f0927bd0b469fcce70f3cd5de4e918d/project/rag_agent/tools.py)
