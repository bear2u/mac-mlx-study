# 맥 AI 추론 실습실

Apple Silicon 맥에서 AI 추론을 공부하는 한국어 튜토리얼입니다. 기본 강의 12개와 프로젝트 6개의 단계별 실습, 맥용 에이전틱 RAG 튜토리얼 6강을 담았습니다.

[공부 사이트](https://bear2u.github.io/mac-mlx-study/) · [프로젝트 실습](https://bear2u.github.io/mac-mlx-study/projects/)

## 로컬에서 읽기

Node.js 22.23.4 이상을 준비하고 실행합니다.

```sh
cd study
npm ci
npm run dev
```

브라우저에서 [로컬 사이트](http://localhost:7788/)를 엽니다. 강의는 `study/src/content/docs/`에서 수정할 수 있습니다.

## GitHub Pages 빌드

```sh
cd study
SITE_URL=https://bear2u.github.io SITE_BASE=/mac-mlx-study npm run build
```

정적 파일은 `dist/`에 생성됩니다. 공개 버전은 `gh-pages` 브랜치의 루트에서 제공하며, 해당 브랜치에는 정적 파일과 빈 `.nojekyll` 파일을 둡니다. 로컬 전용 설정은 Git에서 제외되는 `study/.env.local`에 둡니다.
