#!/usr/bin/env python3
"""Build the live site and every design/* branch into one static preview site.

Each version is built with Jekyll the way GitHub Pages builds www.emipws.org,
then moved under /<slug>/: root-relative links are rewritten, search engines
are told not to index it, and a small "draft preview" badge is added. The
compare page from site/ goes at the root, with designs.json describing every
version.

Run from the root of a checkout of the `previews` branch:

    python3 build/build_all.py            # build into _out/
    python3 build/build_all.py --only editorial
"""
import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_out"
SRC = ROOT / "_src"
UPSTREAM = "https://github.com/EMIPws/emipws.github.io.git"
REPO = os.environ.get("GITHUB_REPOSITORY", "EMIP-website-update/emip-website-update.github.io")
# Where design/* branches are read from; "." uses local branches when testing.
REMOTE = os.environ.get("PREVIEW_REMOTE", "origin")

ATTR = re.compile(r"""(\s(?:href|src|action|poster)\s*=\s*["'])/(?!/)""", re.I)
SRCSET = re.compile(r"""(\ssrcset\s*=\s*)(["'])(.*?)\2""", re.I | re.S)
CSS_URL = re.compile(r"""(url\(\s*["']?)/(?!/)""", re.I)
REFRESH = re.compile(r"""(http-equiv=["']refresh["']\s+content=["']\d+;\s*url=)/(?!/)""", re.I)
HEAD = re.compile(r"<head(\s[^>]*)?>", re.I)
BODY_END = re.compile(r"</body>", re.I)
LINK = re.compile(r"""\s(?:href|src)\s*=\s*["']([^"'#?]*)""", re.I)


def git(*args, capture=False):
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, text=True,
                            stdout=subprocess.PIPE if capture else None)
    return result.stdout.strip() if capture else None


def versions():
    """The live site first, then every design/* branch of this repository."""
    found = [{"slug": "current", "branch": "master", "remote": UPSTREAM,
              "branch_url": "https://github.com/EMIPws/emipws.github.io/tree/master"}]
    heads = git("ls-remote", "--heads", REMOTE, "refs/heads/design/*", capture=True)
    for line in filter(None, heads.splitlines()):
        branch = line.split("refs/heads/", 1)[1]
        found.append({"slug": branch.split("/", 1)[1].replace("/", "-"), "branch": branch,
                      "remote": REMOTE, "branch_url": f"https://github.com/{REPO}/tree/{branch}"})
    return found


def checkout(version):
    ref = f"refs/preview/{version['slug']}"
    # Shallow fetches only in CI: locally they would mark commits in your own
    # repository as shallow and hide their history.
    depth = ["--depth", "1"] if os.environ.get("GITHUB_ACTIONS") else []
    git("fetch", "--quiet", *depth, "--no-tags", version["remote"],
        f"+refs/heads/{version['branch']}:{ref}")
    sha, date, subject = git("log", "-1", "--format=%H%x00%cI%x00%s", ref, capture=True).split("\x00")
    version.update(sha=sha, date=date, subject=subject)
    dest = SRC / version["slug"]
    if dest.exists():
        git("worktree", "remove", "--force", str(dest))
    git("worktree", "add", "--quiet", "--detach", str(dest), ref)
    return dest


def jekyll(src, dest):
    config = f"{src / '_config.yml'},{ROOT / 'build' / '_config.ghpages.yml'}"
    env = dict(os.environ, JEKYLL_ENV="production")
    env.setdefault("BUNDLE_GEMFILE", str(ROOT / "build" / "Gemfile"))
    subprocess.run(["bundle", "exec", "jekyll", "build", "--source", str(src),
                    "--destination", str(dest), "--config", config],
                   cwd=ROOT, env=env, check=True)


def prefix_srcset(match, base):
    parts = []
    for part in match.group(3).split(","):
        part = part.strip()
        if part.startswith("/") and not part.startswith("//"):
            part = base + part[1:]
        parts.append(part)
    return match.group(1) + match.group(2) + ", ".join(parts) + match.group(2)


def move_under(dest, version):
    """Rewrite a site built for "/" so it works from /<slug>/."""
    base = f"/{version['slug']}/"
    badge = (f'<script src="/_hub/badge.js" data-design="{html.escape(version["slug"])}" '
             f'data-title="{html.escape(version["title"])}" defer></script>')
    (dest / "CNAME").unlink(missing_ok=True)
    for path in dest.rglob("*"):
        if path.suffix not in (".html", ".css"):
            continue
        text = path.read_text(encoding="utf-8", errors="surrogateescape")
        text = ATTR.sub(lambda m: m.group(1) + base, text)
        text = SRCSET.sub(lambda m: prefix_srcset(m, base), text)
        text = CSS_URL.sub(lambda m: m.group(1) + base, text)
        text = REFRESH.sub(lambda m: m.group(1) + base, text)
        if path.suffix == ".html":
            text = HEAD.sub(lambda m: m.group(0) + '<meta name="robots" content="noindex, nofollow">', text, count=1)
            text = BODY_END.sub(lambda m: badge + m.group(0), text, count=1)
        path.write_text(text, encoding="utf-8", errors="surrogateescape")


def broken_links(dest, slug):
    """Internal links that point at nothing, as (page, target) pairs."""
    missing = set()
    for page in dest.rglob("*.html"):
        for target in LINK.findall(page.read_text(encoding="utf-8", errors="replace")):
            if not target.startswith(f"/{slug}/"):
                continue
            local = OUT / target.lstrip("/")
            if not (local.is_file() or (local / "index.html").is_file() or local.with_suffix(".html").is_file()):
                missing.add((str(page.relative_to(OUT)), target))
    return sorted(missing)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--only", help="build just this slug (plus the compare page)")
    args = parser.parse_args()

    notes = json.loads((ROOT / "design-notes.json").read_text())
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    SRC.mkdir(exist_ok=True)

    built = []
    for version in versions():
        if args.only and version["slug"] != args.only:
            continue
        note = notes.get(version["slug"], {})
        version["title"] = note.get("title") or version["slug"].replace("-", " ").capitalize()
        version["note"] = note.get("note", "")
        version["featured"] = bool(note.get("featured"))
        print(f"\n== {version['title']} ({version['branch']})", flush=True)
        src = checkout(version)
        dest = OUT / version["slug"]
        jekyll(src, dest)
        move_under(dest, version)
        version["url"] = f"/{version['slug']}"
        version.pop("remote")
        built.append(version)

    shutil.copytree(ROOT / "site", OUT, dirs_exist_ok=True)
    (OUT / "designs.json").write_text(json.dumps({"repo": REPO, "designs": built}, indent=2))

    for version in built:
        missing = broken_links(OUT / version["slug"], version["slug"])
        print(f"{version['slug']}: {len(missing)} broken internal link(s)")
        for page, target in missing[:15]:
            print(f"  {page} -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
