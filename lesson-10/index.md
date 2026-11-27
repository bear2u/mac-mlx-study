---
title: "10 · Instruments로 병목 찾기"
description: "첫 답이 늦는 동안 GPU는 무엇을 하고 있을까?"
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 10 · Instruments로 병목 찾기

**첫 답이 늦는 동안 GPU는 무엇을 하고 있을까?**

전체 응답 시간에는 토큰화, GPU 작업 제출, GPU 연산, 네트워크 전송이 모두 들어갑니다. 시간축을 보면 GPU가 일한 구간과 다음 작업을 기다린 구간을 구분할 수 있습니다.

## 직접 해보기

Xcode의 Open Developer Tool 메뉴에서 Instruments를 엽니다. Metal System Trace 템플릿을 선택하고 8과 서버 프로세스를 대상으로 기록을 시작합니다. 짧은 질문 하나와 긴 문서를 붙인 질문 하나를 순서대로 보낸 뒤 기록을 종료하세요.

두 요청 각각에서 GPU 작업이 시작한 시점과 작업 사이의 빈 구간을 확대하세요. 빈 구간이 보이면 같은 구간의 CPU 스레드 활동과 대조합니다.

## 실험 노트

긴 입력에서 늘어난 구간에 표시를 남기고 가능한 원인 하나를 적습니다. 가설을 확인하기 위해 다음 실행에서 바꿀 조건도 한 가지 정하세요.

[공식 참고 자료](https://developer.apple.com/metal/tools/)

Source: https://bear2u.github.io/mac-mlx-study/lesson-10/index.mdx
