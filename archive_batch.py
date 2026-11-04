# -*- coding: utf-8 -*-
"""2026-10-27 归档批次合并脚本
用法：
  python -X utf8 archive_batch.py          # 只查重 + 预演，不写盘
  python -X utf8 archive_batch.py --write   # 真正写入四个文件
"""
import re, os, sys, difflib, importlib

BASE = os.path.dirname(os.path.abspath(__file__))
WRITE = "--write" in sys.argv

CAT_KEY = {"人物": "renwu", "场景": "changjing", "构图": "goutu",
           "特效": "texiao", "周边": "zhoubian", "艺术": "yishu"}

ENTRIES = []
import glob
mods = sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(BASE, "_new_*.py")))
if not mods:
    print("根目录没有 _new_*.py，没有待入库内容。")
    sys.exit(0)
for mod in mods:
    m = importlib.import_module(mod)
    ENTRIES += m.ENTRIES
print("待入库条目：", len(ENTRIES), "（来源模块：%s）" % "、".join(mods))


def norm(s):
    s = re.sub(r"\s+", "", s)
    return re.sub(r"[，。、；：！？…—·「」『』（）()【】\[\]《》,.;:!?\"'`~@#$%^&*+=|\\/<>_-]", "", s)


master = open(os.path.join(BASE, "PROMPT_MASTER.md"), encoding="utf-8").read()

# 解析现有条目
ANCHOR = re.compile(r'<a id="([a-z]+)-(\d+)"></a>\n### (.+?)\n', re.M)
marks = list(ANCHOR.finditer(master))
existing = []
for i, m in enumerate(marks):
    key, num, title = m.group(1), int(m.group(2)), m.group(3).strip()
    end = marks[i + 1].start() if i + 1 < len(marks) else len(master)
    body = master[m.end():end].strip()
    existing.append({"key": key, "num": num, "title": title, "body": body})
print("现有条目：", len(existing))

# 各类已用最大编号
used = {}
for e in existing:
    used[e["key"]] = max(used.get(e["key"], 0), e["num"])
print("现有编号上限：", used)

# ---- 查重 ----
DUP = 0.85
print("\n=== 查重（阈值 %.2f）===" % DUP)
suspect = []
for idx, ne in enumerate(ENTRIES, 1):
    a = norm(ne["body"])
    best, best_e, best_head = 0.0, None, 0.0
    for e in existing:
        b = norm(e["body"])
        r = difflib.SequenceMatcher(None, a, b).ratio()
        rh = difflib.SequenceMatcher(None, a[:500], b[:500]).ratio()
        if max(r, rh) > best:
            best, best_e, best_head = max(r, rh), e, rh
    flag = "⚠ 疑似重复" if best >= DUP else "ok"
    if best >= DUP:
        suspect.append((ne["title"], best_e["title"], best))
        DUP_cnt = len(suspect)
    print("%2d %-6s %-42s 最高相似 %.3f  ← %s  [%s]" %
          (idx, ne["cat"], ne["title"][:42], best, best_e["title"][:30], flag))

print("\n疑似重复：", len(suspect))
for t, o, r in suspect:
    print("  ", t, "≈", o, "%.3f" % r)

if not WRITE:
    print("\n[预演模式] 未写盘。加 --write 执行。")
    sys.exit(0)

if suspect:
    print("\n存在疑似重复，已中止写盘。请先人工确认。")
    sys.exit(1)

# ---- 写入 cat_*.md ----
from collections import defaultdict
by_cat = defaultdict(list)
for ne in ENTRIES:
    by_cat[ne["cat"]].append(ne)

for cat, items in by_cat.items():
    p = os.path.join(BASE, "cat_%s.md" % cat)
    t = open(p, encoding="utf-8").read()
    block = ""
    for ne in items:
        block += "\n## %s\n\n%s\n\n---\n" % (ne["title"], ne["body"])
    marker = "\n## 跨引用说明"
    if marker in t:
        t = t.replace(marker, block + marker, 1)
    else:
        t = t.rstrip() + "\n" + block
    open(p, "w", encoding="utf-8").write(t)
    print("写入", p, "+%d 条" % len(items))

