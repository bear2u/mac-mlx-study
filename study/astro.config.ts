import { existsSync } from "node:fs";
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import nimbus, {
  defineConfig as defineNimbusConfig,
} from "@cloudflare/nimbus-docs";
import { tableScroll } from "@cloudflare/nimbus-docs/markdown";

const localEnv = new URL(".env.local", import.meta.url);
if (existsSync(localEnv)) process.loadEnvFile(localEnv);

const nimbusConfig = defineNimbusConfig({
  site: process.env.SITE_URL || "http://localhost:7788",
  title: "맥 AI 추론 실습실",
  description: "내 맥에서 언어 모델을 실행하고 추론 성능을 측정하는 열두 번의 실험",
  locale: "ko",
  socialImageAlt: "맥 AI 추론 실습실 학습 안내",
  sidebar: {
    items: ["index", { autogenerate: { collection: "docs" } }],
  },
});

export default defineConfig({
  // nimbus:adapter
  output: "static",
  base: process.env.SITE_BASE || "/",
  server: { host: "127.0.0.1", port: 7788 },
  // Tailwind v4 via its Vite plugin (the integration Astro recommends for
  // Tailwind v4 — replaces the PostCSS plugin, which doesn't build under
  // Astro 7's Vite 8 bundler).
  vite: {
    preview: { allowedHosts: process.env.PREVIEW_HOST ? [process.env.PREVIEW_HOST] : [] },
    plugins: [tailwindcss()],
  },
  // Hover-prefetch link targets so full-page navigations feel instant without
  // a client-side router.
  prefetch: {
    prefetchAll: true,
    defaultStrategy: "hover",
  },
  integrations: [
    nimbus(nimbusConfig, {
      // Authoring rules are opt-in by design — your repo, your taste. The
      // two below are the load-bearing pair: frontmatter has to validate
      // against the content schema for the page to render properly, and
      // broken internal links are 404s for your readers. Add the others
      // (heading hierarchy, code-block language, style, etc.) when you're
      // ready to enforce them — see `nimbus-docs lint --help`.
      rules: {
        "nimbus/frontmatter-shape": "error",
        "nimbus/internal-link": "error",
      },
      markdown: {
        // Wrap wide tables so they scroll instead of overflowing the page
        // (styled by `.nb-table-scroll` in src/styles/prose.css).
        hastPlugins: [tableScroll()],
        // `## Install {#install}` gives a heading a fixed id. A heading that
        // ends in other `{…}` text, such as `{account_id}` in a .md file, is
        // read as attributes too; remove this to keep it as text.
        features: { headingAttributes: true },
      },
    }),
  ],
});
