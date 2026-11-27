---
title: "로컬 AI 벤치마크 플랫폼"
description: "같은 요청을 보냈을 때 첫 답이 가장 빠른 엔진과 여러 요청을 가장 빨리 끝내는 엔진이 같은지 살펴봅니다."
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 로컬 AI 벤치마크 플랫폼

**난이도 ★★☆☆☆** · 연계 강의 [3강](https://bear2u.github.io/mac-mlx-study/lesson-03/) · [5강](https://bear2u.github.io/mac-mlx-study/lesson-05/) · [9강](https://bear2u.github.io/mac-mlx-study/lesson-09/)

같은 요청을 보냈을 때 첫 답이 가장 빠른 엔진과 여러 요청을 가장 빨리 끝내는 엔진이 같은지 살펴봅니다.

## 만들 결과물

엔진별 지연 시간, 메모리, 처리량을 비교하는 웹 대시보드

## 단계별 튜토리얼

- [01 · 실험 폴더와 비교 조건 만들기](https://bear2u.github.io/mac-mlx-study/projects/benchmark/01-design/)
- [02 · 세 추론 서버를 같은 주소에서 실행하기](https://bear2u.github.io/mac-mlx-study/projects/benchmark/02-servers/)
- [03 · 스트림에서 첫 글자와 토큰 수 기록하기](https://bear2u.github.io/mac-mlx-study/projects/benchmark/03-stream/)
- [04 · 동시 요청과 메모리 측정기 구현하기](https://bear2u.github.io/mac-mlx-study/projects/benchmark/04-batch/)
- [05 · 세 엔진 실행과 원시 결과 검산](https://bear2u.github.io/mac-mlx-study/projects/benchmark/05-experiment/)
- [06 · 웹 대시보드로 결과 비교하기](https://bear2u.github.io/mac-mlx-study/projects/benchmark/06-dashboard/)

## 완료 기준

동일한 질문에 대한 세 엔진의 결과와 재현 명령을 대시보드에서 확인할 수 있습니다. 형식 또는 설정이 달랐던 비교에는 그 차이를 표시합니다.

Source: https://bear2u.github.io/mac-mlx-study/projects/benchmark/index.mdx
