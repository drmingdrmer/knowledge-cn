# Knowledge website

This repository builds https://drmingdrmer.github.io/knowledge-cn/ with Hugo
0.164.0. Its templates and styles come from OpenACID Blog. Keep changes
scoped to this repository unless the user requests work elsewhere.

## Source files and generated output

- `vault/`: the Obsidian vault; edit all knowledge Markdown and canvases here.
- `vault/pages/`: Hugo pages, including the home page, guide, and map pages.
- `vault/canvases/`: Obsidian JSON Canvas files.
- `vault/notes/<topic>/`: Markdown cards and attachments referenced by canvases.
- `vault/plans/`: planning notes, excluded from the published site.
- `vault/.obsidian/`: shared Obsidian settings; local workspace files are ignored.
- `layouts/`: Hugo templates and Markdown render hooks.
- `assets/`: CSS and JavaScript processed and fingerprinted by Hugo.
- `static/renderer/`: vendored canvas renderer, libraries, fonts, and licenses.
- `hugo.yaml`: site URL, menus, renderer paths, and Markdown settings.
- `tests/test_site.py`: checks generated links, map pages, and bundled notes.
- `public/` and `resources/`: ignored build output; edit source files instead.

## Content and URL rules

Normal Hugo pages need `title` and `description` in their YAML front matter.
A map page also needs `layout: canvas` and a `canvas` path such as
`canvases/my-topic.canvas`. The home page lists map pages automatically.
See [README.md](README.md#add-content) for the content format.

File paths inside a canvas are relative to the vault root, normally
`vault/`. Preserve those paths when moving or copying notes and attachments.
Keep a Hugo topic page in `vault/pages/` for every published canvas.

Hugo reads `vault/pages/` as content, mounts `vault/canvases/` at
`static/canvases`, and mounts `vault/notes/` at `static/vault/notes`.
A Markdown-only mount at `static/vault` preserves earlier note URLs.
Mount these directories separately so Hugo watches edits in each component.
Obsidian settings, trash, and plans stay outside the published mounts.

The production URL includes `/knowledge-cn/`. Keep configured asset, canvas,
and vault paths relative to the site base URL, without a leading slash.
Use `relURL` for these paths, `.RelPermalink` for page links, and `relref`
for Markdown links between Hugo pages. Check generated URLs when changing
templates; a root-relative path can bypass the GitHub Pages project prefix.

Keep reader-facing pages focused on the knowledge and its connections.
Put publishing and development instructions in the README.

## Vendored renderer

When updating `static/renderer/`, copy a specific upstream commit from
`drmingdrmer/obsidian-canvas-render` with its libraries, fonts, and licenses.
Update the recorded revision in README.md. Keep the renderer's assets
locally served so maps use the same origin as their notes.

The board mounts inside a shadow root. Site styles belong in
`assets/css/main.css`; renderer styles belong to the vendored bundle.

## Build and verification

Use the Hugo version pinned in `.github/workflows/pages.yml`. Run these
production checks after changing site code or content:

```sh
hugo --gc --minify --panicOnWarning
python3 tests/test_site.py
```

Run `hugo server` for local preview. For layout or interaction changes,
check the affected pages in a browser at desktop and narrow widths.
For renderer integration changes, also check loaded notes, formulas,
search, card sizing, and rendered/source note views. Inspect page errors
and failed asset requests, including paths under `/knowledge-cn/`.

## Publishing

`.github/workflows/pages.yml` builds and checks pull requests. Pushes to
`main` also deploy `public/` to GitHub Pages. Pages uses GitHub Actions as
its publishing source, with the `github-pages` environment restricted to
`main`. Stage, commit, push, and change GitHub settings only when requested.
