# -*- coding: utf-8 -*-
import re, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.hyperlink import Hyperlink

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "PROMPT_MASTER.md")

cat_map = {
    "renwu": "人物", "changjing": "场景", "goutu": "构图",
    "texiao": "特效", "zhoubian": "周边", "yishu": "艺术",
}
fallback = {
    "人物": "角色设定 / 人像精修 / 人物渲染",
    "场景": "环境 / 地点 / 场景类视觉",
    "构图": "镜头 / 分镜 / 版式 / 信息图",
    "特效": "光效 / 能量 / 法术特技",
    "周边": "商品化 / 纪念品 / 周边",
    "艺术": "插画风 / 艺术字 / 艺术海报",
}

text = open(MASTER, encoding="utf-8").read()
lines = text.split("\n")

entries = []
cat = None
cur = None

def finalize():
    global cur
    if cur is not None:
        # 从正文抽取「风格/用途」
        usage_parts = []
        for bl in cur["body"].split("\n"):
            s = bl.strip()
            if s.startswith(">"):
                inner = re.sub(r'^>\s*', '', s).strip()
                if re.search(r'(用途|风格|适用|使用说明)', inner):
                    usage_parts.append(inner)
        usage = "；".join(usage_parts) if usage_parts else fallback[cur["cat"]]
        entries.append((cur["cat"], cur["title"], usage, cur["body"].strip(), cur["src"]))
        cur = None

i, N = 0, len(lines)
while i < N:
    line = lines[i].strip()
    m = re.match(r'<a id="([^"]+)"></a>', line)
    if m:
        aid = m.group(1)
        if aid in cat_map:
            finalize()
            cat = cat_map[aid]
        elif re.match(r'[a-z]+-\d+', aid):
            finalize()
            j = i + 1
            while j < N and not lines[j].startswith("### "):
                j += 1
            title = lines[j].replace("### ", "", 1).strip() if j < N else ""
            src = ""
            sm = re.search(r'（原\s*(.+?)\s*）', title)
            if sm:
                src = sm.group(1)
                title = title[:title.index("（原")].strip()
            k = j + 1
            buf = []
            while k < N and not re.match(r'<a id="', lines[k].strip()):
                buf.append(lines[k])
                k += 1
            cur = {"cat": cat, "title": title, "body": "\n".join(buf), "src": src}
        i += 1
        continue
    i += 1
finalize()

wb = Workbook()
idx = wb.active
idx.title = "索引"
idx["A1"] = "提示词库总表（Excel 导出）"
idx["A1"].font = Font(bold=True, size=14)
idx["A2"] = "共 6 大类。点击「前往」可跳转到「提示词」页对应大类；「提示词」页可按列筛选。"
idx["A2"].font = Font(italic=True, color="555555")
idx.append([])
idx.append(["大类", "条目数", "前往"])
hr = idx.max_row
for c in range(1, 4):
    cell = idx.cell(row=hr, column=c)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="305496")
    cell.alignment = Alignment(horizontal="center")

ws = wb.create_sheet("提示词")
cols = ["序号", "大类", "条目", "风格/用途", "提示词内容", "来源"]
ws.append(cols)
for c in range(1, len(cols)+1):
    cell = ws.cell(row=1, column=c)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="305496")
    cell.alignment = Alignment(horizontal="center", vertical="center")

thin = Side(style="thin", color="D9D9D9")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

row = 2
seq = 1
first_row = {}
counts = {}
for cname in ["人物", "场景", "构图", "特效", "周边", "艺术"]:
    first_row[cname] = row
    cnt = 0
    for (ecat, etitle, eusage, ebody, esrc) in entries:
        if ecat != cname:
            continue
        cnt += 1
        ws.cell(row=row, column=1, value=seq)
        ws.cell(row=row, column=2, value=ecat)
        ws.cell(row=row, column=3, value=etitle)
        ws.cell(row=row, column=4, value=eusage)
        ws.cell(row=row, column=5, value=ebody)
        ws.cell(row=row, column=6, value=esrc)
        for c in range(1, 7):
            cell = ws.cell(row=row, column=c)
            cell.border = border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
        row += 1
        seq += 1
    counts[cname] = cnt
    ws.auto_filter.ref = f"A1:F{row-1}"

link_font = Font(color="0563C1", underline="single")
for cname in ["人物", "场景", "构图", "特效", "周边", "艺术"]:
    r = idx.max_row + 1
    idx.cell(row=r, column=1, value=cname)
    idx.cell(row=r, column=2, value=counts[cname])
    cell = idx.cell(row=r, column=3, value="前往")
    link = Hyperlink(ref=f"C{r}", location=f"提示词!A{first_row[cname]}", display="前往")
    cell.hyperlink = link
    cell.font = link_font
    cell.alignment = Alignment(horizontal="center")

widths = {"A": 6, "B": 8, "C": 30, "D": 38, "E": 95, "F": 22}
for col, w in widths.items():
    ws.column_dimensions[col].width = w
idx.column_dimensions["A"].width = 12
idx.column_dimensions["B"].width = 10
idx.column_dimensions["C"].width = 12

ws.freeze_panes = "A2"
idx.freeze_panes = "A5"

out = os.path.join(BASE, "提示词库总表.xlsx")
wb.save(out)
print("saved:", out)
print("total entries:", len(entries))
print("per category:", counts)
