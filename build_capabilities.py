# -*- coding: utf-8 -*-
"""从 PROMPT_MASTER.md 生成能力索引（capabilities.json + CAPABILITIES.md）。

用法：
    python -X utf8 build_capabilities.py

词表固定，新增条目自动按规则打标；规则覆盖不到的用手写 OVERRIDES 补。
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "PROMPT_MASTER.md")
OUT_JSON = os.path.join(BASE, "capabilities.json")
OUT_MD = os.path.join(BASE, "CAPABILITIES.md")

CAT_NAME = {
    "renwu": "人物", "changjing": "场景", "goutu": "构图", "texiao": "特效",
    "zhoubian": "周边", "yishu": "艺术", "novelai": "NovelAI", "midjourney": "Midjourney",
}

# ---------- 固定词表 ----------
VOCAB = {
    "用途": ["商品主图", "工艺品", "人像写真", "脸模角色", "角色设定", "海报版式",
             "局部特写", "巨物场景", "场景氛围", "建筑空间", "美食", "抽象材质",
             "分镜叙事", "视频片段", "信息图", "特效光效"],
    "质感": ["真实摄影", "半写实CG", "日系厚涂", "平面图形", "工艺材质",
             "电影感", "水彩手绘", "3D渲染"],
    "能力": ["白底抠图", "换背景", "打光增强", "材质重渲", "模特换装", "排版文字",
             "构图重构", "风格迁移", "局部精修", "尺度对比", "光效营造"],
    "模型": ["Midjourney", "NovelAI", "SD", "通用"],
}

RULES = {
    "用途": [
        ("商品主图", ["电商商品图", "商品", "白底", "平铺图", "产品打光", "主图", "换装"]),
        ("工艺品", ["冰箱贴", "螺钿", "珐琅", "漆器", "团扇", "工艺"]),
        ("脸模角色", ["脸模"]),
        ("角色设定", ["三视图", "角色设定", "资产图", "角色渲染"]),
        ("人像写真", ["写真", "人像", "COS", "Cosplay", "私房", "随手拍", "博主", "穿搭", "少女角色"]),
        ("海报版式", ["海报", "封面", "艺术字", "版式", "邮票", "拼贴", "编辑设计", "剧情"]),
        ("局部特写", ["特写", "局部", "半脸", "单眼", "close-up", "眼部"]),
        ("巨物场景", ["巨构", "巨物", "巨莲", "巨型", "megalophobia", "尺度"]),
        ("建筑空间", ["建筑", "室内", "客厅", "沙盘", "凉亭", "卧室"]),
        ("分镜叙事", ["分镜", "一镜到底", "storyboard", "景别", "短剧"]),
        ("视频片段", ["视频"]),
        ("信息图", ["设计可视化", "信息图"]),
        ("特效光效", ["仙侠人物特效", "特效"]),
        ("美食", ["美食", "食品", "拉面", "食物"]),
        ("抽象材质", ["抽象", "几何", "材质解构", "液态"]),
        ("场景氛围", ["场景", "景观", "全景", "荷塘", "林", "海", "竹林", "樱花", "客厅"]),
    ],
    "质感": [
        ("真实摄影", ["真实感", "写实", "摄影", "实拍", "EOS", "手机", "照片", "真人"]),
        ("半写实CG", ["超真实AIGC", "3D CG", "CGI", "半写实", "CG 动画"]),
        ("3D渲染", ["3D 渲染", "octane", "渲染材质", "VFX"]),
        ("日系厚涂", ["厚涂", "painterly", "逆光", "日系", "2.5D"]),
        ("平面图形", ["海报", "版式", "图形", "极简", "包豪斯", "Risograph", "halftone", "平面构成"]),
        ("工艺材质", ["螺钿", "珐琅", "漆", "和纸", "纸艺", "贝壳", "木刻", "丝网", "冰箱贴"]),
        ("水彩手绘", ["水彩", "蜡笔", "涂鸦", "手绘", "Doodle", "漫画风"]),
        ("电影感", ["电影", "cinematic", "镜头", "剧照"]),
    ],
    "能力": [
        ("白底抠图", ["白底"]),
        ("换背景", ["场景融合", "换背景", "转绘", "再创作", "实景融合", "转插画", "转译"]),
        ("打光增强", ["打光", "光效", "lighting", "逆光", "体积光"]),
        ("材质重渲", ["3D 渲染材质", "材质", "工艺质感", "渲"]),
        ("模特换装", ["换装", "穿搭"]),
        ("排版文字", ["艺术字", "排版", "版式", "文字", "typography", "题签"]),
        ("构图重构", ["构图", "景别", "取景", "平面构成"]),
        ("风格迁移", ["转插画", "风格码", "风格 tag", "转译", "再创作", "实景融合"]),
        ("局部精修", ["精修", "无痕去除"]),
        ("尺度对比", ["巨物", "巨构", "巨莲", "巨型", "尺度"]),
        ("光效营造", ["逆光", "体积光", "光斑", "flare", "光效"]),
    ],
}

OVERRIDES = {
    # 2026-11-24 批次 K：21:9 材质母题系列——人只占三分之一、景占三分之二，
    # 规则词表抓不到「人像 + 环境」双栖属性，手写补齐；打光/材质/光效是本系列的核心手法。
    **{"midjourney-%d" % i: {"用途": ["人像写真", "场景氛围"],
                             "质感": ["半写实CG", "电影感"],
                             "能力": ["打光增强", "材质重渲", "光效营造"]}
       for i in range(22, 29)},
    # 重打光母版：正文里的「版式」是描述对象不是产出（它出的是图，不是海报），故整组替换用途。
    "yishu-43": {"用途": {"tags": ["人像写真"], "replace": True},
                 "质感": ["半写实CG", "电影感"],
                 "能力": ["打光增强", "材质重渲", "光效营造"],
                 # 正文提到「若在 Midjourney 里用」会被模型识别误判，本条实际是通用指令
                 "模型": ["通用"]},
    "yishu-44": {"用途": {"tags": ["海报版式"], "replace": True},
                 "能力": ["排版文字", "构图重构"]},
    "midjourney-29": {"用途": ["海报版式"]},
    "renwu-1": {"用途": ["脸模角色"]},
    "renwu-3": {"用途": ["人像写真"], "能力": ["局部精修", "换背景"], "质感": ["真实摄影"]},
    "renwu-9": {"用途": ["人像写真"], "质感": ["真实摄影", "电影感"]},
    "zhoubian-2": {"用途": ["商品主图"], "能力": ["打光增强", "材质重渲"], "质感": ["真实摄影"]},
    "zhoubian-3": {"用途": ["商品主图"], "能力": ["白底抠图", "局部精修"], "质感": ["真实摄影"]},
    "zhoubian-5": {"用途": ["商品主图"], "能力": ["打光增强", "光效营造"], "质感": ["真实摄影"]},
    "zhoubian-6": {"用途": ["商品主图"], "能力": ["材质重渲"], "质感": ["3D渲染"]},
    "zhoubian-7": {"用途": ["商品主图"], "能力": ["模特换装"], "质感": ["真实摄影"]},
    "novelai-6": {"用途": ["局部特写"], "质感": ["日系厚涂"], "能力": ["光效营造", "风格迁移"]},
    "novelai-9": {"用途": ["局部特写"], "质感": ["日系厚涂"], "能力": ["光效营造", "构图重构"]},
    "midjourney-14": {"用途": ["巨物场景", "场景氛围"], "能力": ["尺度对比"]},
    "midjourney-19": {"用途": ["人像写真"], "质感": ["3D渲染"]},
    "yishu-13": {"用途": ["海报版式"], "能力": ["风格迁移", "构图重构"]},
}

RECIPES = [
    {
        "name": "新品商品主图（真实棚拍）",
        "keywords": ["商品主图", "产品", "主图", "棚拍", "真实"],
        "main": "zhoubian-2",
        "support": ["zhoubian-3", "zhoubian-5"],
        "desc": "产品打光给光位与材质，01 白底给干净底子，03 加强高光与轮廓；三条同为真实摄影语言，可直接叠用。",
        "rule": "保留白底版本的纯背景，不要叠加场景融合条目，否则背景会被二次生成。",
    },
    {
        "name": "品类专用商品图",
        "keywords": ["商品主图", "美妆", "护肤", "珠宝", "手表", "数码", "家电", "家具", "食品", "宠物", "母婴", "运动", "汽车"],
        "main": "zhoubian-10",
        "support": ["zhoubian-11", "zhoubian-13", "zhoubian-12"],
        "desc": "08–20 是按品类写好的专用条目（美妆口红 / 护肤品 / 食品饮料 / 珠宝 / 手表 / 3C / 家电 / 家具 / 家居 / 宠物 / 母婴 / 运动 / 汽车），按品类直接取用，再叠 02 打光。",
        "rule": "一个画面只用一个品类条目，避免材质描述互相冲突。",
    },
    {
        "name": "人物真实感精修",
        "keywords": ["人像", "真实", "精修", "写真", "皮肤"],
        "main": "renwu-3",
        "support": ["renwu-9"],
        "desc": "精修五大词给真实感与无痕处理，EOS R6 条目给相机光学与焦段；合用于人像写真的底子。",
        "rule": "精修条目含多段用途，取用时只取「人物真实感」这一段，不要整段照搬。",
    },
    {
        "name": "日系局部人脸特写",
        "keywords": ["局部", "人脸", "特写", "眼睛", "逆光", "日系"],
        "main": "novelai-6",
        "support": ["novelai-9", "novelai-2"],
        "desc": "06 是可复用风格母版，09 是母版在「半脸枝叶遮挡」下的完整写法，02 提供玻璃水珠折射；三者共用青白高调语汇。",
        "rule": "只用于局部人脸；人物全身或手部入画时，删掉 glossy hair / individual hair strands，避免塑料发与崩手。",
    },
    {
        "name": "海报版式与文字",
        "keywords": ["海报", "版式", "艺术字", "文字", "封面"],
        "main": "yishu-13",
        "support": ["yishu-26", "yishu-2"],
        "desc": "13 是通用转图模板（禁文字），26 给单色印刷制版质感，02 给手写艺术字；版式与字形分开取用。",
        "rule": "13 明确禁文字，需要文字时改用 02/28，不要在同一条里既禁文字又要文字。",
    },
    {
        "name": "巨物尺度场景",
        "keywords": ["巨物", "巨构", "尺度", "压迫感", "宏大"],
        "main": "changjing-7",
        "support": ["changjing-8", "midjourney-14"],
        "desc": "巨构给建筑尺度，科幻概念给荒凉星球巨物，宋代巨莲给自然物的巨物化；核心是「极小人物 + 极大主体」的比例关系。",
        "rule": "尺度靠比例描述与镜头高度实现，不要靠堆「巨大」形容词。",
    },
    {
        "name": "角色三视图资产",
        "keywords": ["三视图", "角色设定", "资产图", "设定图"],
        "main": "midjourney-11",
        "support": ["midjourney-10"],
        "desc": "11 是中文三视图资产图（正面 / 背面 / 头肩），10 是 2.5D 厚涂三视图；前者偏 3D 转 2D 卡通，后者偏厚涂插画。",
        "rule": "两条都是 1:1 方形三栏布局，换角色时锁死「同一角色、同一服装、同一比例」三项。",
    },
    {
        "name": "商品图 + 模特场景",
        "keywords": ["商品主图", "模特", "穿搭", "服装", "上身"],
        "main": "zhoubian-7",
        "support": ["renwu-8", "zhoubian-4"],
        "desc": "05 模特换装负责把衣服穿到人身上，潮流少女条目给真实手机写真质感，02 场景融合把人物放进使用场景。",
        "rule": "换装条目不要与白底条目同时使用；先定场景再定光。",
    },
]


def parse_entries(text):
    """按锚点切片。章节锚点（<a id="midjourney"></a>）也要作为边界，
    否则每个大类最后一条会把下一章整章内容吞进来。"""
    marks = list(re.finditer(r'<a id="([a-z]+)(?:-(\d+))?"></a>', text))
    out = []
    for i, m in enumerate(marks):
        key, num = m.group(1), m.group(2)
        if num is None:
            continue
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        chunk = text[m.end():end].lstrip("\n")
        title = chunk.split("\n", 1)[0].lstrip("# ").strip()
        model = re.search(r'^> 模型：(.+)$', chunk, re.M)
        use = re.search(r'^> 用途：(.+)$', chunk, re.M)
        body = chunk.split("\n", 1)[1] if "\n" in chunk else ""
        out.append({
            "id": "%s-%s" % (key, num),
            "cat": CAT_NAME.get(key, key),
            "title": title,
            "model_line": (model.group(1).strip() if model else ""),
            "use_line": (use.group(1).strip() if use else ""),
            "body": body,
        })
    return out


def detect_model(e):
    m = e["model_line"]
    low = (m + " " + e["body"][:400]).lower()
    if "midjourney" in low or "--ar " in low:
        return "Midjourney"
    if "novelai" in low or "danbooru" in low:
        return "NovelAI"
    if "negative prompt" in low or "illustrious" in low or "stable diffusion" in low:
        return "SD"
    return "通用"


def tag_entry(e):
    """用途只看标题与用途行（正文里的 '室内' 之类会污染）；
    质感与能力可参考正文前 600 字。"""
    hay_use = " ".join([e["title"], e["use_line"]]).lower()
    hay_full = " ".join([e["title"], e["use_line"], e["body"][:600]]).lower()
    result = {g: [] for g in VOCAB}
    for group, rules in RULES.items():
        hay = hay_use if group == "用途" else hay_full
        for tag, kws in rules:
            if any(k.lower() in hay for k in kws):
                if tag not in result[group]:
                    result[group].append(tag)
    result["模型"] = [detect_model(e)]
    # 3D 渲染优先：命中了 3D 渲染就不再挂「真实摄影」，除非正文明确是实拍/照片
    if "3D渲染" in result["质感"] and "真实摄影" in result["质感"]:
        if not any(k in hay_full for k in ("摄影机", "拍摄", "照片", "实拍", "eos", "镜头")):
            result["质感"].remove("真实摄影")
    for group, tags in OVERRIDES.get(e["id"], {}).items():
        if group == "模型":
            result[group] = tags
        elif isinstance(tags, dict):          # {"tags": [...], "replace": True} 整组替换
            result[group] = list(tags["tags"])
        else:
            for t in tags:
                if t not in result[group]:
                    result[group].append(t)
    # 保序：按词表顺序排列，便于阅读与比对
    for group in result:
        order = VOCAB[group]
        result[group] = sorted(set(result[group]), key=lambda x: order.index(x) if x in order else 99)
    return result


def main():
    text = open(MASTER, encoding="utf-8").read()
    entries = parse_entries(text)
    for e in entries:
        e["tags"] = tag_entry(e)
        e.pop("body", None)
        e.pop("model_line", None)

    stats = {}
    for e in entries:
        stats[e["cat"]] = stats.get(e["cat"], 0) + 1

    data = {
        "generated_from": "PROMPT_MASTER.md",
        "count": len(entries),
        "vocab": VOCAB,
        "stats": stats,
        "recipes": RECIPES,
        "entries": entries,
    }
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    lines = []
    lines.append("# 能力索引（Capabilities Index）\n")
    lines.append("> 由 `build_capabilities.py` 从 `PROMPT_MASTER.md` 自动生成，共 **%d 条**。\n"
                 "> 作用：把「库里有几条提示词」变成「库里能干什么」，让 Agent 按**能力**而不是按标题关键词选条目。\n"
                 "> 机读版：`capabilities.json`；检索：`python -X utf8 find.py \"商品主图 真实\"`\n" % len(entries))
    lines.append("---\n")
    lines.append("## 一、词表（固定，不随意新增）\n")
    for group in ["用途", "质感", "能力", "模型"]:
        lines.append("- **%s**：%s" % (group, " · ".join(VOCAB[group])))
    lines.append("")
    lines.append("> 每组可多选；`用途` 描述画面是什么，`质感` 描述它看起来像什么，`能力` 描述它能替你完成哪一步操作，`模型` 决定语法。\n")
    lines.append("---\n")

    lines.append("## 二、联动配方（常见任务 → 条目组合）\n")
    lines.append("| 任务 | 主条目 | 辅条目 | 怎么拼 | 硬约束 |")
    lines.append("|---|---|---|---|---|")
    for r in RECIPES:
        lines.append("| %s | `%s` | %s | %s | %s |" % (
            r["name"], r["main"], "、".join("`%s`" % x for x in r["support"]),
            r["desc"], r["rule"]))
    lines.append("")
    lines.append("> 配方的意义：单条提示词是「整图描述」，不能直接相加。配方规定谁给骨架、谁给光位、谁给材质。\n")
    lines.append("---\n")

    lines.append("## 三、分类统计\n")
    lines.append("| 大类 | 条目数 |")
    lines.append("|---|---|")
    for cat in ["人物", "场景", "构图", "特效", "周边", "艺术", "NovelAI", "Midjourney"]:
        if cat in stats:
            lines.append("| %s | %d |" % (cat, stats[cat]))
    lines.append("| **合计** | **%d** |\n" % len(entries))
    lines.append("---\n")

    lines.append("## 四、全量打标表\n")
    lines.append("| ID | 标题 | 模型 | 用途 | 质感 | 能力 |")
    lines.append("|---|---|---|---|---|---|")
    for e in entries:
        t = e["tags"]
        lines.append("| `%s` | %s | %s | %s | %s | %s |" % (
            e["id"], e["title"].replace("|", "／"),
            "、".join(t["模型"]), "、".join(t["用途"]) or "—",
            "、".join(t["质感"]) or "—", "、".join(t["能力"]) or "—"))
    lines.append("")

    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))

    print("entries: %d" % len(entries))
    print("stats:", stats)
    print("wrote:", os.path.basename(OUT_JSON), os.path.basename(OUT_MD))


if __name__ == "__main__":
    main()
