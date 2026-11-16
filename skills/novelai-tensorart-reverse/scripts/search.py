#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Search the local Tensor.Art prompt-article index for reusable tags.

The index is built by build_index.py. This script never touches the network.

Usage:
    python search.py hair backlight hand
    python search.py "头发 逆光 手部" --topic hair --limit 4
    python search.py --topic negative --lines 20
    python search.py --list
    python search.py --article 867587987527991248
    python search.py hair --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "assets" / "index.json"

try:
    from build_index import TOPICS          # shared topic vocabulary
except Exception:                            # noqa: BLE001
    TOPICS = {}

# Chinese/Japanese visual descriptors -> English tags used by Tensor.Art articles.
SYNONYMS = {
    "头发": ["hair", "hairstyle", "bangs"], "发丝": ["hair"], "发型": ["hairstyle", "hair"],
    "发色": ["hair color"], "刘海": ["bangs"], "双马尾": ["twintails"],
    "手部": ["hand", "finger", "gesture"], "手指": ["finger", "hand"], "手势": ["gesture", "hand"],
    "逆光": ["backlight", "rim light", "lighting"], "打光": ["lighting"],
    "光影": ["lighting", "light effect"], "光照": ["lighting"],
    "眼睛": ["eyes", "eye"], "瞳孔": ["iris", "pupil", "eyes"],
    "姿势": ["pose", "posture"], "动作": ["pose", "posture", "action"], "体态": ["posture"],
    "背景": ["background"], "景深": ["depth of field", "bokeh"], "虚化": ["bokeh"],
    "负面": ["negative"], "反向": ["negative"], "避坑": ["negative"],
    "画风": ["style", "stylization"], "质感": ["style", "skin", "texture"], "风格": ["style"],
    "表情": ["expression", "facial", "emotion"], "脸部": ["facial", "face"],
    "皮肤": ["skin"], "服装": ["clothing", "outfit"], "服饰": ["clothing"],
    "视角": ["perspective", "angle"], "构图": ["perspective", "composition"],
    "模型": ["model", "illustrious", "novelai", "sdxl"], "底模": ["model", "checkpoint"],
    "权重": ["weighting", "parentheses"], "括号": ["parentheses", "braces"],
    "画质": ["masterpiece", "best quality", "highres"], "人鱼": ["merfolk"],
    "厚涂": ["painterly", "impasto", "style"], "线稿": ["lineart"],
    "髪": ["hair", "hairstyle"], "手": ["hand", "finger"],
    "光": ["lighting", "light"], "目": ["eyes"],
}


def expand(term: str):
    t = term.lower().strip()
    out = [t]
    for cn, ens in SYNONYMS.items():
        if cn in t or t == cn:
            out.extend(ens)
    return list(dict.fromkeys(out))


def score_article(a, terms, topic_filter):
    title = a["title"].lower()
    lines = a["text"].splitlines()
    topics = a.get("topics", [])
    if topic_filter and topic_filter not in topics:
        return None

    # --topic with no keywords: show representative lines of that topic
    if not terms:
        tw = [w.lower() for w in TOPICS.get(topic_filter or "", [])]
        picked = [i for i, ln in enumerate(lines) if any(w in ln.lower() for w in tw)][:40]
        if not picked:
            picked = list(range(min(40, len(lines))))
        return float(a.get("likes", 0)), picked, lines

    score = 0.0
    hits = []
    for term in terms:
        variants = expand(term)
        primary = variants[0]
        if any(v in title for v in variants):
            score += 30                       # a dedicated article beats a long general one
        if any(v == t or v in t for v in variants for t in topics):
            score += 4
        term_hits = []
        for i, ln in enumerate(lines):
            low = ln.lower()
            n = sum(1 for v in variants if v in low)
            if n:
                w = 3.0 if primary in low else 1.6
                term_hits.append((w * min(n, 3) + (2 if len(ln) < 90 else 0), i))
        term_hits.sort(key=lambda x: -x[0])
        score += sum(w for w, _ in term_hits[:4])   # cap: long articles cannot flood the score
        hits.extend(term_hits[:12])
    score += min(a.get("likes", 0), 5000) / 5000.0 * 2   # mild popularity tiebreak

    seen, picked = set(), []
    for w, i in sorted(hits, key=lambda x: -x[0]):
        if i in seen:
            continue
        seen.add(i)
        picked.append(i)
    return score, picked[:40], lines


