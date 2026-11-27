---
title: "07 · 공통 문서의 캐시 재사용하기"
description: "같은 문서를 두 번 읽는 비용을 줄일 수 있을까?"
sidebar:
  order: 7
---

**같은 문서를 두 번 읽는 비용을 줄일 수 있을까?**

서로 다른 질문이 같은 토큰 열로 시작하면 공통 앞부분의 계산 결과를 저장해 다음 요청에 이용할 수 있습니다. 캐시 파일을 만드는 비용과 이후 질문에서 아끼는 비용을 따로 봅니다.

## 직접 해보기

실습 폴더에 긴 문서의 일반 텍스트를 document.txt로 저장하세요. 같은 모델과 원문을 사용합니다.

```sh
cat document.txt | mlx_lm.cache_prompt --model "$MODEL" --prompt - --prompt-cache-file doc-cache.safetensors
mlx_lm.generate --prompt-cache-file doc-cache.safetensors --prompt "문서의 주제를 한 줄로 알려줘." --max-tokens 64
mlx_lm.generate --prompt-cache-file doc-cache.safetensors --prompt "핵심 용어 세 개를 뽑아줘." --max-tokens 64
```

캐시 없이 문서와 각 질문을 함께 입력한 경우와 비교하세요. 채팅 템플릿 및 특수 토큰 처리도 기록합니다.

## 실험 노트

캐시 생성 시간, 파일 크기, 재사용 요청의 처리 시간을 적습니다. 생성 비용을 회수하려면 같은 문서에 몇 번 질문해야 하는지 추정하세요.

[공식 참고 자료](https://github.com/ml-explore/mlx-lm)
