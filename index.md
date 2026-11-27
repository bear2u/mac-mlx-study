---
title: "맥 AI 추론 실습실"
description: "한 대의 맥으로 모델 실행부터 GPU 성능 분석까지 공부하는 한국어 실습 과정"
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 맥 AI 추론 실습실

맥에서 첫 답변을 생성한 뒤, 문서가 길어지거나 여러 사람이 동시에 질문할 때 무엇이 달라지는지 측정합니다. 한 과를 마칠 때마다 실험 노트에 결과와 이유를 한 줄씩 남기세요.

**준비물** · Apple Silicon 맥, Python 3, 터미널, 모델을 내려받을 인터넷 연결. 후반 GPU 분석 실습에는 Xcode를 사용합니다.

[01 · 첫 모델 실행부터 시작하기](https://bear2u.github.io/mac-mlx-study/lesson-01/) · [프로젝트 실습 목차](https://bear2u.github.io/mac-mlx-study/projects/)

## 기초 · 모델 한 개 이해하기

- [01 · 맥에서 첫 모델 실행하기](https://bear2u.github.io/mac-mlx-study/lesson-01/) — 내 맥은 어떤 조건에서 첫 답을 생성했을까?
- [02 · 다음 토큰이 정해지는 과정](https://bear2u.github.io/mac-mlx-study/lesson-02/) — 모델이 문장을 어디에서 끊어 읽을까?
- [03 · 입력 처리와 답변 생성 측정하기](https://bear2u.github.io/mac-mlx-study/lesson-03/) — 긴 문서를 넣으면 어느 구간이 길어질까?
- [04 · 4비트와 8비트 비교하기](https://bear2u.github.io/mac-mlx-study/lesson-04/) — 메모리를 줄이면 내 과제의 정답률은 얼마나 달라질까?

## 측정 · 엔진과 캐시 비교하기

- [05 · llama.cpp로 기준값 만들기](https://bear2u.github.io/mac-mlx-study/lesson-05/) — 다른 추론 엔진에서 같은 작업을 어떻게 비교할까?
- [06 · KV 캐시의 메모리 비용](https://bear2u.github.io/mac-mlx-study/lesson-06/) — 대화가 길어지면 어떤 데이터가 쌓일까?
- [07 · 공통 문서의 캐시 재사용하기](https://bear2u.github.io/mac-mlx-study/lesson-07/) — 같은 문서를 두 번 읽는 비용을 줄일 수 있을까?
- [08 · 로컬 스트리밍 API와 첫 토큰](https://bear2u.github.io/mac-mlx-study/lesson-08/) — 사용자가 실제로 느끼는 대기 시간은 얼마일까?

## 최적화 · 추론 서버 분석하기

- [09 · 여러 요청을 동시에 보내기](https://bear2u.github.io/mac-mlx-study/lesson-09/) — 동시 사용자가 늘면 누가 더 오래 기다릴까?
- [10 · Instruments로 병목 찾기](https://bear2u.github.io/mac-mlx-study/lesson-10/) — 첫 답이 늦는 동안 GPU는 무엇을 하고 있을까?
- [11 · RMSNorm 연산의 정확도와 속도](https://bear2u.github.io/mac-mlx-study/lesson-11/) — 작은 연산을 바꾸었을 때 같은 결과를 더 빨리 얻을까?
- [12 · 내 맥의 추론 실험 보고서](https://bear2u.github.io/mac-mlx-study/lesson-12/) — 내가 쓰는 작업에 가장 적합한 설정은 무엇일까?

Source: https://bear2u.github.io/mac-mlx-study/index.mdx
