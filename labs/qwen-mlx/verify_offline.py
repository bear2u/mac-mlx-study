import errno
import socket
from pathlib import Path

from langchain_core.messages import HumanMessage
from core.rag_system import RAGSystem
from core.document_manager import DocumentManager

with socket.socket() as sock:
    sock.settimeout(3)
    assert sock.connect_ex(("1.1.1.1", 443)) == errno.EPERM, "네트워크 차단 정책을 확인하세요"

rag = RAGSystem()
rag.initialize()
documents = DocumentManager(rag)
if "solbit.md" not in documents.get_markdown_files():
    assert documents.add_documents([str(Path("example/solbit.md").resolve())]) == (1, 0)

question = "솔빛 관측소 파란 건조함의 반납 시각과 장소, 반납 확인 문구를 문서에서 찾아 한국어로 답해 주세요."
result = rag.agent_graph.invoke({"messages": [HumanMessage(content=question)]}, config=rag.get_config())
answer = result["messages"][-1].content
contexts = [ctx for item in result["agent_answers"] for ctx in item.get("contexts", [])]
print(answer)
assert any("solbit.md" in ctx and "달빛우표-483" in ctx for ctx in contexts), "검색 근거 확인 실패"
assert all(fact in answer for fact in ("동쪽 보관실", "달빛우표-483")), "장소 또는 확인 문구 누락"
assert "21시 10분" in answer or "21:10" in answer, "반납 시각 불일치"
print("검증 통과 · 외부 TCP 차단, 문서 검색, 답변 일치")
