# -*- coding: utf-8 -*-
"""按「能力」检索提示词库，并返回可直接套用的联动配方。

用法：
    python -X utf8 find.py "商品主图 真实"
    python -X utf8 find.py "局部人脸 逆光" --limit 5
    python -X utf8 find.py --tag 商品主图 --cat 周边
    python -X utf8 find.py "海报 版式" --json

完全离线，只读 capabilities.json。
"""
import argparse
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(BASE, "capabilities.json")

GROUP_WEIGHT = {"用途": 3.0, "能力": 2.5, "质感": 2.0, "模型": 1.0}


def load():
    if not os.path.isfile(INDEX):
        sys.exit("capabilities.json 缺失，先跑 python -X utf8 build_capabilities.py")
    with open(INDEX, encoding="utf-8") as f:
        return json.load(f)


def score(entry, tokens):
    """标签精确命中权重最高，标签模糊命中次之，标题只作小幅加分。
    这样「商品主图」不会被标题里带「超真实」的关系图挤掉。"""
    s = 0.0
    title = entry["title"].lower()
    for tk in tokens:
        if tk in title:
            s += 1.5
        for group, tags in entry["tags"].items():
            w = GROUP_WEIGHT.get(group, 1.0)
            for tag in tags:
                t = tag.lower()
                if tk == t:
                    s += w * 2.0
                elif tk in t or t in tk:
                    s += w * 0.5
    return s


def expand(tokens):
    """中文没有空格，整词「局部人脸」匹配不到「局部特写」。
    拆成 2 字滑窗补一遍，长词本身仍保留。"""
    out = []
    for tk in tokens:
        if tk not in out:
            out.append(tk)
        if len(tk) >= 3 and all("\u4e00" <= c <= "\u9fff" for c in tk):
            for i in range(len(tk) - 1):
                bg = tk[i:i + 2]
                if bg not in out:
                    out.append(bg)
    return out


def sort_key(item):
    s, e = item
    cat, num = e["id"].rsplit("-", 1)
    return (-s, cat, int(num) if num.isdigit() else 0)


def search(data, tokens, cat=None, tag=None, limit=8):
    hits = []
    for e in data["entries"]:
        if cat and e["cat"] != cat:
            continue
        if tag and tag not in sum(e["tags"].values(), []):
            continue
        s = score(e, tokens)
        if tag:
            s += 2.0
        if s > 0:
            hits.append((s, e))
    hits.sort(key=sort_key)
    return hits[:limit]


def match_recipes(data, tokens, limit=3):
    out = []
    for r in data["recipes"]:
        s = sum(1 for k in r["keywords"] if any(k in t or t in k for t in tokens))
        if s:
            out.append((s, r))
    out.sort(key=lambda x: -x[0])
    return out[:limit]


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("query", nargs="*", help="检索词，中英皆可，空格分隔")
    ap.add_argument("--cat", help="限定大类：人物/场景/构图/特效/周边/艺术/NovelAI/Midjourney")
    ap.add_argument("--tag", help="精确限定某个标签")
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    data = load()
    raw = [t.lower() for t in " ".join(args.query).split() if t.strip()]
    tokens = expand(raw)
    if not tokens and not args.tag and not args.cat:
        ap.print_help()
        print("\n词表：")
        for g, tags in data["vocab"].items():
            print("  %s: %s" % (g, " · ".join(tags)))
        return

    hits = search(data, tokens, args.cat, args.tag, args.limit)
    recs = match_recipes(data, tokens)

    if args.json:
        print(json.dumps({
            "query": raw,
            "results": [{"id": e["id"], "title": e["title"], "cat": e["cat"], "tags": e["tags"]}
                        for _, e in hits],
            "recipes": recs,
        }, ensure_ascii=False, indent=1))
        return

    print("Query: %s | 命中 %d 条 | 库内共 %d 条" % (" ".join(raw) or "(标签筛选)", len(hits), data["count"]))
    print("=" * 68)
    for i, (s, e) in enumerate(hits, 1):
        print("%d. %-14s %s" % (i, "`%s`" % e["id"], e["title"]))
        print("   大类 %s ｜ 模型 %s" % (e["cat"], "、".join(e["tags"]["模型"])))
        print("   用途 %s" % ("、".join(e["tags"]["用途"]) or "—"))
        print("   质感 %s" % ("、".join(e["tags"]["质感"]) or "—"))
        print("   能力 %s" % ("、".join(e["tags"]["能力"]) or "—"))
    if not hits:
        print("  （无命中，换同义词或 --tag 试试）")

    if recs:
        print("\n可套用配方")
        print("-" * 68)
        for s, r in recs:
            print("· %s" % r["name"])
            print("  主：`%s`  辅：%s" % (r["main"], "、".join("`%s`" % x for x in r["support"])))
            print("  %s" % r["desc"])
            print("  约束：%s" % r["rule"])


if __name__ == "__main__":
    main()
