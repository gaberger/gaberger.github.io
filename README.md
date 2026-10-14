# gaberger.github.io

A Field CTO Perspective, Gary Berger's blog, built with Hugo and deployed to GitHub Pages by
`.github/workflows/pages.yml` on every push to `master`.

- `content/posts/<slug>/index.md`: one folder per post, front matter plus its
  images. The posts were extracted from the 2017 Hugo build.
- `content/about.md`: the About page.
- `site/`: Hugo config (`hugo.toml`), layouts and CSS. The theme lives here, so
  the build has no outside dependency.

The HTML at the repository root (`index.html`, `2017/`, `tags/` and the rest)
is the old 2017 build. Once Pages is switched to GitHub Actions it is no longer
served, and it can be deleted.

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

## One-time setup

In the repository's **Settings → Pages**, set **Source** to **GitHub Actions**
and clear the custom domain. `firstclassfunc.com` is no longer owned.
