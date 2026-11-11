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

## Project and experiment cards

`content/projects.md` and `content/experiments.md` list one card per project.
`url` is the GitHub repository. If the project also has a github.io site, add
it as `site`: the card's title then opens the site, and the card shows both a
Site and a GitHub link.

```yaml
      - name: "Earshot"
        site: "https://gaberger.github.io/earshot/"
        url: "https://github.com/gaberger/earshot"
```

A repository with GitHub Pages turned on owns `gaberger.github.io/<repo>/` and
hides any page of this blog at the same path. That is why the `experiments`
repository has Pages turned off.

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

Then generate the post's header image and link-preview card:

```bash
pip install playwright && playwright install chromium   # once
python3 scripts/make-covers.py <slug>
```

This writes `hero.jpg` (shown at the top of the post) and `cover.jpg` (the
1200x630 LinkedIn preview, with the title) into the post folder. Each post gets
its own network-graph artwork, seeded from the slug, so re-running reproduces it.
Use `--force` to regenerate after changing a title.

For a diagram with a dark-mode version, save it as `name-dark.png` next to
`name.png`; the theme toggle shows the matching one.

Preview locally with `cd site && hugo server`.

## Hosting

The site is served at https://gaberger.github.io from the root of `master`. If
**Settings → Pages → Source** is later switched to **GitHub Actions**, the same
workflow's Pages artifact takes over and nothing else needs to change.
