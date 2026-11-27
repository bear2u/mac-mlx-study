---
title: "05 · llama.cpp로 기준값 만들기"
description: "다른 추론 엔진에서 같은 작업을 어떻게 비교할까?"
---

> Documentation Index
> Fetch the complete documentation index at: https://bear2u.github.io/mac-mlx-study/llms.txt
> Use this file to discover all available pages before exploring further.

# 05 · llama.cpp로 기준값 만들기

**다른 추론 엔진에서 같은 작업을 어떻게 비교할까?**

llama.cpp의 llama-bench는 입력 처리(pp)와 토큰 생성(tg)을 분리해 측정합니다. 같은 4비트라도 GGUF와 MLX 가중치의 표현 방식이 달라 측정값에는 엔진과 파일 형식의 영향이 함께 들어갑니다.

## 직접 해보기

Homebrew로 도구를 설치하고 Qwen2.5-7B-Instruct의 GGUF 파일 중 Q4_K_M판을 준비하세요. 아래 경로를 내려받은 실제 파일 경로로 바꿉니다.

```sh
brew install llama.cpp
llama-bench -m "/실제/경로/model.gguf" -p 512 -n 128 -r 3
```

결과의 pp512와 tg128 행을 읽습니다. 3과의 MLX 결과 옆에 실제 입력 길이와 측정 방식도 표시하세요. [GGUF 모델 파일](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/tree/main)

## 실험 노트

엔진 버전, 모델 파일명, 출력의 backend, pp와 tg 속도를 적습니다. 비교 조건 중 일치한 항목과 차이가 남은 항목을 각각 한 가지 설명하세요.

[공식 참고 자료](https://github.com/ggml-org/llama.cpp/tree/master/tools/llama-bench)

Source: https://bear2u.github.io/mac-mlx-study/lesson-05/index.mdx
