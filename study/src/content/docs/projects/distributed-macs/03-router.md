---
title: "03 · 요청을 번갈아 배정하는 라우터 구현"
sidebar:
  order: 3
---

**만들 것** · 각 새 요청을 건강한 서버 하나에 전달하고 응답 헤더로 실제 선택을 알려 주는 HTTP 라우터. A의 실습 디렉터리에 아래를 `router.py`로 저장하세요. 비동기 클라이언트를 쓰므로 한 요청이 생성되는 동안 다른 요청도 접수할 수 있습니다.

```python
from itertools import count
from uuid import uuid4
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response, StreamingResponse

app = FastAPI()
nodes = [("studio", "http://127.0.0.1:8091"), ("book", "http://127.0.0.1:8092")]
turn = count()

@app.post("/v1/chat/completions")
async def route(request: Request):
    payload = await request.json()
    first = next(turn) % len(nodes)
    rid = uuid4().hex
    async with httpx.AsyncClient(timeout=2, trust_env=False) as probe:
        for offset in range(len(nodes)):
            name, base = nodes[(first + offset) % len(nodes)]
            try:
                status = await probe.get(base + "/v1/models")
                status.raise_for_status()
                break
            except httpx.HTTPError:
                continue
        else:
            raise HTTPException(503, "사용 가능한 추론 서버가 없습니다")

    client = httpx.AsyncClient(timeout=180, trust_env=False)
    try:
        upstream = await client.send(
            client.build_request("POST", base + "/v1/chat/completions", json=payload),
            stream=True,
        )
    except httpx.HTTPError as error:
        await client.aclose()
        raise HTTPException(502, f"{name} 연결 실패") from error
    headers = {"X-Worker": name, "X-Request-ID": rid}
    print(rid, name, upstream.status_code, flush=True)
    try:
        if payload.get("stream") and upstream.is_success:
            async def chunks():
                try:
                    async for part in upstream.aiter_bytes():
                        yield part
                finally:
                    await upstream.aclose()
                    await client.aclose()
            return StreamingResponse(chunks(), media_type="text/event-stream", headers=headers)
        body = await upstream.aread()
        return Response(body, status_code=upstream.status_code,
                        media_type="application/json", headers=headers)
    finally:
        if not (payload.get("stream") and upstream.is_success):
            await upstream.aclose()
            await client.aclose()
```

## 실행하고 배정 확인하기

A의 가상환경에서 `python -m uvicorn router:app --host 127.0.0.1 --port 8090`으로 실행합니다. 새 터미널에서 실습 디렉터리로 이동한 뒤 아래 요청을 네 번 보냅니다.

```sh
for n in 1 2 3 4; do
  curl -fsS -D - -o /dev/null -H 'Content-Type: application/json'     --data-binary @request.json http://127.0.0.1:8090/v1/chat/completions
done
```

헤더의 x-worker가 studio와 book을 번갈아 가리키고 x-request-id가 요청마다 달라지는지 확인합니다. 한 이름만 나오면 양쪽 서버의 모델 조회를 다시 수행하세요. 이 라우터는 매 요청마다 상태 조회 한 번을 추가하므로 다음 실험에는 이 비용도 포함됩니다.
