---
title: "03 · 답을 보기 전에 채점 기준 정하기"
description: "모델이 계산과 한국어 정보 추출을 얼마나 잘하는지 비교할 작은 고정 시험지를 만듭니다."
sidebar:
  order: 3
---

모델이 계산과 한국어 정보 추출을 얼마나 잘하는지 비교할 작은 고정 시험지를 만듭니다.

## 정답이 분명한 문제 만들기

실습 폴더에서 아래 블록을 실행하세요. 각 줄은 문제 ID, 입력, 기대 출력이 든 JSON 객체입니다. 모델이 답을 설명하면 오답으로 처리하는 **완전 일치율**을 측정합니다. 정답 지식과 출력 형식 준수를 함께 재는 지표입니다.

```sh
cat > cases.jsonl <<'CASES'
{"id":"multiply","prompt":"6묶음에 연필이 4자루씩 있다. 모두 몇 자루인가? 숫자만 출력해.","answer":"24"}
{"id":"subtract","prompt":"창고에 38개가 있었고 9개를 꺼냈다. 남은 수량을 숫자만 출력해.","answer":"29"}
{"id":"label","prompt":"메모: 오후 담당은 민지, 오전 담당은 수진. 오전 담당 이름만 출력해.","answer":"수진"}
{"id":"code","prompt":"메모: 파랑팀은 K71, 초록팀은 M12. 초록팀 코드만 출력해.","answer":"M12"}
{"id":"weekday","prompt":"문서: 금요일에는 본관, 목요일에는 별관에서 모인다. 목요일 장소만 출력해.","answer":"별관"}
{"id":"sort","prompt":"숫자 7, 19, 3 중 가장 작은 값을 숫자만 출력해.","answer":"3"}
CASES
python - <<'PYCODE'
import json
from pathlib import Path
cases = [json.loads(s) for s in Path("cases.jsonl").read_text().splitlines()]
assert len({c["id"] for c in cases}) == len(cases)
assert all(c["prompt"] and c["answer"] for c in cases)
print(len(cases), "문제 준비 완료")
PYCODE
```

## 오답 판정 연습

정답이 24일 때 “24”와 “24자루입니다.”를 적어 보세요. 앞뒤 공백을 제거하면 전자만 일치합니다. 나중에 채점 결과를 읽을 때 후자는 **형식 오류**로 기록하면 지식 오류와 구분해 해석할 수 있습니다.

**확인** · 여섯 문제가 모두 읽히면 준비 완료입니다. 자신의 용도를 반영하려면 지금 예제 네 개를 더 작성하고, 모든 모델에 같은 파일을 사용하세요. 여섯 문제의 점수는 이 질문 묶음에서 관찰한 결과입니다. 

**막힐 때** · JSON 오류에 나온 행에서 큰따옴표와 쉼표를 확인하세요. 줄 하나에 객체 하나를 유지해야 다음 과의 평가기가 읽을 수 있습니다.
