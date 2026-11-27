---
title: "여러 맥을 연결한 분산 AI 서버"
description: "맥 두 대에 요청을 나누는 방법과 두 대가 한 모델의 계산을 나누는 방법을 각각 실험합니다."
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 여러 맥을 연결한 분산 AI 서버

**난이도 ★★★★★** · 연계 강의 [8강](https://bear2u.github.io/mac-mlx-study/lesson-08/) · [9강](https://bear2u.github.io/mac-mlx-study/lesson-09/) · [12강](https://bear2u.github.io/mac-mlx-study/lesson-12/)

맥 두 대에 요청을 나누는 방법과 두 대가 한 모델의 계산을 나누는 방법을 각각 실험합니다.

## 만들 결과물

맥 스튜디오와 맥북으로 구성한 분산 서버 및 장애 복구 기록

## 단계별 튜토리얼

- [01 · 두 맥의 실습 환경 맞추기](https://bear2u.github.io/mac-mlx-study/projects/distributed-macs/01-nodes/)
- [02 · 같은 모델의 서버 두 개 띄우기](https://bear2u.github.io/mac-mlx-study/projects/distributed-macs/02-replicas/)
- [03 · 요청을 번갈아 배정하는 라우터 구현](https://bear2u.github.io/mac-mlx-study/projects/distributed-macs/03-router/)
- [04 · 처리량 측정과 장애 복구 시험](https://bear2u.github.io/mac-mlx-study/projects/distributed-macs/04-load-failure/)
- [05 · 두 장비의 통신 경로 검증](https://bear2u.github.io/mac-mlx-study/projects/distributed-macs/05-collective/)
- [06 · 모델 하나를 두 맥에 분할하고 비교](https://bear2u.github.io/mac-mlx-study/projects/distributed-macs/06-sharded/)

## 완료 기준

요청 분산과 모델 분할의 결과표를 각각 남깁니다. 어느 실험에서 처리량이 달라졌고 어느 실험에서 장비당 모델 메모리가 달라졌는지 설명합니다.

Source: https://bear2u.github.io/mac-mlx-study/projects/distributed-macs/index.mdx
