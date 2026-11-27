---
title: "개인용 AI 추론 클라우드"
description: "맥 스튜디오 한 대에서 사용자별로 요청을 받고 모델을 선택하는 추론 서비스를 만듭니다."
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 개인용 AI 추론 클라우드

**난이도 ★★★☆☆** · 연계 강의 [8강](https://bear2u.github.io/mac-mlx-study/lesson-08/) · [9강](https://bear2u.github.io/mac-mlx-study/lesson-09/)

맥 스튜디오 한 대에서 사용자별로 요청을 받고 모델을 선택하는 추론 서비스를 만듭니다.

## 만들 결과물

API 키 발급, 모델 선택, 대기열, 스트리밍, 사용량 기록을 갖춘 서버

## 단계별 튜토리얼

- [01 · 실습 폴더와 서버 배치 준비](https://bear2u.github.io/mac-mlx-study/projects/inference-cloud/01-workspace/)
- [02 · 예측 가능한 모델 응답 만들기](https://bear2u.github.io/mac-mlx-study/projects/inference-cloud/02-engine/)
- [03 · API 키 발급과 사용 기록 저장소](https://bear2u.github.io/mac-mlx-study/projects/inference-cloud/03-keys/)
- [04 · 동시 실행 한도와 대기열 구현](https://bear2u.github.io/mac-mlx-study/projects/inference-cloud/04-queue/)
- [05 · 모델 선택과 스트리밍 중계 연결](https://bear2u.github.io/mac-mlx-study/projects/inference-cloud/05-gateway/)
- [06 · 두 사용자로 정상·혼잡·취소 검사](https://bear2u.github.io/mac-mlx-study/projects/inference-cloud/06-acceptance/)
- [07 · 실제 MLX 모델 연결과 최종 인수 실험](https://bear2u.github.io/mac-mlx-study/projects/inference-cloud/07-real-models/)

## 완료 기준

두 사용자가 모델을 골라 스트리밍 답변을 받고 각자의 사용량을 확인할 수 있습니다. 유효하지 않은 키와 대기열이 가득 찬 경우도 테스트합니다.

Source: https://bear2u.github.io/mac-mlx-study/projects/inference-cloud/index.mdx
