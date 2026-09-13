#!/usr/bin/env python3
"""Refresh the blog-post list in README.md from the blogs' RSS feeds.

Only the region between the BLOG-POSTS markers is rewritten; everything else in
the README is hand-written and must survive untouched.

No third-party dependencies — the two feeds are well-formed RSS 2.0, so the
standard library covers it and CI needs no install step.
"""

from __future__ import annotations

import html
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"

START_MARKER = "<!-- BLOG-POSTS:START -->"
END_MARKER = "<!-- BLOG-POSTS:END -->"

POSTS_PER_BLOG = 5
TIMEOUT_SECONDS = 30
USER_AGENT = "Twodragon0-profile-readme/1.0 (+https://github.com/Twodragon0/Twodragon0)"


@dataclass(frozen=True)
class Blog:
    label: str
    site: str
    feed: str
    # Post links must stay on this host. A feed that starts handing out links
    # elsewhere is either compromised or misconfigured; either way it does not
    # belong in a README that represents me.
    host: str


# 2twodragon.com is deliberately absent: it serves no feed. /rss, /feed and
# /feed/ all answer HTTP 200 with zero <item> elements (checked 2026-09-11).
# It is still linked from the README, just not collected.
BLOGS = (
    Blog(
        label="Tech Blog",
        site="https://tech.2twodragon.com",
        feed="https://tech.2twodragon.com/feed.xml",
        host="tech.2twodragon.com",
    ),
    Blog(
        label="Tistory",
        site="https://twodragon.tistory.com",
        feed="https://twodragon.tistory.com/rss",
        host="twodragon.tistory.com",
    ),
)


def clean(text: str) -> str:
    """Normalise a feed title to exactly one level of escaping.

    Feeds differ in how many times they encode entities. Escaping blindly turns
    an already-encoded "Docker &amp; Kubernetes" into "&amp;amp;", which renders
    as literal "&amp;". Unescape to a fixed point, then escape once.
    """
    previous = None
    current = text
    while current != previous:
        previous = current
        current = html.unescape(current)
    current = " ".join(current.split())
    # Markdown link text: brackets would break the link, quotes are harmless.
    current = current.replace("[", "(").replace("]", ")")
    return html.escape(current, quote=False)


def fetch(blog: Blog) -> list[tuple[datetime, str, str]]:
    request = urllib.request.Request(blog.feed, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            raw = response.read()
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        print(f"  ! {blog.label}: fetch failed: {error}", file=sys.stderr)
        return []

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as error:
        print(f"  ! {blog.label}: not parseable as XML: {error}", file=sys.stderr)
        return []

    posts: list[tuple[datetime, str, str]] = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not title or not link:
            continue
        if urllib.parse.urlparse(link).hostname != blog.host:
            print(f"  ! {blog.label}: off-host link skipped: {link}", file=sys.stderr)
            continue
        raw_date = (item.findtext("pubDate") or "").strip()
        try:
            published = parsedate_to_datetime(raw_date)
        except (TypeError, ValueError):
            published = datetime.min.replace(tzinfo=timezone.utc)
        if published.tzinfo is None:
            published = published.replace(tzinfo=timezone.utc)
        posts.append((published, clean(title), link))

    posts.sort(key=lambda post: post[0], reverse=True)
    return posts


def render(results: list[tuple[Blog, list[tuple[datetime, str, str]]]]) -> str:
    lines: list[str] = []
    for blog, posts in results:
        if not posts:
            continue
        lines.append(f"**[{blog.label}]({blog.site})**")
        lines.append("")
        for _, title, link in posts[:POSTS_PER_BLOG]:
            lines.append(f"- [{title}]({link})")
        lines.append("")
    # Each blog gets its own list rather than one merged "latest N". The two
    # publish at very different rates, so a merged cut silently drops the
    # slower blog entirely.
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append(f"<sub>Updated {stamp} — see <code>scripts/update_blog_posts.py</code></sub>")
    return "\n".join(lines)


def main() -> int:
    results = []
    for blog in BLOGS:
        posts = fetch(blog)
        print(f"  {blog.label}: {len(posts)} posts")
        results.append((blog, posts))

    if not any(posts for _, posts in results):
        # Leave the README alone rather than replacing it with an empty list.
        print("no posts from any feed; leaving README unchanged", file=sys.stderr)
        return 1

    text = README.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    if not pattern.search(text):
        print(f"markers not found in {README}", file=sys.stderr)
        return 1

    block = f"{START_MARKER}\n\n{render(results)}\n\n{END_MARKER}"
    README.write_text(pattern.sub(lambda _: block, text, count=1), encoding="utf-8")
    print(f"wrote {README}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
