# NovelAI 提示词集

> 本类收纳 NovelAI / Danbooru tag 系提示词与日系插画逆向产物，正文原样保留，不翻译不改写。
> 每条顶部 `> 模型：` 标注**实际语法**：NAI 用 `{word}` / `[word]` 与 `Undesired content:`，SD 系用 `(word:1.2)` 与独立 `negative prompt:`，两者不可混写。
> 分类依据为**语料体系**（NovelAI / Illustrious 系日系插画 tag），不是严格按语法划分；少数条目为 SD 格式，已在元信息中注明。


## 晨雾林间·叶影光斑俯视特写（NovelAI · Undesired content）

> 模型：NovelAI（`{word}` / `[word]` 加权，`Undesired content:` 负面段）
> 用途：日系高精细半写实插画 · 晨雾林间俯视特写；银蓝发少女、逆光叶影、高调青蓝白。
> 来源：2026-11-15 小黑盒 807972cf5ffa 逆向收尾交付。

masterpiece, best quality, absurdres, 1girl, solo, silver-blue hair, blunt bangs,
Dynamic hair, blue eyes, white dress, from above, high angle, close-up,
looking at viewer, {Volumetric lighting}, {Natural lighting}, Backlit,
motion_blur, bokeh, depth of field, blurry foreground of leaves,
dawn, light specks only among the leaves, [detailed background],
pale cyan and white palette
Undesired content: lowres, bad anatomy, extra limbs, text, watermark, jpeg artifacts, worst quality

---

## 雨后玻璃窗·水珠折射侧脸（NovelAI · Undesired content）

> 模型：NovelAI（`{word}` / `[word]` 加权，`Undesired content:` 负面段）
> 用途：日系高精细半写实插画 · 雨后玻璃窗侧脸；水珠折射、逆光、高调青蓝白。
> 来源：2026-11-15 小黑盒 807972cf5ffa 逆向收尾交付。

masterpiece, best quality, absurdres, 1girl, solo, silver-blue hair, blunt bangs,
high ponytail, hair ribbon, blue eyes, mole under eye, white off-shoulder dress,
side view, bust shot, head tilt, looking away, {Backlit}, {High-key lighting},
Practical Lighting, bokeh, depth of field, blurry foreground,
rain droplets only on the window glass, refraction only inside the droplets,
tiny light specks only in the background air, [detailed background],
soft cyan and white palette
Undesired content: lowres, bad anatomy, extra limbs, text, watermark, jpeg artifacts, worst quality

---

## 暖橙红舞狮·迎光特写（negative prompt 版）

> 模型：Stable Diffusion / Illustrious 系（`negative prompt:` 段；**非 NovelAI 语法**）
> 用途：暖橙红异角色反例 · 迎光特写；同一画风下的暖色盘变体。
> 来源：2026-11-15 小黑盒 807972cf5ffa 逆向收尾交付。

masterpiece, best quality, 1girl, solo, brown hair, straw hat, amber eyes,
red festive outfit, close-up, looking at viewer, Warm lighting, Hard light,
red theme, Practical Lighting, golden sparks only in the background, bokeh,
depth of field, warm orange and crimson palette
negative prompt: lowres, bad anatomy, extra limbs, text, watermark, jpeg artifacts, worst quality

---

## 青蓝水折射·草帽窗边仰视（negative prompt 版）

> 模型：Stable Diffusion / Illustrious 系（`negative prompt:` 段；**非 NovelAI 语法**）
> 用途：青蓝水折射 · 草帽窗边；玻璃与水面折射、气泡、体积光、高调青蓝白。
> 来源：2026-11-15 小黑盒 807972cf5ffa 逆向收尾交付。

masterpiece, best quality, 1girl, solo, silver-blue hair, blunt bangs, straw hat,
blue eyes, white summer dress, three-quarter view, medium shot, sitting by a window,
Backlit, Volumetric lighting, Colorful lighting, Reflection, refraction only inside
the glass and water surface, transparent bubbles in blurry foreground, bokeh,
depth of field, high-key cyan and white palette, tiny light specks only in the air
negative prompt: lowres, bad anatomy, extra limbs, text, watermark, jpeg artifacts, worst quality

---

## 樱花树下·捧发光玻璃球（negative prompt 版）

> 模型：Stable Diffusion / Illustrious 系（`negative prompt:` 段；**非 NovelAI 语法**）
> 用途：樱花树下捧发光玻璃球；前景樱枝与风铃虚化、逆光、粉白高调。
> 来源：2026-11-15 小黑盒 807972cf5ffa 逆向收尾交付。

masterpiece, best quality, 1girl, solo, silver-blue hair, blunt bangs, high ponytail,
pink ribbon hair ornament, blue eyes, mole under eye, white kimono with red collar,
sideways/profile view, bust shot, looking down, holding a glowing glass orb in front
of her chest, wrists covered by wide sleeves, cherry blossom branches and wind chimes
in blurry foreground, Backlit, High-key lighting, Practical Lighting, bokeh,
depth of field, refraction only inside the glass orb, tiny light specks only in the
background air, soft pink and white palette
negative prompt: lowres, bad anatomy, extra limbs, text, watermark, jpeg artifacts, worst quality

