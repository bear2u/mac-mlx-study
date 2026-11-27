---
title: "12 · 내 맥의 추론 실험 보고서"
description: "내가 쓰는 작업에 가장 적합한 설정은 무엇일까?"
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 12 · 내 맥의 추론 실험 보고서

**내가 쓰는 작업에 가장 적합한 설정은 무엇일까?**

긴 문서에 반복해서 질문하는 사람과 여러 사용자의 짧은 질문을 처리하는 서버는 서로 다른 목표를 가집니다. 사용 장면을 먼저 정하면 어떤 지표를 개선해야 하는지 결정할 수 있습니다.

## 직접 해보기

1. “긴 한국어 문서에 연속으로 질문하기”처럼 한 가지 사용 장면을 고릅니다.
2. 기준 설정을 고정하고 캐시 사용 여부나 양자화 비트 수 중 하나만 바꿉니다.
3. 동일한 입력과 출력 상한으로 조건마다 세 번 측정합니다. 답변이 요구한 사실을 포함하는지도 채점하세요.
4. 아래 표에 중앙값을 적고 재현 명령과 실제 모델 버전을 덧붙입니다.

| 조건 | TTFT(초) | 생성 속도(토큰/초) | 최대 메모리(GB) | 정답 수 |
| --- | --- | --- | --- | --- |
| 기준 설정 | | | | |
| 변경 설정 | | | | |

첨부 글에 나온 27B 모델의 초당 50.6토큰을 재현해 보고 싶다면 모델 ID, 양자화, 칩, 입력 길이를 먼저 확인하세요.

## 실험 노트

“이 작업에서는 ___ 설정을 선택했다. ___가 개선됐고 ___의 비용이 들었다.”를 측정값으로 완성합니다. 다음 실험은 아직 설명되지 않은 결과 한 가지에서 시작하세요.

[공식 참고 자료](https://github.com/ggml-org/llama.cpp/tree/master/tools/llama-bench)

Source: https://bear2u.github.io/mac-mlx-study/lesson-12/index.mdx
