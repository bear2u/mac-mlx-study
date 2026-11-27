---
title: "04 · 동시 실행 한도와 대기열 구현"
description: "한 요청을 실행하고 두 요청까지 기다리게 합니다."
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 04 · 동시 실행 한도와 대기열 구현

동시에 처리할 수 있는 요청이 하나일 때 네 사람이 거의 동시에 질문한다고 가정하세요. 첫 요청이 GPU를 사용하고 다음 두 요청은 대기합니다. 네 번째 요청에는 즉시 429를 반환합니다. 오래 대기한 요청은 빠져나갈 수 있어야 합니다.

## gate.py 저장하기

```python
import asyncio
from time import monotonic

class Full(Exception):
    pass

class Gate:
    def __init__(self, running=1, waiting=2, timeout=30):
        self.slots = asyncio.Semaphore(running)
        self.capacity = running + waiting
        self.present = 0
        self.timeout = timeout

    async def enter(self):
        if self.present >= self.capacity:
            raise Full()
        # 같은 이벤트 루프 안에서 검사와 증가 사이에는 await가 없다.
        self.present += 1
        start = monotonic()
        try:
            await asyncio.wait_for(self.slots.acquire(), timeout=self.timeout)
        except BaseException:
            self.present -= 1
            raise
        return round((monotonic() - start) * 1000)

    def leave(self):
        self.slots.release()
        self.present -= 1
```

## 모델 없이 경계 확인하기

```sh
python - <<'PYTEST'
import asyncio
from gate import Gate, Full

async def test():
    g = Gate(running=1, waiting=1, timeout=1)
    await g.enter()
    waiter = asyncio.create_task(g.enter())
    await asyncio.sleep(0)
    try:
        await g.enter()
    except Full:
        print("세 번째 요청 거절")
    g.leave()
    print("두 번째 요청 진입, 대기 ms =", await waiter)
    g.leave()
    assert g.present == 0
asyncio.run(test())
PYTEST
```

마지막 값이 0이면 입장한 두 요청의 자리가 모두 반환됐습니다. `timeout`을 작게 하고 첫 작업을 오래 붙들면 대기 시간 초과 경로도 실험할 수 있습니다. 이 게이트는 한 프로세스의 메모리를 쓰므로 뒤에서 Uvicorn을 워커 하나로 실행합니다.

Source: https://bear2u.github.io/mac-mlx-study/projects/inference-cloud/04-queue/index.mdx