---

## 日系高精细逆光厚涂·风格 tag 母版（早期版）

> 模型：通用 Danbooru tag 串（无负面段）
> 用途：小黑盒 807972cf5ffa 那组图的**风格母版**，记录逆向时用到的全部质感词；主力用于**局部人脸 / 眼部特写**类画面。
> ✅ 入库状态：2026-11-16 用户确认**可入库**，正式作为风格母版条目使用。
> ⚠ 用法边界：`glossy hair` / `individual hair strands` / `subsurface scattering` / `caustics` 为裸材质词，人物全身或手部入画时实测易把头发画成塑料、手部崩坏；用于局部人脸时风险低，若要人物入画则按「减法原则」裁切或遮挡这些部位。
> 来源：2026-11-15 用户提供；正文原样保留。

masterpiece, best quality, ultra-detailed, extremely detailed, absurdres, highres, delicate face, highly detailed eyes, intricate iris, multiple eye highlights, glossy hair, individual hair strands, fine lineart, soft painterly gradients, backlighting, volumetric lighting, dappled sunlight, leaf shadows, rim light, lens flare, rainbow flare, sparkling particles, floating light dots, translucent glass, water droplets, refraction, caustics, subsurface scattering, high-key lighting, cyan and white color grading, pastel accents, soft contrast, foreground foliage, depth of field, bokeh, cinematic composition

---

## Rossi｜高级时装杂志封面·先锋编辑设计（NovelAI tag 串）

> 模型：NovelAI / 通用文生图 tag 串（用户标注为 NAI，无独立 `negative prompt:` 段）
> 用途：明日方舟 Rossi 角色 · 高级时装杂志封面 / 先锋平面设计；朱红＋深勃艮第＋象牙白的大色块、超大衬线字与印刷质感。
> 来源：用户 2026-11-15 直接提供，正文原样保留，不翻译不改写。

masterpiece, best quality, amazing quality, very aesthetic, absurdres, newest, ultra-detailed, intricate details,
1girl, solo, rossi_(arknights), blonde hair, golden eyes, wolf ears, wolf tail, red hooded cloak, white dress, black corset, fingerless gloves,
youthful appearance, petite, cute face, soft cheeks, delicate facial features, large expressive golden eyes, playful confident smile, lively personality,
avant-garde fashion editorial, luxury fashion campaign, high-end magazine cover, contemporary graphic design, art direction, editorial photography, fashion advertising, experimental typography, sophisticated visual hierarchy,
asymmetric layout, bold graphic composition, oversized typography, large serif lettering, elegant typography, modern sans-serif typography, editorial text layout, small captions, issue number, fine print, typographic grid, overlapping text and figure, cropped lettering, generous negative space, print design,
waist-up to mid-thigh portrait, dynamic three-quarter pose, slightly tilted body, looking directly at viewer, one hand gently holding hood, other hand reaching toward foreground, elegant hand gesture, flowing red cape, sculptural fabric folds, graceful silhouette,
slightly alluring, playful charm, fitted black corset, cinched waist, delicate collarbone, elegant neckline, natural youthful proportions,
vivid vermilion background, deep burgundy geometric blocks, ivory white graphic elements, minimal abstract shapes, bold color blocking, restrained antique gold accents,
dramatic studio lighting, hard directional spotlight, strong chiaroscuro, sculpted facial shadows, golden hair rim light, deep burgundy fabric shadows, crisp highlights, cinematic contrast,
refined anime illustration, painterly anime aesthetic, impressionist oil painting influence, delicate visible brushstrokes, layered pigments, sophisticated color transitions, fine broken-color technique, expressive yet controlled brushwork,
luxurious print texture, subtle paper grain, screen printing texture, halftone details, distressed ink, metallic gold foil accents, editorial print finish,
beautifully structured blonde hair, layered flowing locks, individual flyaway strands, golden and pale cream highlights, detailed wolf fur, intricate fabric texture, refined facial rendering, clean lineart, polished commercial illustration

---

## Rossi｜万圣节幽灵装·平面图形插画（NovelAI 长文本分段）

> 模型：NovelAI / 通用文生图（用户标注为 NAI；分段长文本，负面约束写在正文末尾）
> 用途：明日方舟 Rossi 角色 · 万圣节幽灵床单装；低角度仰视、橙紫平面色块背景、半透织物透光。
> 来源：用户 2026-11-15 直接提供；已去除消息层的 `@long-text:...` 与 `<long_text_quote>` 包装，正文原样保留。

masterpiece, best quality, amazing quality, very aesthetic, absurdres, newest, ultra-detailed, sharp focus, intricate details, crisp lineart,

1girl, solo, rossi_(arknights), arknights, official character design, faithful character design, bear ears, original hairstyle, original hair color, original eye color, faithful original appearance,

