# EMIP website drafts

Redesign drafts for [www.emipws.org](https://www.emipws.org). This repository is a fork of [EMIPws/emipws.github.io](https://github.com/EMIPws/emipws.github.io), the source of the live site.

**Compare the drafts and give feedback: <https://emip-website-update.github.io/>**

## Branches

| Branch | What it holds |
| --- | --- |
| `previews` (default) | This README, the compare page and the build that publishes every draft |
| `master` | The live site's source. Kept in sync with EMIPws/emipws.github.io; don't edit it here |
| `design/<name>` | One design draft each, published at `https://emip-website-update.github.io/<name>/` |

The compare page always shows the live site as **Current site**, built straight from EMIPws/emipws.github.io.

## Adding a design

1. Branch from an existing design, so the new branch carries `.github/workflows/preview.yml` (it rebuilds the previews on every push):

   ```
   git switch -c design/<name> design/editorial
   ```

   If you start from `master` instead, copy `.github/workflows/preview.yml` over from `design/editorial`.
2. Push the branch. About two minutes later it appears in the compare page's menus.
3. Optionally give it a title and a one-line note in [`design-notes.json`](design-notes.json) on this branch.

## Feedback

**Give feedback** on the compare page opens a prefilled GitHub issue form ([`design-feedback`](../../issues?q=label%3Adesign-feedback) label) that names the preferred design and the page the reviewer was looking at. The compare page tallies those issues under "Feedback so far". Reviewers without a GitHub account can use **Copy as text** and send their feedback by email.

## How the previews are built

[`build/build_all.py`](build/build_all.py) builds the live site and every `design/*` branch with the gems GitHub Pages uses ([`build/Gemfile`](build/Gemfile)), then moves each one under `/<name>/`: root-relative links are rewritten, pages are marked `noindex` so they don't compete with www.emipws.org in search results, and a small "Draft preview" badge links back to the compare page. It also reports internal links that point nowhere.

The [Build previews](../../actions/workflows/previews.yml) workflow runs when this branch or a design branch is pushed, once a day, and on demand (**Run workflow**). To try a build locally with your own branches:

```
PREVIEW_REMOTE=. python3 build/build_all.py
```

The result is in `_out/`.

## Proposing the chosen design

Open a pull request from the design branch to `master` of EMIPws/emipws.github.io, leaving out `.github/workflows/preview.yml`.