# ---- 写入 PROMPT_MASTER.md（必须插进对应大类章节内，不能一律追加到文末）----
CAT_ORDER = ["人物", "场景", "构图", "特效", "周边", "艺术"]
NEXT_KEY = {"人物": "changjing", "场景": "goutu", "构图": "texiao",
            "特效": "zhoubian", "周边": "yishu"}

add_by_cat = {}
for ne in ENTRIES:
    k = CAT_KEY[ne["cat"]]
    used[k] += 1
    add_by_cat.setdefault(ne["cat"], "")
    add_by_cat[ne["cat"]] += '\n<a id="%s-%d"></a>\n### %s\n\n%s\n' % (
        k, used[k], ne["title"], ne["body"])

for cat in CAT_ORDER:
    if cat not in add_by_cat:
        continue
    blk = add_by_cat[cat]
    if cat == "艺术":                      # 末类，直接追加
        master = master.rstrip() + "\n" + blk
    else:                                  # 其余插到下一个大类锚点之前
        marker = '<a id="%s"></a>' % NEXT_KEY[cat]
        i = master.index(marker)
        master = master[:i].rstrip() + "\n" + blk + "\n" + master[i:]
open(os.path.join(BASE, "PROMPT_MASTER.md"), "w", encoding="utf-8").write(master)
print("写入 PROMPT_MASTER.md +%d 条（已按大类插入对应章节）" % len(ENTRIES))

# ---- 子目录插入 ----
master = open(os.path.join(BASE, "PROMPT_MASTER.md"), encoding="utf-8").read()
for cat, items in by_cat.items():
    k = CAT_KEY[cat]
    nums = [int(m.group(1)) for m in re.finditer(r'<a id="%s-(\d+)"></a>' % k, master)]
    first_new = nums[-len(items)]
    lines = "".join("- [%s](#%s-%d)\n" % (ne["title"], k, n)
                    for ne, n in zip(items, range(first_new, first_new + len(items))))
    block_re = re.compile(
        r'(<a id="%s"></a>\n## [^\n]+\n\n)((?:- \[[^\]]+\]\(#%s-\d+\)\n)+)' % (k, k))
    m = block_re.search(master)
    if m:
        master = master[:m.start(2)] + m.group(2) + lines + master[m.end(2):]
        print("子目录插入", cat, len(items), "条")
    else:
        print("⚠ 子目录块未匹配，需手工处理：", cat)
open(os.path.join(BASE, "PROMPT_MASTER.md"), "w", encoding="utf-8").write(master)

# ---- INDEX ----
idx_p = os.path.join(BASE, "PROMPT_INDEX.md")
idx = open(idx_p, encoding="utf-8").read()
total_old, total_new = len(existing), len(existing) + len(ENTRIES)
idx = idx.replace("共 **%d 个提示词条目**" % total_old, "共 **%d 个提示词条目**" % total_new)
for cat, items in by_cat.items():
    cnt_old = len([e for e in existing if e["key"] == CAT_KEY[cat]])
    cnt_new = cnt_old + len(items)
    idx = re.sub(r"(\| %s \| )%d( \|)" % (cat, cnt_old), r"\g<1>%d\g<2>" % cnt_new, idx)
    names = "、".join(x["title"] for x in items)
    # 在该行的 包含 列末尾追加
    pat = re.compile(r"(\| %s \| %d \| )([^|]*?)( \|)" % (cat, cnt_new))
    idx = pat.sub(lambda m: m.group(1) + m.group(2)
                  + "；**2026-10-27 新增**：" + names + m.group(3), idx, count=1)
open(idx_p, "w", encoding="utf-8").write(idx)
print("更新 PROMPT_INDEX.md：%d → %d 条" % (total_old, total_new))
print("\n完成。接着请重跑 build_xlsx.py 并读回校验。")