**Costume:**
halloween ghost costume, oversized white ghost sheet, large white fabric draped over head and entire body, lightweight sheer white fabric, semi-transparent cloth, translucent fabric, delicate gauzy material, soft flowing fabric, layered fabric folds, loose oversized silhouette, fabric naturally suspended away from the body, visible soft body silhouette through the fabric, subtle overlapping fabric layers, strategically layered opaque folds covering the chest, fully covered breasts, no visible nipples, no exposed intimate areas, irregular flowing hemline, hem reaching mid-thigh, bare legs, no additional clothing,

**Pose and Action:**
adorable lively crouching pose, playful low squat, knees bent and body leaning forward, both arms raised and spread outward while holding the two edges of the oversized ghost sheet, spreading the fabric like little ghost wings, wide flowing cloth forming a playful silhouette around her body, one hand slightly raised higher than the other, fingers playfully curled like little ghost claws, energetic open gesture, lively movement, slightly tilted head, playful welcoming posture,

**Expression:**
mischievous cheerful smile, slightly open mouth, one small visible fang, playful "awoo" expression, bright lively eyes, slightly narrowed smiling eyes, rosy cheeks, cute impish expression, looking directly at viewer,

**Camera and Composition:**
low-angle shot, upward perspective from slightly below, three-quarter view, medium-full shot, character dominates the frame, dynamic diagonal composition, expressive silhouette, flowing fabric spreading outward, clear separation between character and background,

**Background and Graphic Design:**
stylized abstract Halloween graphic background, no physical environment, no realistic scenery, large bold overlapping color blocks, irregular geometric shapes, flowing curved shapes, asymmetrical graphic composition, vivid pumpkin orange, muted violet, warm cream white and deep plum purple, contrasting flat color planes, playful decorative silhouettes of tiny bats, crescent moons, stars and miniature pumpkins, scattered small decorative shapes, subtle layered paper-cut aesthetic, generous negative space, visually rich but uncluttered,

**Lighting and Fabric Rendering:**
soft warm peach-orange illumination, delicate peach-colored rim light along the translucent fabric edges, gentle light passing through thin white cloth, subtle fabric transparency, softly visible underlying silhouette, layered folds creating natural opacity variations, intricate fabric creases, delicate overlapping shadows, soft highlights, luminous ivory fabric, gentle warm skin tones,

**Art Style:**
high-end Japanese anime illustration, popular Pixiv illustration aesthetic, refined anime cel shading, delicate clean lineart, sophisticated soft shading, polished digital painting, exquisite character rendering, luminous pastel colors, bright and airy atmosphere, clean color separation, smooth gradients, crisp details, elegant graphic design, charming Halloween illustration,

No text, no watermark, no additional characters, no photorealism, no rough texture, no grain, no noise, no visible nipples, no exposed intimate areas.

---

## 半脸枝叶遮挡·单眼特写（NovelAI · 局部人脸）

> 模型：通用 Danbooru tag 串（无负面段；`{}` 为 NAI 加权）
> 用途：局部人脸特写；前景枝叶横切画面、半张脸被遮挡、只露一只眼，逆光穿叶形成额头叶影与发缘轮廓光；青白高调、前景虚化。
> ✅ 入库状态：2026-11-16 用户确认入库；与 `novelai-6`（风格母版）同源，是其在「局部人脸」场景下的完整成图写法。
> ⚠ 用法边界：`glossy hair` / `individual hair strands` 为裸材质词，人物全身或手部入画时易致塑料发与崩手；本条目把人脸裁到局部，风险低。
> 来源：2026-11-16 用户提供，正文原样保留，不翻译不改写。

masterpiece, best quality, ultra-detailed, extremely detailed, absurdres, highres, delicate face, highly detailed eyes, intricate iris, multiple eye highlights, glossy hair, individual hair strands, fine lineart, soft painterly gradients, 1girl, close-up, half of the face hidden by leaves, foreground branch crossing the frame, one eye visible, partial face, cropped face, hair over one eye, {backlighting}, {volumetric lighting}, dappled sunlight filtering through leaves, leaf shadows across the forehead, rim light along the hair edge, lens flare, rainbow flare, sparkling particles, floating light dots, high-key lighting, cyan and white color grading, pastel accents, soft contrast, foreground foliage out of focus, depth of field, bokeh, cinematic composition
Undesired content: lowres, bad anatomy, extra limbs, text, watermark, jpeg artifacts, worst quality

---

## 跨引用说明
- ↳ `novelai-7`、`novelai-8` 两条 Rossi 提示词原属「人物」类 `renwu-30` / `renwu-31`，2026-11-15 迁入本类，正文未改动。
- ↳ `novelai-9` 与 `novelai-6` 同源：`novelai-6` 是可复用的风格母版，`novelai-9` 是母版在「局部人脸 + 前景枝叶遮挡」下的完整成图写法。
- ↳ 构件级 tag 与逆向规则见 `skills/novelai-tensorart-reverse/`。
