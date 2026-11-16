# NovelAI / Illustrious 图片逆向：规则与踩坑记录

本文件是 `SKILL.md` 的详细展开。逆向日系 AI 插画时按需查阅。

---

## 0. 先判断模型路线，再决定是否检索 tag

逆向任何图像时，不要仅凭用户说“逆向”就进入 NovelAI / Danbooru tag 工作流，也不要将候选限制在 Midjourney 与 NovelAI。先根据图像的画种、构图、几何一致性、材质与光照反应、笔触和生成瑕疵，比较合理的模型家族：Midjourney / Niji、NovelAI、Stable Diffusion / SDXL（Illustrious、Pony 等）、Flux、GPT Image / DALL·E 等通用图像模型，以及 Blender / Unreal / Octane 等真实 3D 渲染。候选应随图像类型变化，不要求每次穷举所有家族。

明确区分两个问题：

- **来源判断**：原图实际由哪种模型生成。仅凭外观通常无法确认，应给出可见证据、倾向与不确定性。
- **复现路线**：哪个模型最适合按用户目标重做。模型被选为复现路线，不等于它就是原图来源。

只有在目标路线确实适合 Danbooru / SD tag 的日系插画时，才查询本文的 Tensor.Art 索引。摄影使用摄影语言；3D / CG 使用建模、材质、渲染器和物理光照语言；GPT Image / DALL·E / Flux 等路线按自然语言约束组织。不要把一种模型的参数、负面词格式和加权语法照搬到另一种模型。

## 1. 先分清「构件」与「画风」

| 可反推（构件） | 不可反推（画风） |
| --- | --- |
| 主体、人数、动作、姿态 | 线稿粗细与收笔方式 |
| 构图、视角、裁切、宽高比 | 上色层数、渐变柔和度 |
| 光源方向、逆光/侧逆光、色温 | 高光形状（带状 / 点状 / 环状） |
| 场景元素、前景遮挡、粒子 | 皮肤/头发的「材质感」 |
| 配色盘、明暗对比 | 噪点、笔触、厚涂堆叠 |

**画风在底模 / LoRA / finetune 里，不在 tag 里。** 社区里所谓「画师串」反推不出来，原因就在这里。
用户拿提示词出的图与原图质感差很大时，第一反应应当是：
1. 问/判断当前用的底模（NovelAI v3 / Illustrious 系 / Pony / SDXL + 哪些 LoRA）；
2. 建议换到相近底模或加对应 LoRA；
3. 再谈 tag 微调。

**不要**用一堆 `cinematic lighting, ultra detailed, soft shading, delicate lineart` 去"堆出"画风——只会让画面更油、更塑料。

---

## 2. 减法原则（本 skill 最重要的约束）

### 真实翻车案例

用户反馈「头发发质违和、手指容易出错」→ 加了一堆部位质感词和负面词：
- 正向：`soft matte silky hair`、`broad soft highlight bands`、`detailed fingers`
- 负向：`plastic hair, glass hair, waxy hair, malformed fingers, extra fingers`

结果用户反馈：**「头发更加像塑料了，手部也很诡异」**。方案被证伪。

### 为什么

1. SD 的 `negative prompt:` 是 **CFG 负向引导**，不是"屏蔽词表"。写 `plastic hair` 会高频激活 `hair` 这个 token，模型注意力被锁死在头发上。
2. `soft matte silky hair` + `broad soft highlight bands` 本身就是 **3D 渲染 / 塑料材质的签名**，越写越像塑料。
3. `fingers hidden / only fingertips visible` 会逼模型画「残缺的手」，比画错更诡异。
4. 部位词堆得越多，模型越倾向于把它当作必须精细刻画的主体，反而放大缺陷。

### 正确做法

1. **彻底不描述该部位**：不写发质、不写高光形状、不写手指细节。让它作为整体的一部分自然生成。
2. **物理规避**：手出画、被袖口/道具/前景遮挡、改半身裁切、让头发大面积落在画外或被帽子/发饰覆盖。
3. **后期修**：局部 inpaint 重绘手/发，比在提示词里较劲有效得多。
4. **negative 精简到 ≤12 词**，只留全局崩坏项（`lowres, bad anatomy, extra limbs, text, watermark, jpeg artifacts`），**不出现任何具体部位词**。
5. 若必须提，只用一次中性结构词，不加质感形容词。

