---
title: "09 · 여러 요청을 동시에 보내기"
description: "동시 사용자가 늘면 누가 더 오래 기다릴까?"
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 09 · 여러 요청을 동시에 보내기

**동시 사용자가 늘면 누가 더 오래 기다릴까?**

서버는 도착한 요청을 기다리게 하거나 함께 처리할 수 있습니다. 연속 배칭은 먼저 끝난 요청의 자리에 새 요청을 넣어 연산 자원을 활용합니다. 처리량과 개별 요청의 지연은 따로 측정합니다.

## 직접 해보기

8과의 서버를 켜 두고 실습 폴더에서 아래 명령을 실행합니다. 각 조건은 같은 요청 네 개를 처리하고 동시에 실행하는 개수만 바꿉니다.

```sh
for parallel in 1 2 4; do
  time (seq 4 | xargs -P "$parallel" -I '{}' python client.py)
done
```

각 조건을 세 번 반복하세요. 서버가 요청을 실제로 묶는지 확인하려면 서버 로그를 살펴봅니다. 후속 실험으로 vLLM-Metal의 지원 모델과 설치 조건을 확인한 뒤 같은 API 요청을 보내 보세요.

## 실험 노트

4 ÷ 전체 벽시계 시간으로 초당 완료 요청 수를 구하고 가장 오래 기다린 요청의 TTFT도 적습니다. 에러가 나면 성공한 요청 수만 셉니다.

[공식 참고 자료](https://github.com/vllm-project/vllm-metal)

Source: https://bear2u.github.io/mac-mlx-study/lesson-09/index.mdx
