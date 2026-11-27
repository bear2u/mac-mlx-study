---
title: "05 · 두 장비의 통신 경로 검증"
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 05 · 두 장비의 통신 경로 검증

**준비** · 두 대의 실제 맥, 같은 사설망에서 서로 접근 가능한 IP, 1단계에서 확인한 SSH 접속과 동일한 Python 절대 경로가 필요합니다. HTTP 서버와 SSH 포워딩은 여기서 사용하지 않습니다. MLX 프로세스 두 개가 직접 통신합니다.

## 1. 호스트 파일 준비하기

A의 실습 폴더에 `hosts.json`을 저장합니다. 아래 예시의 주소와 SSH 대상은 각각 **자기 장비의 실제 값**으로 바꿉니다. 시스템 설정 → 네트워크에서 현재 사용할 인터페이스의 IPv4 주소를 확인합니다. ssh 필드는 로그인 대상이고 ips는 두 맥 사이에서 데이터가 오갈 주소입니다.

```json
[
  {"ssh":"사용자A@studio.local","ips":["192.168.1.10"]},
  {"ssh":"사용자B@book.local","ips":["192.168.1.11"]}
]
```

## 2. 합이 3인지 확인하기

`collective.py`를 아래처럼 저장합니다. 각 장비의 프로세스 번호(rank)가 0 또는 1이고, 둘이 보낸 1과 2를 더하면 양쪽 모두 3을 받아야 합니다.

```python
import socket
import mlx.core as mx

group = mx.distributed.init()
assert group.size() == 2
value = mx.array(group.rank() + 1)
total = mx.distributed.all_sum(value, stream=mx.cpu)
print(socket.gethostname(), "rank", group.rank(), "sum", total.item(), flush=True)
assert total.item() == 3
```

A에서 다음을 실행합니다. BOOK_SSH는 1단계에서 사용한 실제 주소를 설정합니다. 같은 디렉터리에서 실행해야 원격 장비도 같은 작업 경로를 찾을 수 있습니다.

```sh
cd /Users/Shared/mac-inference-lab
source venv/bin/activate
scp collective.py "$BOOK_SSH":/Users/Shared/mac-inference-lab/
mlx.launch --backend ring --hostfile hosts.json --   /Users/Shared/mac-inference-lab/venv/bin/python /Users/Shared/mac-inference-lab/collective.py
```

서로 다른 호스트명이 한 줄씩 나타나고 두 줄 모두 sum 3이면 다음 단계로 진행합니다. 멈추면 Ctrl+C로 런처를 종료하고 양쪽의 주소·방화벽 연결 허용·패스워드 없는 SSH·파일 경로를 점검합니다. 같은 맥에서 실행한 두 프로세스는 두 장비 간 연결을 검증하지 못합니다. [MLX 호스트 파일과 ring 백엔드](https://github.com/ml-explore/mlx/blob/main/docs/src/usage/launching_distributed.rst)

Source: https://bear2u.github.io/mac-mlx-study/projects/distributed-macs/05-collective/index.mdx