一句口诀：**某处反复崩，就把那个词从提示词里删掉，而不是加更多词去修它。**

---

## 3. 语法对照（跨模型必须改写）

| 用途 | NovelAI | SD / Illustrious / Pony | Midjourney |
| --- | --- | --- | --- |
| 加权 | `{word}` ≈ ×1.05，`[word]` ≈ ×0.95，`word::1.2` | `(word:1.2)`、`[word]` | `word::2`（语义权重，机制不同） |
| 负面 | `Undesired content:` 段 / `[word]` | 独立 `negative prompt:` 段 | `--no a, b` |
| 质量词 | `masterpiece, best quality` | 同；`score_9` 系列**仅 Pony** | `--hd --raw --p` |
| 画幅 | 靠分辨率 | 靠分辨率 | `--ar 9:16` 等 |
| 分隔符 | 逗号 tag 串 | 逗号 tag 串 | 自然语言短语 |

**注意**：`score_9, score_8_up, ...` 是 Pony Diffusion 专用质量分桶，混进 Illustrious / NovelAI 提示词会污染画面。
Midjourney 的 `--ar --hd --raw --p` 在 SD/NAI 里无效；SD 的 `negative prompt:` 在 MJ 里要改写成 `--no`。

**MJ 审核坑**：即使写在 `--no` 里，`human breasts / bikini / exposed skin` 等词仍可能触发内容审核。删除性化/裸露词，用「成年 + 完整着装」正向描述，负面只留画风/结构类词。

---

## 4. Tensor.Art 文章 → 构件速查

索引里可直接用 `--article <id>` 或 `--topic` 找到的高价值文章（标题为站点原文）：

| 需求 | 文章 |
| --- | --- |
| 通用风格 tag / 视角 / 光效 | `Some prompts I've collected 一些我收藏的提示词`（中英对照，含 Stylization / View 分区） |
| 发型 | `Prompting: Hairstyles`、`Prompting: Hair Styles (Fem+Male)`、`HairStyle Prompts Sharing - AIの髪のプロンプト集 - 发型提示词分享`、`Prompting: Male Hairstyles`、`Prompting: Hair Coloring` |
| 手部 / 手势 | `Gesture Prompts Sharing🫶 - AIの手のプロンプト集 - 手部提示词分享` |
| 姿势（Danbooru tag） | `Posture Tag Study Results (Tags from Danbooru)`、`Dual-character Action Prompts Sharing - 二人用アクションprompts` |
| 光影 | `Prompting: Lighting`、`Prompt reference for "Lighting Effects"` |
| 眼睛 | `Prompting: Eyes. Colors, Shapes & More`、`Prompting: Eyes (Part 1)` |
| 皮肤 / 质感标记 | `Prompting: Skin Colors, Conditions, Types, Marks and Scars` |
| 背景 | `Prompting: Backgrounds` |
| 视角 / 构图 | `Prompting: Perspectives` |
| 表情 | `Sharing expressions prompts`、`Prompting: Facial Expressions`、`Beginner Guide for Prompts (Lesson 1 Emotions)` |
| 负面词 | `Negative Prompts` |
| 权重语法 | `Understanding the Use of Parentheses in Prompt Weighting for Stable Diffusion` |
| 质量分桶（Pony） | `Understanding Score_9, Score_8_Up, Score_7_Up, Score_6_Up, Score_5_Up, Score_4_Up` |
| 服饰 | `Prompting: Clothing series Vol. 1 - Headwear`、`Prompting: Fashion Styles`、`Prompting: Traditional Clothing` |
| 人鱼 / 亚人 | `Prompting: Merfolk`、`Sharing Demihuman prompts` |
| 身体部位中文对照 | `绘图提示词整理：第一章｜常用身体部位与表情关键词` |
| 工作流 | `ControlNet: Openpose adapter`、`ControlNet: QR Code adapter`、`How to create Lora (Basic version)` |

