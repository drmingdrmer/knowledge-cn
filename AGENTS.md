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
- `static/`: site images and other locally hosted assets.
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

## Card writing: title, conclusion, proof, then supporting details

Keep each card focused on one independently referenceable definition, protocol
rule, counterexample, or conclusion. Its proof and examples must support that
one point. Split out another conclusion when it can serve as a separate premise
or has different proof dependencies. Reuse existing premise cards instead of
repeating their content.

For consensus, introduce quorum, read quorum, write quorum, and quorum
intersection as basic concepts. Use majority as a quorum configuration example.
State which quorum families must intersect in each proof.

Treat a complete workflow or source section as a canvas group when it contains
several knowledge points. In plans, distinguish groups from individual cards.
Choose card boundaries by the knowledge being proved, rather than word counts
or individual algorithm steps. Draw dependency arrows only when the source card
is used to prove the target card; use groups for reading order and motivation.

Arrange each card from the most important information to supplementary details:

1. Start with one main title using `#`.
2. Place the key conclusion in the first paragraph, directly below the title.
   Include the conditions needed to understand the conclusion's scope.
3. Follow with the proof or derivation. Explain how the conclusion follows
   from its premises, including any required definitions and assumptions.
4. Put examples after the proof, followed by further details and references
   as needed.

Except for the main title and opening conclusion paragraph, all content must
belong to a section introduced by a `##` subheading. Use `###` for subdivisions
when needed. Give each subheading a specific description of its section's
content so readers can see the card's structure at a glance.

Size canvas cards for the knowledge overview: show the main title and opening
conclusion, with later sections below the initial viewport. Readers select a
card and press Space to expand it. Keep the full note in the same Markdown file.
Check that the opening conclusion fits and the first subheading stays below
the collapsed card's viewport. Use compact spacing to keep proof paths visible.

## Canvas kinds and connections

Follow the renderer's [board conventions](../obsidian-canvas-render/CONVENTIONS.md).

- Concepts have no color. Theorems use cyan (`"5"`), explanations yellow
  (`"3"`), examples green (`"4"`), and warnings red (`"1"`).
- Proof dependencies keep the default gray, leave the premise's right side,
  and enter the conclusion's left side with an arrow. Place conclusions
  farther right than their premises.
- Optional examples, explanations, and warnings hang below their parent:
  use a green (`"4"`) edge from the parent's bottom to the detail's top.
- Related topics use purple (`"6"`) edges between top sides.
- Orange (`"2"`) is reserved for renderer previews. Hex colors carry no
  semantic kind. Group colors distinguish areas; keep red for warnings.

## Remote renderer

The browser imports `params.knowledge.renderer` from jsDelivr, pinned to
`drmingdrmer/obsidian-canvas-render` tag `v0.1.0`. CSS, libraries, and fonts
resolve relative to that module URL. Canvas files and notes stay on this site.
Keep the renderer URL pinned to an explicit release. Update `hugo.yaml` and
README.md together when upgrading. Load renderer assets at runtime; keep
vendored copies and build-time downloads out of this repository.

The board mounts inside a shadow root. Site styles belong in
`assets/css/main.css`; renderer changes belong in its upstream repository.

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
