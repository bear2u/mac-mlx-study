---
title: "06 · 검색 실패와 답변 실패를 나눠 평가하기"
description: "작은 채점 세트로 근거 검색과 최종 답변의 오류 위치를 구분합니다."
sidebar:
  order: 6
---

첫 답변 하나가 맞아도 다른 장비의 시간을 섞거나 문서에 없는 사실을 만들어 낼 수 있습니다. 같은 매뉴얼로 아래 네 문제를 평가하세요. 각 문제를 새 대화에서 시작하면 이전 답의 영향도 줄일 수 있습니다.

| 질문 | 기대하는 근거 또는 행동 |
| --- | --- |
| 파란 건조함은 언제 어디로 반납하나? | 관측 당일 21시 10분, 동쪽 보관실 |
| 은색 기록계는 언제 어디로 반납하나? | 다음 날 08시 40분, 서쪽 보관실 |
| 두 장비의 대여 코드를 장비별로 알려줘. | 건조함 자두-17, 기록계 모래-32 |
| 건조함 대여 비용은 얼마인가? | 비용 정보가 없다고 답함 |

## 채점표 작성

실습 폴더에 results.tsv를 만들고 각 답변을 확인한 뒤 값을 채웁니다. 첫 세 문제에는 필요한 근거가 검색 결과에 모두 있으면 evidence에 1, 최종 답의 사실이 모두 맞으면 correct에 1을 기록합니다. 마지막 문제는 evidence를 비우고 근거 없는 금액을 지어내지 않았으면 correct에 1을 기록합니다.

```sh
printf 'id\tevidence\tcorrect\n1\t\t\n2\t\t\n3\t\t\n4\t\t\n' > results.tsv
```

편집 후 아래 코드를 실행합니다. 정답인 질문만 골라서 보고하지 않도록 네 줄이 모두 있는지도 검사합니다.

```sh
uv run --locked python - <<'PYCODE'
import csv
with open("results.tsv") as f:
    rows = list(csv.DictReader(f, delimiter="\t"))
assert [r["id"] for r in rows] == ["1", "2", "3", "4"]
assert all(r["correct"] in ("0", "1") for r in rows)
assert all(r["evidence"] in ("0", "1") for r in rows[:3])
print("근거 발견", sum(int(r["evidence"]) for r in rows[:3]), "/ 3")
print("최종 답 정답", sum(int(r["correct"]) for r in rows), "/ 4")
PYCODE
```

## 한 번 더 개선하기

근거가 빠졌다면 4단계의 검색어를 먼저 바꾸고, 근거는 있는데 답이 틀렸다면 5단계의 질문 재작성과 최종 집계를 확인하세요. 변수 하나를 바꾼 뒤 동일한 질문으로 재측정합니다. 원본의 evaluation.ipynb는 RAGAS로 도구 출력과 답변을 평가하는 심화 자료입니다. 이 강의에서 만든 문서와 질문에 적용하려면 평가 데이터도 교체해야 합니다.

**완료 기준** · 한 질문을 골라 어떤 도구가 어느 문서를 찾아냈는지, 최종 답이 그 근거와 일치하는지를 재현할 수 있습니다. 오답이라면 처음 틀어진 단계와 다음 실험에서 바꿀 조건을 하나씩 적습니다.

[이 단계의 원본 코드](https://github.com/GiovanniPasq/agentic-rag-for-dummies/blob/c1b339b54f0927bd0b469fcce70f3cd5de4e918d/notebooks/evaluation.ipynb)
