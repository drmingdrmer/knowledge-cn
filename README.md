# Knowledge 中文版

分布式系统、数学与软件的关联知识卡片。

**[阅读网站](https://drmingdrmer.github.io/knowledge-cn/)**

The site uses Hugo 0.164.0 and adapts the templates and styles from
[OpenACID Blog](https://github.com/openacid/openacid.github.io). Its interactive
maps load [obsidian-canvas-render v0.1.0](https://github.com/drmingdrmer/obsidian-canvas-render/tree/v0.1.0)
directly from jsDelivr in the browser. `params.knowledge.renderer` in
`hugo.yaml` sets the tagged URL. The renderer's CSS, libraries, and fonts load
from the same CDN path; canvases and notes are served by this site.

## Preview and verify

Run `hugo server` to preview the site. Browsing a map requires access to
`cdn.jsdelivr.net`. The production checks are:

```sh
hugo --gc --minify --panicOnWarning
python3 tests/test_site.py
```

## Add content

Open `vault/` as a vault in Obsidian. Edit canvases, cards, and site pages there.

- `vault/canvases/`: maps, including nested topic folders.
- `vault/notes/<topic>/`: Markdown cards and attachments referenced by maps.
- `vault/pages/`: Hugo pages, including the home page, guide, and topic pages.
- `vault/plans/`: planning notes, excluded from the published site.

Canvas file references are relative to `vault/`, such as
`notes/distributed-consensus/majority.md`. Obsidian updates links when files move.
New notes default to `notes/`, pasted attachments to `notes/attachments/`, and
note links use relative paths. Create or move maps into `canvases/`.
Local workspace state and trash are ignored by Git; Obsidian settings are
excluded from the published site.

Hugo reads pages from `vault/pages/`, publishes cards under `vault/notes/`, and
publishes canvases under `canvases/` to preserve existing website URLs.
Earlier Markdown URLs under `vault/` remain available for saved note views.
Each site page needs `title` and `description` in its YAML front matter.
A map's page uses:

```yaml
---
title: My topic
description: What this map explains.
layout: canvas
canvas: canvases/my-topic.canvas
---
```

Every map page appears on the home page automatically. Paths in `canvas`,
`vault`, and site asset settings are relative to the site's base URL; omit
the leading slash so they also work under GitHub Pages' `/knowledge-cn/` path.

## Publish

Pushes to `main` build, check, and deploy through
[GitHub Actions](https://github.com/drmingdrmer/knowledge-cn/actions/workflows/pages.yml).
Pull requests run the same build and checks. GitHub Pages uses **GitHub Actions**
as its publishing source. Update `baseURL` in `hugo.yaml` when moving the site.