def main():
    ap = argparse.ArgumentParser(description="Search Tensor.Art prompt-article index")
    ap.add_argument("keywords", nargs="*", help="en/zh/jp visual descriptors")
    ap.add_argument("--topic", help="restrict to a topic (see --topics)")
    ap.add_argument("--topics", action="store_true", help="list available topics")
    ap.add_argument("--limit", type=int, default=5, help="max articles to show (default 5)")
    ap.add_argument("--lines", type=int, default=12, help="max matching tag lines per article")
    ap.add_argument("--list", action="store_true", help="list all indexed article titles")
    ap.add_argument("--article", help="dump the full plain text of one article id")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    if not INDEX.exists():
        print("ERROR: index missing. Run: python scripts/build_index.py", file=sys.stderr)
        return 2
    doc = json.loads(INDEX.read_text(encoding="utf-8"))
    arts = doc["articles"]

    if args.topics:
        print("Available topics:", ", ".join(doc.get("topics", [])))
        print("Built:", doc.get("built_at"), "| articles:", doc.get("article_count"))
        return 0

    if args.list:
        out = [{"id": a["id"], "title": a["title"], "topics": a["topics"],
                "likes": a["likes"], "lines": a["line_count"]} for a in arts]
        if args.json:
            print(json.dumps(out, ensure_ascii=False, indent=1))
        else:
            for a in out:
                print("%s | %-6s | %4d lines | %s" % (
                    a["id"], ",".join(a["topics"][:2]), a["lines"], a["title"]))
        return 0

    if args.article:
        a = next((x for x in arts if x["id"] == args.article), None)
        if not a:
            print("no such article id: %s" % args.article, file=sys.stderr)
            return 1
        print("# %s\n%s\n%s\n" % (a["title"], a["url"], "-" * 60))
        print(a["text"])
        return 0

    raw = re.split(r"[,，;；\s]+", " ".join(args.keywords))
    terms = [t for t in (x.strip().lower() for x in raw) if len(t) >= 2]
    if not terms and not args.topic:
        print("ERROR: give at least one keyword, or use --topic / --list / --article", file=sys.stderr)
        return 2

    ranked = []
    for a in arts:
        r = score_article(a, terms, args.topic)
        if r is None:
            continue
        sc, picked, lines = r
        if terms and sc <= 2:            # only popularity tiebreak -> no real hit
            continue
        ranked.append((sc, a, picked, lines))
    ranked.sort(key=lambda x: -x[0])

    results = []
    for sc, a, picked, lines in ranked[: args.limit]:
        results.append({
            "id": a["id"], "title": a["title"], "url": a["url"],
            "mirror_url": a["mirror_url"], "topics": a["topics"],
            "likes": a["likes"], "score": round(sc, 1),
            "matched_lines": [lines[i] for i in picked[: args.lines]],
        })

    if args.json:
        print(json.dumps({"query": terms, "topic": args.topic, "results": results},
                         ensure_ascii=False, indent=1))
        return 0

    print("Query: %s | topic: %s | index: %s (%d articles) | hits: %d" % (
        " ".join(terms) or "-", args.topic or "-", doc.get("built_at"), len(arts), len(ranked)))
    if not results:
        print("\nNo matches. Try broader English tags, --list to browse, or rebuild the index.")
        return 0
    for n, r in enumerate(results, 1):
        print("\n" + "=" * 68)
        print("#%d  %s   [score %s]" % (n, r["title"], r["score"]))
        print("URL : %s" % r["url"])
        print("info: topics=%s | likes=%s" % (",".join(r["topics"]), r["likes"]))
        print("matched tag lines:")
        for ln in r["matched_lines"]:
            print("   - " + ln[:240])
    print("\n" + "=" * 68)
    print("REMINDER: these are building-block tags, not a full style prompt.")
    print("Style/texture comes from the base model + LoRA. Do not stack tags or negatives.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
