# 提示词库 · Prompt Library

![prompts](https://img.shields.io/badge/prompts-105-orange)
![content](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey)
![code](https://img.shields.io/badge/code-MIT-blue)

一套 AI 图像 / 视频生成提示词的开源集合。按 **人物 / 场景 / 构图 / 特效 / 周边 / 艺术** 六大类组织，正文原样保留，不翻译、不总结、不改写。

**共 95 条。**

| 大类 | 条数 | 里面是什么 |
|---|---|---|
| 人物 | 17 | 脸模、人像写真、角色渲染、角色涂鸦 |
| 场景 | 8 | 环境、分镜、巨构、视频分镜脚本 |
| 构图 | 5 | 景别、版式构成、图生提示词 |
| 特效 | 1 | 仙侠人物特效（35 例） |
| 周边 | 22 | 电商商品图全体系，白底到各品类专用 |
| 艺术 | 42 | 插画风、艺术字、海报转译、剧情海报 |

艺术类占得最多，因为它最难标准化：人像和商品图的套路是收敛的，海报每次都得重新搭骨架。

---

## 快速开始

克隆下来，三种用法，按需要挑一种。

```bash
git clone https://github.com/Nihilist-ZIO/prompt-library.git
cd prompt-library
```

**① 直接用**
打开对应的 `cat_*.md`，找到条目，复制正文。

**② 快速找**
打开 `PROMPT_MASTER.md`，六大类合并在一个文件里，顶部有总目录、每个大类下有条目子目录，全部是 `#锚点` 跳转。

**③ 筛选**
打开 `提示词库总表.xlsx`。「索引」页看六大类分布，点「前往」跳到「提示词」页对应大类；「提示词」页有「大类 / 风格用途」列，开了自动筛选。

---

## 目录结构

```
prompt-library/
├── PROMPT_INDEX.md        总入口：六大类导航与用法说明
├── PROMPT_MASTER.md       单文件总表（95 条 · 锚点跳转）
├── 提示词库总表.xlsx        Excel 分享版（索引页 + 提示词页 · 可筛选）
├── cat_人物.md            17 条
├── cat_场景.md            8 条
├── cat_构图.md            5 条
├── cat_特效.md            1 条
├── cat_周边.md            22 条
├── cat_艺术.md            42 条
├── 配色库.md              跨项目配色参考
├── 技能联动组合技.md       组合用法示例
├── 归档日志.md            增改记录与维护纪律
├── build_xlsx.py          从总表锚点重建 Excel
├── archive_batch.py       批量入库脚本（含查重）
└── by-detail/             20 个最早的单文件版本，备查
```

## 依赖

只用 Python 标准库 + `openpyxl`。

```bash
pip install openpyxl
python -X utf8 build_xlsx.py
```

输出应为 `total entries: 95`。如果对不上，说明某处没同步，别急着提交。

---

## 怎么往里加词条

不要直接改 `PROMPT_MASTER.md`，它是合并产物。改源文件，然后按顺序同步：

1. 写进对应 `cat_*.md`，条目用 `## 标题`，正文原样，末尾加 `---`
2. 同步 `PROMPT_MASTER.md`：正文 + 该大类顶部子目录加一条 `- [标题](#大类-N)`
3. 同步 `PROMPT_INDEX.md`：条目总数 + 「六大类一览」里的条数与包含内容
4. 重跑 `python -X utf8 build_xlsx.py`
5. **读回校验**：新条目数必须与 `PROMPT_INDEX.md` 声明的一致
6. **查重**：正文去掉空白与标点后做 `difflib.SequenceMatcher`，相似度 > 0.9 视为重复，不入库

### 两条血泪教训

**① 入库不能追加到文件末尾。**
`PROMPT_MASTER.md` 是按大类分章节的，条目归属由它所在的章节决定。追加到文末 = 全部变成最后一个大类。正确做法是插到「下一个大类锚点」之前，只有末类艺术才追加文末。

**② 只校验总数会漏掉分布错误。**
总数对、分布全错，是最隐蔽的一类错。必须额外看 `build_xlsx.py` 输出的 `per category`，并检查每个条目锚点是否落在自己大类的章节区间内。

用 `archive_batch.py` 可以省掉手工同步：把新条目写进根目录一个 `_new_*.py`（格式见 `archive_batch.py` 顶部注释），先跑 `python -X utf8 archive_batch.py` 预演查重，确认后加 `--write` 写盘，再重跑 `build_xlsx.py`。

---

## 说明

- 正文均为原样保留，包含原作者的措辞、标点习惯，甚至有重复逗号这类原文瑕疵，不代为修润。
- `by-detail/` 是最早整理的 20 个细粒度单文件，未并入六大类，留作备查。
- 计数以 `build_xlsx.py` 为准（按锚点计 95 条）。同目录的 `PROMPT_MASTER.xlsx` 若存在，是按 `###` 子块计的另一口径，数值更大，两者不要互相参照。

## 许可

本项目采用**双许可**，内容和代码分别适用不同协议：

| 范围 | 文件 | 协议 | 你能做什么 |
|---|---|---|---|
| 提示词内容 | `*.md`、`*.xlsx` | **CC BY 4.0** | 随便用、随便改、可以商用，**署名即可** |
| 代码 | `*.py` | **MIT** | 随便用，保留版权声明即可 |

- 完整法律文本：[`LICENSE-CONTENT`](LICENSE-CONTENT)（CC BY 4.0，适用于 `*.md` / `*.xlsx`）、[`LICENSE`](LICENSE)（MIT，**仅**适用于 `build_xlsx.py` 与 `archive_batch.py`）
- 注：`LICENSE` 保持 MIT 标准原文未加任何附注，以便 GitHub 正确识别协议；适用范围以上表为准。
- 署名方式：注明「作者：阿金（Nihilist-ZIO）」，并附上本仓库链接即可，不必另行申请授权。
- 说明：单条提示词的可版权性本身存在争议（过短或纯功能性的描述可能不构成作品）。这里的协议主要作用是**表明意图、约束搬运、让使用者敢用**，不是一纸能打赢官司的武器。

## 贡献

欢迎提 PR 或 issue。新增词条请按上面的六步走，并跑一遍查重——**重复的创意不值得占一个位置，但重复的写法值得合并。**