**重要**：这些文章里常标注测试底模（例如某手势篇写明 `The tested Model is ✨🎨Illustrious - AnimeMaster✨`）。
这条信息通常比文章里的 tag 更值钱——它直接告诉你该用什么模型，务必单独提取给用户。

---

## 5. 图片定性清单（Step 1 展开）

逐项写下来，再决定检索哪些词：

1. **画种**：日系半写实插画 / 2.5D 厚涂 / 平涂赛璐璐 / 真人摄影 / 3D CG 静帧 / 水墨
2. **画幅**：9:16 竖版 / 1:1 / 16:9；是否满屏、是否有留白
3. **主体**：人数、身份、年龄感、发色发长、服饰、关键道具
4. **动作与视线**：朝向、身体扭转、手部位置、是否看镜头
5. **构图**：景别（胸像/半身/全身）、机位、前景遮挡、对称或偏移
6. **光**：主光方向、逆光/侧逆光、体积光、叶影、边缘光、色温
7. **色盘**：主色 3–5 个、饱和度、冷暖关系
8. **介质与特效**：玻璃/水/纱、折射、粒子、光斑、散景
9. **画风签名**：线稿有无、上色层数、高光形状、笔触/噪点
10. **易崩部位**：长发、手、眼睛、复杂服饰结构 —— 这些直接走减法原则

---

## 6. 交付格式（用户长期偏好，硬性）

- **每组提示词一个独立代码块，组内完全自包含**。禁止「沿用上方母版」「同上，仅替换 X」「请自行拼接」。
- 只交付一份时也用单独代码块。
- 每组开头标注所属模型（NovelAI / Stable Diffusion / Illustrious / Midjourney / GPTimage 等），必要时附 `negative prompt:` 独立段。
- Midjourney 提示词**末尾必须带完整参数串**：
  - 竖版 `--ar 9:16 --hd --raw --p`
  - 方形三视图 `--ar 1:1 --hd --raw --p`
  - 横版 `--ar 16:9 --hd --raw --p`
  - `--hd --raw --p` 三项必须随 `--ar` 一起写全
- 多组提示词之间用简短中文说明隔开，不要堆叠代码块。
- 附一句底模 / LoRA 建议与"哪些差异不是 tag 能解决的"。
- 用户说「不要推送到 GitHub」时，只交付内容，不动 `prompt-library` 仓库。

---

## 7. 站点与索引技术备注

- `https://tensor.art/articles` 在部分代理下返回 `502 CONNECT tunnel failed`；抓取统一用 `https://tensorart.me/articles`（同一站点镜像，Nuxt SSR 结构一致）。
- 页面是 **Nuxt 3 SSR**，`__NUXT_DATA__` 用 devalue 序列化成**扁平数组**，容器里的整数都是指向其他元素的索引；负数索引是 `undefined/NaN/Infinity` 等哨兵值。`payload_root()` 负责还原。
- 文章列表数据在 `$svue-query.queries[2].state.data.pages[0].items`，每篇含 `id / title / content(HTML 全文) / publishedAt / statisticsInfo / cover / creator`。
- vue-query 的 `queryKey` 是 `["articles", {"sort":"MOST_LIKE","visibility":"FLAW","activeTag":"all"}]`，`pages[0]` 有 `cursor:"40"`、`hasMore:true`。**SSR 只预取第一页**，`?cursor=40` 不会翻页；`?sort=LATEST` 会返回另一批 40 篇，两批合并去重约 79 篇。
- `?tag=prompt`、`?sort=MOST_READ` 会 500，不要作为默认批次。
- 正文 HTML 转纯文本时按 `<br>/<p>/<li>/<h*>` 换行，基本能做到「一行一个 tag」，这也是检索以**行**为单位打分的原因。
- 索引文件 `assets/index.json`（含 `text` 全文）与 `assets/articles/<id>.txt`（单篇纯文本），均可用常规文本工具直接 grep。
