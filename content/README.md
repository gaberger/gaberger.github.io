# Lambda FU: extracted content

Markdown copies of the posts on www.firstclassfunc.com, taken from the built
Hugo HTML in this repository. The Hugo source was never committed, so these
files are the only editable copy of the posts.

- `posts/<slug>/index.md`: one folder per post, with front matter (title, date,
  categories, tags, original URL) and its images alongside.
- `about.md`: the author card from the sidebar.

The layout matches Hugo page bundles, so `posts/` can be dropped into a Hugo
site's `content/` folder as-is.

Not carried over: the `1/01/a-brief-look-at-network-automation/` page, a stale
copy of the automation post dated year 1. The Facebook post also links one
image from Facebook's CDN, which was never stored in the repo.
