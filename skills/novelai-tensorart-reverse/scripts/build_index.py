#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a local searchable index of Tensor.Art open prompt articles.

Tensor.Art's /articles page is Nuxt SSR: its __NUXT_DATA__ payload embeds the
FULL HTML body of each listed article. Two sort batches (default MOST_LIKE and
?sort=LATEST) together expose ~79 distinct prompt articles. No private API,
no login, no browser automation needed.

Usage:
    python build_index.py                 # fetch default batches, merge into index
    python build_index.py --refresh      # rebuild index from scratch
    python build_index.py --url URL      # append an extra article-list URL
    python build_index.py --article ID   # append one article detail page
    python build_index.py --no-fetch     # rebuild index.json from cached .txt files
"""
from __future__ import annotations

import argparse
import html as htmlmod
import json
import re
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ART_DIR = ASSETS / "articles"
INDEX = ASSETS / "index.json"

BASE = "https://tensorart.me/articles"   # NOTE: tensor.art is blocked by some proxies; .me works
DEFAULT_URLS = [BASE, BASE + "?sort=LATEST"]
UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
}

# Topic vocabulary: used to auto-tag articles and to support --topic filtering.
TOPICS = {
    "hair":        ["hairstyle", "hair style", "hair color", "bangs", "ponytail",
                    "twintails", "braid", "发型", "发色", "头发", "刘海", "髪", "ヘア"],
    "hand":        ["hand", "finger", "gesture", "fingertips", "手部", "手势", "手指", "手の", "指"],
    "lighting":    ["lighting", "backlight", "rim light", "light effect", "光影",
                    "打光", "布光", "逆光", "照明", "ライティング"],
    "eyes":        ["eyes", "eye color", "iris", "pupil", "眼睛", "瞳", "眼部", "目の"],
    "pose":        ["posture", "pose", "position", "kneeling", "sitting", "danbooru",
                    "姿势", "姿态", "动作", "ポーズ"],
    "background":  ["background", "scenery", "bokeh", "depth of field", "背景", "场景", "散景"],
    "negative":    ["negative prompt", "negative", "负面", "反向提示", "ネガティブ"],
    "quality":     ["masterpiece", "best quality", "score_9", "highres", "画质", "质量", "高清"],
    "weighting":   ["weighting", "parentheses", "curly braces", "emphasis", ":1.5", "权重", "括号"],
    "model":       ["illustrious", "novelai", "pony", "sdxl", "noobai", "checkpoint",
                    "底模", "模型", "大模型"],
    "face":        ["expression", "facial", "blush", "smile", "emotion", "表情", "脸", "颜"],
    "body":        ["body", "skin", "merfolk", "demihuman", "身体", "皮肤", "人鱼", "兽人"],
    "clothing":    ["clothing", "outfit", "headwear", "fashion", "服装", "服饰", "衣装"],
    "perspective": ["perspective", "angle", "close-up", "portrait", "视角", "构图", "透视"],
    "style":       ["style", "stylization", "art style", "ink wash", "ukiyo-e",
                    "画风", "风格", "艺术风格"],
    "workflow":    ["controlnet", "lora", "openpose", "img2img", "inpaint", "训练", "工作流"],
}

# Nuxt 3 devalue special negative indices
SPECIAL = {-1: None, -2: None, -3: None, -4: None, -5: None, -6: -0.0}


def fetch(url: str, retries: int = 2) -> str:
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=45) as resp:
                return resp.read().decode("utf-8", "replace")
        except Exception as e:                       # noqa: BLE001
            last = e
            if i + 1 < retries:
                time.sleep(1.5)
    raise RuntimeError("fetch failed: %s (%s: %s)" % (url, type(last).__name__, last))


def payload_root(page_html: str):
    """Return the de-serialised Nuxt state tree from __NUXT_DATA__."""
    m = re.search(r'<script[^>]*id="__NUXT_DATA__"[^>]*>(.*?)</script>', page_html, re.S)
    if not m:
        m = re.search(r'<script[^>]*data-nuxt-data="nuxt-app"[^>]*>(.*?)</script>', page_html, re.S)
    if not m:
        raise ValueError("no __NUXT_DATA__ payload found")
    arr = json.loads(m.group(1))
    cache = {}

    def get(i):
        if isinstance(i, int) and i < 0:
            return SPECIAL.get(i)
        if i in cache:
            return cache[i]
        v = arr[i]
        if isinstance(v, list):
            out = []
            cache[i] = out
            for x in v:
                out.append(get(x) if isinstance(x, int) and not isinstance(x, bool) else x)
            return out
        if isinstance(v, dict):
            out = {}
            cache[i] = out
            for k, x in v.items():
                out[k] = get(x) if isinstance(x, int) and not isinstance(x, bool) else x
            return out
        cache[i] = v
        return v

    return get(0)


def collect_articles(root, sink: dict):
    """Find every dict that looks like an article (title + HTML content + id)."""
    def walk(o):
        if isinstance(o, dict):
            if (isinstance(o.get("title"), str) and o.get("title")
                    and isinstance(o.get("content"), str) and len(o["content"]) > 80
                    and o.get("id") is not None):
                aid = str(o["id"])
                prev = sink.get(aid)
                if prev is None or len(o["content"]) > len(prev[1]):
                    sink[aid] = (o["title"], o["content"], o)
            for v in o.values():
                if isinstance(v, (dict, list)):
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                if isinstance(v, (dict, list)):
                    walk(v)
    walk(root)


def to_lines(rich_html: str):
    """Flatten article HTML into one tag per line (Tensor.Art articles are tag lists)."""
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", rich_html, flags=re.S | re.I)
    h = re.sub(r"<img[^>]*>", "\n", h, flags=re.I)
    h = re.sub(r"<br\s*/?>|</p>|</li>|</h[1-6]>|</tr>|</div>|</table>", "\n", h, flags=re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    h = htmlmod.unescape(h).replace("\xa0", " ").replace("\u3000", " ")
    lines = []
    for ln in h.split("\n"):
        ln = re.sub(r"[ \t]+", " ", ln).strip()
        if ln:
            lines.append(ln)
    return lines


def tag_topics(title: str, lines):
    blob = (title + "\n" + "\n".join(lines)).lower()
    scores = {}
    for topic, words in TOPICS.items():
        n = sum(blob.count(w.lower()) for w in words)
        if n:
            scores[topic] = n
    return [t for t, _ in sorted(scores.items(), key=lambda kv: -kv[1])[:4]]


def build_record(aid, title, rich_html, meta):
    lines = to_lines(rich_html)
    stat = meta.get("statisticsInfo") or {}
    try:
        likes = int(str(stat.get("likeCount") or 0))
    except ValueError:
        likes = 0
    try:
        reads = int(str(stat.get("readCount") or 0))
    except ValueError:
        reads = 0
    ts = meta.get("publishedAt")
    published = ""
    if isinstance(ts, (int, float)) and ts > 0:
        published = datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d")
    return {
        "id": aid,
        "title": title,
        "url": "https://tensor.art/articles/" + aid,
        "mirror_url": "https://tensorart.me/articles/" + aid,
        "published": published,
        "likes": likes,
        "reads": reads,
        "topics": tag_topics(title, lines),
        "line_count": len(lines),
        "text": "\n".join(lines),
    }


def main():
    ap = argparse.ArgumentParser(description="Build Tensor.Art prompt-article index")
    ap.add_argument("--refresh", action="store_true", help="discard existing index and rebuild")
    ap.add_argument("--url", action="append", default=[], help="extra article-list URL to crawl")
    ap.add_argument("--article", action="append", default=[], help="extra article id to crawl")
    ap.add_argument("--no-fetch", action="store_true", help="rebuild index.json from cached .txt files only")
    args = ap.parse_args()

    ASSETS.mkdir(parents=True, exist_ok=True)
    ART_DIR.mkdir(parents=True, exist_ok=True)

    existing = {}
    if INDEX.exists() and not args.refresh:
        try:
            for a in json.loads(INDEX.read_text(encoding="utf-8")).get("articles", []):
                existing[a["id"]] = a
            print("loaded existing index: %d articles" % len(existing))
        except Exception as e:                       # noqa: BLE001
            print("WARN: could not read existing index: %s" % e, file=sys.stderr)

    urls = []
    if not args.no_fetch:
        urls = list(DEFAULT_URLS) + list(args.url)
        urls += [BASE + "/" + a for a in args.article]
        found = {}
        for u in urls:
            try:
                html = fetch(u)
                root = payload_root(html)
                collect_articles(root, found)
                print("fetched %-58s -> %d article objects (cumulative %d)" % (u[:58], len(found), len(found)))
            except Exception as e:                   # noqa: BLE001
                print("WARN: %s -> %s" % (u, e), file=sys.stderr)
        if not found and not existing:
            print("ERROR: nothing fetched and no cached index. Aborting.", file=sys.stderr)
            return 1
        new = 0
        for aid, (title, rich, meta) in found.items():
            rec = build_record(aid, title, rich, meta)
            if aid not in existing or rec["line_count"] > existing[aid]["line_count"]:
                existing[aid] = rec
                new += 1
        print("new/updated records: %d" % new)
    else:
        # rebuild from cached per-article txt files
        heads = {}
        if INDEX.exists():
            for a in json.loads(INDEX.read_text(encoding="utf-8")).get("articles", []):
                heads[a["id"]] = a
        for p in sorted(ART_DIR.glob("*.txt")):
            aid = p.stem
            lines = p.read_text(encoding="utf-8").splitlines()
            if aid in heads:
                heads[aid]["text"] = "\n".join(lines)
                heads[aid]["line_count"] = len(lines)
                heads[aid]["topics"] = tag_topics(heads[aid]["title"], lines)
                existing[aid] = heads[aid]
        print("rebuilt from %d cached txt files" % len(existing))

    articles = sorted(existing.values(), key=lambda a: (-a["likes"], a["title"]))
    for a in articles:
        (ART_DIR / (a["id"] + ".txt")).write_text(a["text"], encoding="utf-8")

    doc = {
        "built_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": urls or ["cached"],
        "article_count": len(articles),
        "topics": sorted(TOPICS.keys()),
        "articles": articles,
    }
    INDEX.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nINDEX READY: %s" % INDEX)
    print("articles: %d | total tag lines: %d" % (len(articles), sum(a["line_count"] for a in articles)))
    print("topic counts:", {t: sum(1 for a in articles if t in a["topics"]) for t in sorted(TOPICS)})
    return 0


if __name__ == "__main__":
    sys.exit(main())
