# 提示词库 · Prompt Library

![prompts](https://img.shields.io/badge/prompts-124-orange)
![content](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey)
![code](https://img.shields.io/badge/code-MIT-blue)

一套 AI 图像 / 视频生成提示词的开源集合。按 **人物 / 场景 / 构图 / 特效 / 周边 / 艺术 / NovelAI / Midjourney** 八大类组织，正文原样保留，不翻译、不总结、不改写。

**共 124 条。**

---

## 这个库想做什么

**让普通人也能做出自己想要的那张图。**

库本身没什么厉害的，它只是提供一条学习路径：别人踩过的坑、验证过的写法、哪些词有用、哪些词会把画面带偏，都记在这里。

喜欢的朋友尽管订阅，长期维护。

**粉丝群：687805177**

一把剑本身是平平无奇的，但勇者拿上它，它就是圣剑。屏幕前的朋友，这个库也是如此。

---

| 大类 | 条数 | 里面是什么 |
|---|---|---|
| 人物 | 18 | 脸模、人像写真、角色渲染、角色涂鸦、角色资产图、Cosplay 影棚写真 |
| 场景 | 8 | 环境、分镜、巨构、视频分镜脚本 |
| 构图 | 5 | 景别、版式构成、图生提示词 |
| 特效 | 1 | 仙侠人物特效（35 例） |
| 周边 | 22 | 电商商品图全体系，白底到各品类专用 |
| 艺术 | 42 | 插画风、艺术字、海报转译、剧情海报 |
| NovelAI | 9 | NovelAI / Danbooru tag 系提示词、日系插画逆向产物与风格母版 |
| Midjourney | 19 | 超真实AIGC 系列、2.5D 三视图、游戏风CG人物资产图、MJ 风格码；2026-11-16 新增螺钿白虎、宋代巨莲、满月修补、策马逐羊、林中蓝熊、宋代女帝、3D CGI 半身像；少数历史原文保留 `negative prompt:` 行，非 MJ 原生语法，使用时需改写 |

艺术类占得最多，因为它最难标准化：人像和商品图的套路是收敛的，海报每次都得重新搭骨架。

---

## 快速开始

克隆下来，**三种用法**，按需要挑一种。

```bash
git clone https://github.com/Nihilist-ZIO/prompt-library.git
cd prompt-library
```

### 用法 A：直接取用现成提示词

打开对应文件，找到条目，复制正文即可（正文原样保留，不改不译）。

- **`cat_*.md`**：分类源文件，最直接的取词入口
- **`PROMPT_MASTER.md`**：八大类合并在一个文件里，顶部有总目录、每个大类下有条目子目录，全部是 `#锚点` 跳转
- **`提示词库总表.xlsx`**：「索引」页看八大类分布，点「前往」跳到「提示词」页对应大类；「提示词」页有「大类 / 风格用途」列，开了自动筛选

### 用法 B：让 AI Agent 依据本库生成你想要的提示词

把整个仓库（或本目录路径）交给 AI Agent，用自然语言描述你想要的画面，让 Agent 检索库内相关词条，复用其中的风格语法、结构骨架与约束写法，产出一份**全新的、可直接复制的完整提示词**。适合：换主题 / 换场景、把某条风格迁移到别的对象、跨词条组合、按目标模型重写参数。

给 Agent 的说明建议写清三点：

1. **先做模型判断**：未指定模型时，先根据画种、渲染管线、构图能力、材质与可见生成痕迹，比较 Midjourney / Niji、NovelAI、Stable Diffusion / SDXL / Illustrious / Pony、Flux、GPT Image / DALL·E、Blender / Unreal / Octane 等合理候选；区分“原图来源推断”和“可复现路线”，说明依据与不确定性后再选语法。已指定模型时，才按该模型输出。
2. **语法不能混用**：MJ 用 `--ar --hd --raw --p` 参数后缀，NAI 用 `{}` / `[]` 与 `Undesired content:`，SD 用 `(word:1.2)` 与独立 `negative prompt:`，GPT Image / DALL·E / Flux 使用自然语言约束；不同模型不得直接套用另一模型的参数。
3. **输出形态**：多组提示词每组独立代码块、每组完全自包含，不要写「沿用上方」让用户手动拼接。
3. **库的边界**：库内正文只作参考，**不得擅自改写原文**；新产出的提示词要入库，走下面的「怎么往里加词条」流程。

### 用法 C：让 AI Agent 用 Tensor.Art 语料检索构件 tag

仓库内附 `skills/novelai-tensorart-reverse/`：Tensor.Art 开源提示词文章的**本地全文索引**（79 篇 / 3394 行 tag）+ 离线检索脚本 + 逆向规则。适合逆向 NovelAI / Illustrious 系日系插画，或补某一类构件词（发型 / 手部 / 光影 / 姿势 / 眼睛 / 负面词 / 权重语法）。

```bash
cd skills/novelai-tensorart-reverse
python scripts/search.py hair backlight hand --limit 5
python scripts/search.py "头发 逆光 手部" --topic hair
python scripts/search.py --topic negative --lines 20
python scripts/build_index.py --refresh          # 拉最新文章
```

**边界**：它只提供构件级 tag，**不负责画风**。画风由底模 / LoRA / finetune 决定；索引里查不到 `light particles / caustics / lens flare` 这类质感词。详见 `skills/novelai-tensorart-reverse/references/reverse_rules.md`。

> 本机生效副本在 `~/.workbuddy/skills/novelai-tensorart-reverse/`（WorkBuddy 会自动加载）；仓库这份是可移植 / 版本管理的副本，改动记得两边同步。

### 用法 D：按能力检索与联动组合

`capabilities.json` + `CAPABILITIES.md` 是**能力索引层**：把全库条目按固定词表打标（用途 / 质感 / 能力 / 模型），并给出常见任务的联动配方。它解决的是「库里有几条」到「库里能干什么」的断层——按能力选条目，而不是按标题关键词猜。

```bash
python -X utf8 find.py "商品主图 真实"
python -X utf8 find.py "局部人脸 逆光" --limit 5
python -X utf8 find.py --tag 商品主图 --cat 周边
python -X utf8 build_capabilities.py      # 增删条目后重建索引
```

**配方**规定谁给骨架、谁给光位、谁给材质，并写明硬约束。例如「新品商品主图」= `zhoubian-2`（产品打光）+ `zhoubian-3`（白底）+ `zhoubian-5`（光效）；「日系局部人脸特写」= `novelai-6`（母版）+ `novelai-9`（完整写法）+ `novelai-2`（玻璃折射）。

**三条联动纪律**：① 跨条目拼接必须先统一到目标模型语法，MJ 的 `--ar` 不能混进 NAI；② 一个画面只用一个品类/背景条目，避免材质描述互相打架；③ 部位反复崩的条目按减法原则只取风格段，不整段照搬。

> 四种用法不冲突：A 拿现成的，B 让 Agent 基于现成的长新的，C 给 B 补真实构件 tag，D 让 B 按能力选条目并组合。

---

## 使用指引：来提需求时给我什么、怎么说

这一节服务于**用法 B / C**。给的信息越准，产出的提示词越能直接拿去用。

### 一、需要给我什么图

| 情况 | 要给什么 | 为什么 |
|---|---|---|
| 想复刻一张图 | **原始图**：原尺寸、未压缩、未拼接，不要截屏或二次转发的小图 | 压缩会丢线稿、笔触、高光形状，而这些恰恰是判断画种的依据 |
| 想复刻一整套风格 | **同风格 3–9 张**，最好覆盖不同场景 / 景别 | 单张容易把偶然元素当成风格签名；多张才分得出「稳定特征」和「这张特有」 |
| 出图不对、要继续改 | **原图 + 你用上一版提示词生成的失败图**，两张一起给 | 只说「质感不对」无法定位；对比图能判断是底模差异还是 tag 问题 |
| 有明确参考来源 | 原帖链接 / 原始提示词 / 作者标注的底模 | 逆向时可直接取真实 tag，少靠猜 |

尽量一并附上：

- **底模 / LoRA 名称**（NovelAI / Illustrious / Pony / SDXL / Midjourney v8 等）——画风主要由它决定；
- **生成参数**（CFG、采样器、hires denoise、画幅），排查出图差异时很有用；
- 图里有文字 / 水印 / 拼贴边框时，说明是否要保留。

### 二、该怎样提要求

一句话模板：

> **目标模型 + 想要什么 + 给哪些图 + 优先级 + 输出形态 + 是否入库**

具体写清 6 项：

1. **模型判断与语法**：未指定模型时先判断画种与生成管线，比较 MJ / Niji、NovelAI、SDXL / Illustrious / Pony、Flux、GPT Image / DALL·E、Blender / Unreal / Octane 等候选，区分原图来源与复现路线并标注依据和置信度；确定路线后再使用对应语法。MJ 用 `--ar --hd --raw --p`，NAI 用 `{}`、`[]` 与 `Undesired content:`，SD 用 `(word:1.2)` 与独立 `negative prompt:`，GPT Image / DALL·E / Flux 用自然语言约束，不得混用。
2. **目标**：复刻 / 换场景 / 换色盘 / 换角色 / 只补某类构件（发型、手部、光效）。「一比一复刻」和「借这个感觉画别的」是两种活。
3. **画幅与用途**：9:16 竖版壁纸、1:1 三视图、16:9 横版、商品主图……用途会直接影响构图词。
4. **优先级与禁区**：哪些必须准（角色脸、服装结构、配色），哪些可以放松；哪些部位容易崩（长发 / 手 / 眼），是否允许用裁切或遮挡规避。
5. **输出形态**：要几组；多组时每组独立代码块、组内完全自包含，不写「沿用上方」。
6. **是否入库 / 推送**：明确说「归档」「不要推送 GitHub」；没说就只交付内容，不动仓库。

### 三、三个常见误区

- **只给一张压缩小图，要求「一比一」**：能反推构图与主体，反推不了线稿、上色层数与高光形状——那些在底模里。
- **换了模型却要求同样质感**：跨模型要改写语法，还要换 / 加对应 LoRA，单靠提示词补不回来。
- **部位反复崩就一直加词**：头发、手越描越糟。正确做法是减法——不描述该部位、裁切出画或遮挡、后期 inpaint；`negative prompt:` 控制在 12 词内且不出现部位词。

---

## 目录结构

```
prompt-library/
├── PROMPT_INDEX.md        总入口：八大类导航与用法说明
├── PROMPT_MASTER.md       单文件总表（124 条 · 锚点跳转）
├── 提示词库总表.xlsx        Excel 分享版（索引页 + 提示词页 · 可筛选）
├── cat_人物.md            18 条
├── cat_场景.md            8 条
├── cat_构图.md            5 条
├── cat_特效.md            1 条
├── cat_周边.md            22 条
├── cat_艺术.md            42 条
├── cat_NovelAI.md         9 条
├── cat_Midjourney.md     19 条
├── CAPABILITIES.md        能力索引（打标表 + 联动配方）
├── capabilities.json      能力索引机读版（find.py 的数据源）
├── skills/                AI Agent 技能包（Tensor.Art 语料索引 + 检索脚本 + 逆向规则）
│   └── novelai-tensorart-reverse/
├── 配色库.md              跨项目配色参考
├── 技能联动组合技.md       组合用法示例
├── 归档日志.md            增改记录与维护纪律
├── build_xlsx.py          从总表锚点重建 Excel
├── build_capabilities.py  从总表锚点重建能力索引
├── find.py                按能力检索条目与配方
├── archive_batch.py       批量入库脚本（含查重）
└── by-detail/             20 个最早的单文件版本，备查
```

## 依赖

只用 Python 标准库 + `openpyxl`。

```bash
pip install openpyxl
python -X utf8 build_xlsx.py
```

输出应为 `total entries: 124`。如果对不上，说明某处没同步，别急着提交。

---

## 怎么往里加词条

不要直接改 `PROMPT_MASTER.md`，它是合并产物。改源文件，然后按顺序同步：

1. 写进对应 `cat_*.md`，条目用 `## 标题`，正文原样，末尾加 `---`
2. 同步 `PROMPT_MASTER.md`：正文 + 该大类顶部子目录加一条 `- [标题](#大类-N)`
3. 同步 `PROMPT_INDEX.md`：条目总数 + 「八大类一览」里的条数与包含内容
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
- **【永久禁令】** 会话历史里提取的 92 组 Midjourney 提示词候选（本地备查文件 `_batches/20261115/mj_history_candidates.md`）**永远不入库、永远不推送 GitHub**；`.gitignore` 有目录级与文件名级双重兜底。本库收录的 MJ 提示词仅 `cat_Midjourney.md` 中的 12 条。
- `by-detail/` 是最早整理的 20 个细粒度单文件，未并入八大类，留作备查。
- 计数以 `build_xlsx.py` 为准（按锚点计 124 条）。同目录的 `PROMPT_MASTER.xlsx` 若存在，是按 `###` 子块计的另一口径，数值更大，两者不要互相参照。
- `skills/` 内的脚本与索引随仓库版本管理；WorkBuddy 实际加载的是 `~/.workbuddy/skills/` 下的同名副本。

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
