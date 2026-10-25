# Knowledge 中文版

分布式系统、数学与软件的关联知识卡片。

**[阅读网站](https://drmingdrmer.github.io/knowledge-cn/)**

The site uses Hugo 0.164.0 and adapts the templates and styles from
[OpenACID Blog](https://github.com/openacid/openacid.github.io). Its interactive
maps use a local copy of
[obsidian-canvas-render](https://github.com/drmingdrmer/obsidian-canvas-render)
at commit `8b5cdc33af5beb644bf8ab07e25c406c29e615a4`. The renderer's license and
the libraries' licenses are included under `static/renderer/`.

## Preview and verify

Run `hugo server` to preview the site. The production checks are:

```sh
hugo --gc --minify --panicOnWarning
python3 tests/test_site.py
```

## Add content

Hugo pages live in `content/`. A normal Markdown page needs `title` and
`description` in its YAML front matter.

Maps live in `static/canvases/`; the notes they reference live in `static/vault/`.
File paths in a canvas are relative to that vault root. A map's Hugo page uses:

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
