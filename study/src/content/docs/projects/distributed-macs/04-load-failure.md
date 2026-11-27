---
title: "04 · 처리량 측정과 장애 복구 시험"
sidebar:
  order: 4
---

**목표** · 같은 질문 네 건을 한 대와 두 대에서 처리하고, 서버 하나가 중단됐을 때 새 요청이 어디로 가는지 관찰합니다.

## 1. 완료 요청 수와 토큰 수 재기

A에서 아래 코드를 `load.py`로 저장합니다. 2단계의 request.json과 같은 폴더에 둡니다.

```python
import asyncio
import json
import sys
from pathlib import Path
from time import perf_counter
import httpx

async def main(port):
    payload = json.loads(Path("request.json").read_text())
    async with httpx.AsyncClient(timeout=180, trust_env=False) as client:
        async def one():
            t0 = perf_counter()
            r = await client.post(f"http://127.0.0.1:{port}/v1/chat/completions",
                                  json=payload)
            r.raise_for_status()
            return (r.headers.get("x-worker", "직접"), perf_counter() - t0,
                    r.json()["usage"]["completion_tokens"])
        start = perf_counter()
        results = await asyncio.gather(*(one() for _ in range(4)), return_exceptions=True)
        seconds = perf_counter() - start
        done = [item for item in results if isinstance(item, tuple)]
        print(results)
        print("성공/전체", len(done), len(results), "요청/s", len(done) / seconds,
              "출력 토큰/s", sum(row[2] for row in done) / seconds)

asyncio.run(main(int(sys.argv[1])))
```

```sh
python load.py 8091
python load.py 8090
```

준비 실행 후 위 쌍을 세 번 반복합니다. 도착한 네 요청 전체의 경과 시간으로 나눈 값이 처리량입니다. 단일 요청의 생성 속도와 비교할 때는 단위를 구별하세요.

## 2. 중단과 복구 재현하기

1. B의 **추론 서버 터미널에서만** Ctrl+C를 누릅니다. SSH 터널과 라우터는 유지합니다.
2. A에서 `python load.py 8090`를 실행합니다. 새 요청 네 개가 모두 studio에서 완료되는지 확인합니다.
3. B에서 2단계의 서버 명령을 다시 실행하고 모델 조회가 성공할 때까지 기다립니다. 같은 부하에서 book 배정이 돌아오는지 확인합니다.
4. 요청 파일을 스트리밍용으로 복사하고 아래 명령을 실행합니다. 응답 헤더가 book일 때 B 서버를 중단해 보세요. 일부만 전송된 응답은 완료로 집계하지 말고, 새 요청의 배정을 확인합니다.

```sh
python -c 'import json; d=json.load(open("request.json")); d.update(stream=True,max_tokens=1024); d["messages"][0]["content"]="1부터 500까지 차례대로 각 숫자를 한 줄씩 적어줘. /no_think"; print(json.dumps(d))' > stream.json
curl -N -i -H 'Content-Type: application/json' --data-binary @stream.json http://127.0.0.1:8090/v1/chat/completions
```

정상 스트림은 끝까지 도착합니다. 중단된 스트림의 앞부분을 다른 서버가 이어서 재생성하면 중복 토큰이 생길 수 있어 라우터는 자동 재전송하지 않습니다. `request-id, worker, status, 복구 소요 초`를 기록합니다. 두 서버가 모두 꺼졌을 때는 503을 기대합니다. 시험을 마친 뒤 5단계의 모델 분할을 위해 양쪽 서버와 라우터를 Ctrl+C로 종료해 메모리를 확보하세요.
