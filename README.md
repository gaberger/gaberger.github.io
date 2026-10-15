# gaberger.github.io

A Field CTO Perspective, Gary Berger's blog, built with Hugo and deployed to GitHub Pages by
`.github/workflows/pages.yml` on every push to `master`.

- `content/posts/<slug>/index.md`: one folder per post, front matter plus its
  images. The posts were extracted from the 2017 Hugo build.
- `content/about.md`: the About page.
- `site/`: Hugo config (`hugo.toml`), layouts and CSS. The theme lives here, so
  the build has no outside dependency.

The HTML at the repository root (`index.html`, `2017/`, `tags/` and the rest)
is the built site. Don't edit it by hand: the workflow rebuilds it from
`content/` and `site/` and commits it on every push to `master`, because GitHub
Pages serves the root of `master`. Old 2017 URLs that the new site doesn't
cover redirect from stubs in `site/static/`.

## Writing a post

Add `content/posts/<slug>/index.md`:

```markdown
---
title: "Post title"
date: 2026-10-14
categories: ["network"]
tags: ["bpf"]
---

Body in Markdown. Images go in the same folder.
```

Preview locally with `cd site && hugo server`.

## Hosting

The site is served at https://gaberger.github.io from the root of `master`. If
**Settings → Pages → Source** is later switched to **GitHub Actions**, the same
workflow's Pages artifact takes over and nothing else needs to change.
