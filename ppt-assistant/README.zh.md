# PPT 助手 · 使用说明

[English](README.md) | 中文

一个「一条龙」PPT 生成助手：你说需求 + 给数据 → 我（助手）分析需求、写大纲和文案 → 生成**可编辑 .pptx** 交付。生成器、版式和验收器全部内置于本目录；用户工作区只提供内容规格和显式素材路径，不执行工作区里的业务脚本。

安装 Python 依赖：

```bash
python3 -m pip install -r requirements.txt
```

## 目录结构

```
ppt-assistant/
├── generate_ppt.py          # 生成引擎（套模板视觉规范，按 JSON 规格产出 pptx）
├── build_deck.py            # 默认生成引擎（独立 JSON 规格 → 原生可编辑 PPTX）
├── run_pptfast.sh           # 远端 Desktop 同款 pptfast 运行包启动器
├── ingest.py                # 文件摄取：读 .pptx / .pdf / 图片（扫描版自动 OCR）
├── image_fetch.py           # 联网取图：Pexels 语义搜图 → loremflickr → picsum
├── restyle.py               # 原地重排：把已有 PPT 统一为模板字体/配色
├── check.py                 # 检查器：排版一致性 + 文字遮挡/溢出
├── quality_check.py         # 交付门槛：视觉元素、版式变化、16:9 与文字堆砌检测
├── render_ppt.py            # 用户态渲染：soffice → PDF → PNG
├── slide_ops.py             # 跨 PPT 复制/追加可编辑页面，保留媒体与备注
├── slide_patch.py           # 指定形状的图文对齐修复，仅更新选定页面 XML
├── asset_catalog.py         # 素材清单、SHA256 校验和来源文件盘点
├── config.json              # 配置：template + logo + pexels_key(留空,建议用环境变量)
├── analyze_template.py      # 模板拆解工具（分析配色/字体/结构，一般不用跑）
├── sample_work_report.json  # 示例：工作述职内容规格
├── PRD.md                   # 产品需求文档
├── assets/                  # 从模板提取的装饰素材（备用）
└── output/                  # 生成的 pptx + 下载的配图
```

## 使用用户模板（正式交付首选）

当用户提供现成 PPT 模板时，使用 `build_deck.py --template`。该模式直接打开模板文件，按幻灯片编号复用原页，只替换规格中点名的文本框、图片框和备注；模板母版、主题、背景、Logo、装饰形状、页脚和原有版式都会保留，不会执行模板所在目录的脚本。

模板规格不需要 `meta`，每个 `slides` 项必须覆盖模板的一页，并用 PowerPoint 形状名称作为替换键：

```json
{
  "slides": [
    {
      "template_slide": 1,
      "text": {"Title 1": "新的标题", "Subtitle 2": "新的副标题"},
      "notes": "这一页的讲解备注"
    },
    {
      "template_slide": 2,
      "text": {"TextBox 3": "新的页标题"},
      "images": {"Picture 9": "/绝对路径/新的图片.png"}
    }
  ]
}
```

运行和验收：

```bash
python3 build_deck.py template-spec.json output/交付.pptx --template /path/to/template.pptx
python3 quality_check.py output/交付.pptx --template /path/to/template.pptx
python3 render_ppt.py output/交付.pptx --outdir output/render
```

`--template` 模式会拒绝重复或缺失的模板页、不存在的目标形状和无效素材；带 `--template` 的质量检查还会逐页比较页数、布局、形状类型和图片数量。模板页内未列入 `text`/`images` 的内容保持不变，适合先继承成熟视觉稿，再逐步替换内容。

## 现有 PPT 的交付工具

已提交的 PPT 可以补充 Markdown 讲稿和一致的逐页备注，同时保留页面 XML、媒体、背景、图表及公式矢量。GIF 和公式工具用于已授权的页面修改。Python 依赖见 `requirements.txt`；视频转换另需 `ffmpeg`/`ffprobe`，同步需要 `ssh`、`rsync` 及远端 `sha256sum`。

```bash
python3 speaker_notes.py export source.pptx script.md
# Complete the draft from actual slide evidence before embedding.
python3 speaker_notes.py embed source.pptx script.md delivery.pptx
python3 delivery.py audit delivery.pptx --baseline source.pptx --script script.md --gif-pages 8 15 --report acceptance.json
```

Markdown 必须按真实页序为每页提供一个非空 `## Pn｜Title (20 seconds)` 段落，也支持 `（20 秒）`。其他二级章节仅保留在 Markdown，HTML 注释不进入备注。导出复制已有备注，并将缺失讲稿标为 TODO；最终正文由助手依据已核对的事实撰写。写入前拒绝重复、漏页、空白和未完成段落。工具保留所有非备注 ZIP 部件，仅允许必要的备注声明，逐页读回核对后原子替换输出。支持任意页数、重排页面、无备注模板和明确授权的原地更新；保真检查须保留原始基准。

讲稿正式、结论先行，围绕问题、个人贡献、结果和可复用方法、配置或数据展开，保留单位、证据边界和团队归属。逐页秒数为停顿和翻页留余量，并提供压缩方案；预算属于计划时间，不代表实测演讲时长。

### 完整视频动画

```bash
python3 video_gif.py convert source.mp4 demo.gif --target-seconds 10
python3 video_gif.py insert source.pptx demo.gif animated.pptx --page 8 --shape "Picture 9" --speed 10
python3 delivery.py audit animated.pptx --gif-pages 8 --report animation.json
```

转换完整解码第一个视频流，不截取片段。自动选择以接近目标时长为准，理想倍速达到五时优先选五的倍数；短视频使用包括 1X 在内的整数倍速。显式 `--speed` 覆盖自动选择。`--fps`、`--size`、`--speed-multiple` 和 `--timeout` 控制输出，实际时长仅进入 JSON。插入使用报告中的倍速，按名称替换唯一图片，保持比例，添加原生可编辑的左上角 `nX` 标记，保存后验证 GIF 字节和多帧属性。标记字号与配色可配置。此 python-pptx 保存流程仅用于已授权的页面修改，不能用于只改备注。PDF 和编辑视图显示静帧；放映动画须另行检查。

### 排版后的矢量公式

准备 JSON 列表，包含页码、MathText 表达式和以英寸为单位的位置框：

```json
[{"page": 19, "expression": "$T_{\\Delta}=T_t^{-1}T_{t+1}$", "box_inches": [1, 4, 6, 1], "color": "202020", "name": "Relative pose"}]
```

```bash
python3 formula.py source.pptx formulas.json formulas.pptx
```

字形曲线和分数线转换为 PowerPoint 原生自由形状。支持 Matplotlib MathText，不支持完整 LaTeX；无法解析的语法在保存前失败。结果是可编辑矢量，不是公式编辑器的语义对象。数学定义、坐标系、单位和时间索引须核对指定参考。已授权的公式修改需渲染检查。

### 校验后的文件同步

```bash
python3 delivery.py sync /local/delivery --files delivery.pptx script.md acceptance.json --host desktop --destination /remote/delivery
python3 -m unittest test_delivery -v
```

同步以用户要求为前提，只复制根目录下显式选定的普通文件。工具创建目标目录，以校验和方式运行 rsync，不删除远端内容，再逐文件比较远端 SHA256。认证使用主机 SSH 配置、agent 或终端支持的认证方式，密码不作为参数或持久化文件。传输失败或哈希不一致时不报告成功。拒绝根目录之外的文件、重复选择、符号链接和包含换行的文件名。主机使用 SSH 别名或 user@host，目标为 POSIX 绝对路径。当前文件采用稳定名称；旧版归档或模板分离遵循授权范围。

验收比较备注和必要声明之外的全部部件，核对讲稿与备注逐页一致，并要求指定页含动画媒体；不判断布局或放映效果。页面修改后运行 `quality_check.py`、`check.py` 和 `render_ppt.py`，检查对齐、文字堆叠、公式边界和风格。同步测试模拟传输，不代表用户主机已经连通。

### 复用可编辑页面

```bash
python3 slide_ops.py reference.pptx target.pptx merged.pptx --pages 3 5 --position 2
```

`slide_ops.py` 将指定页面复制到尺寸相同的目标 PPT，使用目标主题和版式。它保留形状 XML、可编辑图表、外部超链接、媒体和演讲者备注文本，为导入部件分配唯一文件名并重映射关系 ID。内部页面跳转需要页码映射，因此工具拒绝导入。主题继承可能改变复制页面的外观。输出采用原子写入，两份输入文件保持不变。新增章节后更新目录、章节导航、页码和讲稿，再运行结构和渲染检查。

### 定点图文对齐修复

```bash
python3 slide_patch.py inspect source.pptx > shapes.json
python3 slide_patch.py apply source.pptx alignment.json aligned.pptx
```

使用检查结果中的顶层形状 ID 编写非空 JSON 列表：

```json
[{"page": 3, "shape_id": 12, "box_inches": [1, 2, 5, 1], "text_frame": {"word_wrap": true, "vertical_anchor": "top", "margin_inches": [0, 0, 0, 0], "line_spacing": 1.2, "space_before_pt": 0, "space_after_pt": 0, "alignment": "left"}}]
```

每条操作指定几何位置、文本框设置或两者。内边距按左/上/右/下排列，行距为倍数。文本框修复关闭自动缩放，保留文字、文本片段及字体。仅选定页面 XML 改变，其他页面、媒体、关系、背景和备注字节一致。无效 ID、设置、重复操作或越界框在替换输出前失败。工具执行明确修复，不自动推断对齐，也不编辑组合内的文字或表格单元格。渲染后检查堆叠、换行和图片比例。

### 素材与证据清单

```bash
python3 asset_catalog.py scan ./project-assets --output ./project-assets/assets.json --markdown ./project-assets/assets.md
python3 asset_catalog.py verify ./project-assets ./project-assets/assets.json --strict
```

清单记录稳定的相对路径、文件类型、MIME 类型、字节数和 SHA256。工具跳过隐藏文件和符号链接，严格模式可以发现新增或缺失文件。原始素材与派生预览应分开保存。选择只含素材的目录：工具不检测凭据，也不脱敏文件名。每条结论关联来源并注明测量限制；候选数量、筛选通过候选、动作返回和实际抓取成功属于不同证据。联合配置变化不能证明某项优化的独立贡献，几何预览不能证明机器人实际执行安全。

## 默认生成引擎

复杂 PPT 使用内置 `build_deck.py`，不依赖用户工作区中的 `build_deck.py`、模板脚本或业务目录：

```bash
python3 build_deck.py 规格.json output/输出名.pptx
python3 quality_check.py output/输出名.pptx
python3 render_ppt.py output/输出名.pptx --outdir output/render
```

规格中的图片路径相对于规格 JSON 文件解析。支持 `cover`、`cards`、`process`、`comparison`、`image_split`、`image_grid`、`table`、`chart`、`chart_dashboard` 和 `closing`，图表为 PowerPoint 原生可编辑对象。

## Desktop 同款 pptfast 引擎

远端 Desktop 的增强链路使用 `@liustack/pptfast@0.20.0`：语义 IR、`dense` 内容节奏、图片/对比/步骤等组件，以及 `audit` 几何审查。仓库内的 `run_pptfast.sh` 只解析已安装的运行包，不读取或执行用户工作区代码：

```bash
bash run_pptfast.sh validate deck项目/
bash run_pptfast.sh render deck项目/ -o output/交付.pptx
bash run_pptfast.sh audit deck项目/
```

启动器会先查找当前引擎目录下的 `node_modules/@liustack/pptfast`，再查找 Desktop 部署约定的 `~/ppt-assistant/node_modules/@liustack/pptfast`。找不到运行包时返回 78，并明确提示安装或回退到内置 `build_deck.py`；不会静默生成低质量纯文字稿。

## 快速开始

```bash
python3 generate_ppt.py 规格.json output/输出名.pptx
```

模板默认使用内置的 `assets/base_template.pptx`；可在 `config.json` 的 `template` 里指定其它模板，或用 `--template` 覆盖。

## 配置（config.json）

| 字段 | 说明 |
|------|------|
| `template` | 基底 `.pptx` 模板（相对脚本目录），默认 `assets/base_template.pptx` |
| `logo` | 学术风引擎左上角 logo 图片，默认 `assets/logo.png`；删除/清空则不放置 logo |
| `pexels_key` | 留空；建议改用环境变量 `PEXELS_API_KEY`。无 key 时自动降级 loremflickr/picsum |

> **背景与图标**：生成时保留模板的**母版浅蓝背景**，并在内容页右上角放置模板的 **logo（图片7）**；版式本身灵活程序化生成（配色/字体与模板一致）。

## 视觉规范（已锁定的模板 DNA）

| 项 | 值 |
|----|----|
| 标题字体 | 华文中宋（加粗） |
| 正文字体 | Noto Serif SC |
| 辅助字体 | 微软雅黑 |
| 尺寸 | 16:9 宽屏 13.33×7.5 英寸 |
| 背景 | 母版浅蓝渐变 + 右上角 logo |
| 嵌入字体 | 已随模板保留（华文中宋 / Noto Serif SC / 等线 / 微软雅黑） |

## 配色方案（meta.palette，参考 Coolors / 2025 趋势色）

| 值 | 名称 | 主色 | 强调 | 章节标 |
|----|------|------|------|--------|
| `coastal` | 海岸蓝调（默认） | `#1B4965` 深青蓝 | `#E07A5F` 珊瑚橙 | `#62B6CB` 浅青 |
| `ocean` | 深海蓝 | `#1D3557` 深海蓝 | `#E63946` 珊瑚红 | `#457B9D` 钢蓝 |
| `aurora` | 极光青绿 | `#2A9D8F` 青绿 | `#E76F51` 陶土橙 | `#48CAE4` 浅青 |
| `indigo` | 靛蓝紫 | `#312E81` 靛蓝 | `#E11D48` 玫瑰红 | `#6366F1` 淡紫 |

在 `meta` 里指定：`"palette": "aurora"`。

## 内容规格（JSON）格式

顶层两个字段：

```json
{
  "meta": { "title": "...", "subtitle": "...", "author": "...", "org": "...", "date": "..." },
  "slides": [ { ... }, { ... } ]
}
```

每张幻灯片是一个对象，用 `type` 指定版式：

| type | 用途 | 关键字段 |
|------|------|----------|
| `cover` | 封面 | 取 `meta` 字段 |
| `toc` | 目录 | `title`、`items[]` |
| `section` | 正文（小节+要点，自动双栏） | `chapter`、`title`、`blocks[]`（每块含 `heading` + `points[]`） |
| `bullets` | 编号条目列表 | `chapter`、`title`、`intro`、`items[]`（每项含 `head` + `text`） |
| `table` | 表格 | `chapter`、`title`、`headers[]`、`rows[][]` |
| `process` | 流程/步骤卡片 | `chapter`、`title`、`steps[]`（每步含 `n` + `head` + `text`） |
| `closing` | 结束页 | `text`、`subtitle` |

完整示例见 `sample_work_report.json`。

## 接受输入文件（PPT / PDF / 图片）

助手可以按**文件路径**接受现有 `.pptx` / `.pdf` / 图片：

```bash
python3 ingest.py /path/to/文件.pptx   # .pptx / .pdf / .png / .jpg
```

- **扫描版 PDF / 图片**：自动 OCR（pdftoppm 渲染 + tesseract `chi_sim+eng`）。
- 用途：①给现有 PPT 重新排版/美化；②把 PDF 转成新 PPT；③提取内容或风格做参考。

**注意**：GUI 的附件上传目前只收图片，通用文件请**给文件路径**（或从工作区文件树选）。

## 配图（联网取图 + 填充）

`image` 版式支持两种来源：
- **本地路径**：`"image": "/path/to/x.jpg"`
- **关键词联网填充**：`"keyword": "modern office"` → Pexels 语义搜图（自动署名）→ loremflickr → picsum 兜底

```bash
python3 image_fetch.py "办公室 会议" output/img/office.jpg 1600 900
```

Pexels key 优先读环境变量 `PEXELS_API_KEY`，其次读 `config.json` 的 `pexels_key`（留空则用 loremflickr/picsum 兜底，无需 key）。

## 更改已有 PPT

```bash
# 原地统一字体/配色为模板风格
python3 restyle.py 已有.pptx 输出.pptx
```

深度改动（改内容/重排）走 `ingest.py` 提取 → 重写规格 → `generate_ppt.py` 重新生成。

## 检查（排版一致性 + 遮挡）

```bash
python3 check.py 输出.pptx
```

检查项：字体一致性、配色一致性、标题对齐、**文字遮挡**、文本溢出、出界。生成后交付前建议先跑一遍。

复杂 PPT 还必须通过结构质量门槛，并完成逐页渲染：

```bash
python3 quality_check.py 输出.pptx
python3 render_ppt.py 输出.pptx --outdir 工作区/.render
```

`quality_check.py` 会拒绝 5 页以上的纯文字草稿（图片/图表过少、版式结构不足或页面比例不对）。`render_ppt.py` 优先使用系统 `soffice`，再查找用户目录中的 LibreOffice，不依赖 root 权限。

## 使用流程（怎么用这个助手）

1. 你在这里直接告诉我：**主题、给谁看、讲多久、页数、有哪些原始数据**（也可以给现有 PPT/PDF 的路径让我摄取）。
2. 我分析需求，必要时追问补缺口。
3. 我生成大纲 + 逐页文案，写成规格 JSON。
4. 运行引擎产出 .pptx，你在 GUI 里直接下载。

## 参考模板生成完整转正汇报

当模板只用于封面和视觉参考、正文需要扩展时，使用 `build_deck.py <spec.json> <out.pptx> --template <template.pptx> --probation`，并在规格 `meta` 中设置 `"deck_mode": "native_v2"`、`"theme": "paper"`。该模式适用于 13.333 × 7.5 英寸模板：保留第一张封面原样，正文使用原生文字、图形和可编辑数据图表，结束页沿用封面的母版背景。规格首项为 `{"type": "cover"}`；其余页面的字段由 `DeckBuilder.compose_probation_v2()` 定义，CLI 示例见 [test_build_deck.py](test_build_deck.py)。模板照片之外的正文图片按文件内容检测重复；预制整页图表不作为正文排版的替代品。

可用版式包括目录、职责表、时间线、算法流程、问题排查、候选数据对照、性能结果、现场双图、WRC 照片与职责、语音流程、运行清单、个人总结、改进对照表、成长规划和致谢。使用原始照片或实验局部图，数据直接填入 `evidence.charts` 的 `before` / `after` 数组。新增正文页数与参考模板不同，因此运行普通 `quality_check.py`，不使用要求逐页相等的 `--template` 检查。封面原样保留、图表数据、图片去重和非法规格行为用 `python3 -m unittest discover -s ppt-assistant -p 'test_build_deck.py'` 在仓库根目录验证。

实验局部图直接引用原图：`evidence.image_crop` 或 `root_cause.images[].crop` 使用原图像素坐标 `[left, top, right, bottom]`。生成器在内存中裁剪并嵌入图片，不依赖预览目录或中间裁图；超出原图范围的裁剪会失败。

抓取结果的配对排版支持 `depth_pair` 和 `grasp_comparison`。前者读取两个同尺寸深度 `.npy` 数组，以同一 `crop` 和 `limits_m` 绘制单项深度图与原生色标。后者的三个 `frames` 分别引用 `image`、`calibration`、`before`、`after`，从相机标定和实际选定位姿投影六组原生夹爪线框；`before_opening_mm` / `after_opening_mm` 可用于检查位姿是否与统计一致。同一轮的原始照片可以在前后面板中配对，禁止拿其他轮次或无关场景代替。姿态和开合来自记录，指长、指宽与厚度是显示用的几何参数，不作为碰撞或夹爪标定结论。`evidence` 省略 `image` 时使用两张横排可编辑图表；`research_plan` 展示四个方向，`application_plan` 展示先进模型与本地算法接入。全部相关测试使用 `python3 -m unittest discover -s ppt-assistant -p 'test_*.py'`。

`visual_gallery` 使用三个 `items`，每项指定原始 `image`、透明 `layers`、像素 `crop`、`title` 和 `body`。原图与图层必须来自同一保存帧且尺寸相同，图层须为 RGBA；生成器以相同位置和缩放分别嵌入，可在 PowerPoint 中单独编辑或移除图层，不合成整页图片。`data_table` 使用 `headers`、`rows` 与 `note` 嵌入可编辑数据表。候选筛选记录与现场效果、不同实验之间的统计分别说明，考核要求与实际完成项分别表述。

紧凑优化案例使用 `depth_case`、`pose_case` 与 `efficiency_case`，同页组织优化前、方案和优化后。`depth_case` 引用同帧的两个推理响应、原始照片、标定及深度数组；响应候选数须与规格一致，以分数排序展示前三个候选。`pose_case` 保留三轮配对照片、实际开合与筛选统计；`native_gallery` 从保存位姿绘制其他场景。所有原生夹爪使用相同几何、颜色和线宽。正文创建时清除模板占位符，空文案不生成文本框；原始封面仍保持不变。

`pose_case` 可从每轮执行记录读取全部候选，并用蓝色叠加通过项、红色叠加未通过项；候选密集时在内存中合成同样的夹爪几何，避免生成大量独立形状。讲述顺序可通过规格中的 `slides` 直接调整，推荐先现场项目再算法优化。性能页可用 `after_detail` 写出分割、深度补全、抓取候选生成的耗时和并行关系；成长规划使用 `roadmap` 的近期、中期、长期三列。

## 权限提示

如果会话已经显示 `danger-full-access`，运行 Bash、Write 或渲染命令时不要再次传入 `sandbox_permissions`。重复请求最高权限，或把调用改成 `workspace-write`，会被工具层拒绝；这属于调用参数错误，不代表素材目录没有读写权限。

## 默认约定

- **页数**：默认 20 页（可指定）。
- **数据**：优先用你提供的原始数据；没有时我用合理示例数据并标注。
- **配图**：混合策略（真实图优先 + AI 兜底），当前为后续增强项，暂未接入。

## 路线图

- ✅ M0/M1：模板拆解 + 生成引擎 + 全版式（封面/目录/正文/表格/流程/结束）
- ⬜ M2：图表（原生可编辑 chart）、图标、更多版式
- ⬜ M3：配图（联网真实图 + AI 兜底 + 版权标注）
- ⬜ M4：迭代能力（单页修改、一键换主题、版本管理）
- ⬜ M5：多场景扩展 + PDF 导出

## 原生图表与数据对比

`charts.py` 供默认生成与 `native_v2` 参考模板扩展共用。图表是 PowerPoint 原生对象，数据保存在 PPTX 内嵌工作簿中；在 PowerPoint/WPS 中可编辑图表与数据。渲染复核使用 LibreOffice，尚未验证 WPS 的逐项交互编辑。

| 要表达的关系 | `kind` | 数据要求 |
| --- | --- | --- |
| 类别对比、前后对比 | `column` | 同口径分类和系列 |
| 排名、长类别名称 | `bar` | 单系列可排序、高亮 |
| 时间趋势 | `line` | 有序分类；缺失用 `null` |
| 规模变化 | `area` | 有序分类；保留零基准 |
| 总量构成 | `stacked_column` / `stacked_bar` | 分项使用同一单位 |
| 结构占比 | `percent_column` / `percent_bar` | 非负完整数据，各分类总量大于零 |
| 单个整体的组成 | `donut` / `pie` | 单系列，最多 8 类，非负且总量大于零 |
| 两个数值变量 | `scatter` | `points: [[x, y], ...]`，不连线 |
| 三个数值变量 | `bubble` | `points: [[x, y, size], ...]`，正面积大小 |

`chart` 每页一个图；`chart_dashboard` 每页 `charts` 数组包含 2–4 个图，三个图时底行跨两列。每个图可配置 `title`、`unit`、`source` 和 `takeaway`，页面也可有 `source`、`takeaway` 和 `notes`。图面注释要简短，详细范围与计算口径放备注；超出文本容量会拒绝生成。

```json
{
  "meta": {"title": "耗时分析", "theme": "paper"},
  "slides": [{
    "layout": "chart",
    "title": "比较各项耗时",
    "chart": {
      "kind": "bar",
      "categories": ["分割", "模型推理", "结果校验"],
      "series": [{"name": "耗时", "values": [0.8, 3.5, 0.9]}],
      "sort": "descending",
      "highlight": ["模型推理"],
      "number_format": "0.0",
      "y_axis": {"title": "耗时（秒）", "min": 0, "max": 4, "major_unit": 1}
    },
    "source": "示例数据，非项目实测",
    "takeaway": "模型推理是主要耗时项"
  }]
}
```

CSV 输入用以下字段替代 `categories` 与 `series[].values`，路径相对于 JSON 规格；UTF-8/BOM 均可，空单元格保留为缺测：

```json
{
  "kind": "column",
  "data_file": "metrics.csv",
  "category_column": "项目",
  "series": [
    {"name": "调整前", "column": "before"},
    {"name": "调整后", "column": "after"}
  ]
}
```

分类图支持 1–40 个分类、1–6 个系列，XY 图每系列最多 500 点；实际可读容量取决于面板大小，密集条形图会拒绝生成，需拆页。`x_axis.label_interval` 可指定分类刻度间隔；不指定时按宽度稀疏刻度。`x_axis/y_axis.font_size` 支持 9–18pt，`title` 标注轴单位，数值轴可设 `min/max/major_unit/number_format`。横向条形图同样用 `y_axis` 配置值轴；柱、条、面积图值轴必须包含零且不能隐藏实测值或堆叠总量。

`number_format` 使用 Excel 格式，`series[].color` 为六位 RGB 色值；`data_labels` 控制数值标签。百分比堆叠保留源数量、值轴使用 0–1（显示 0–100%），默认不显示数量标签；显式启用标签时显示源数量，百分比格式只能放在 `y_axis.number_format`。饼/环形图标注占比。`sort` 仅支持单系列 `column/bar`，为 `ascending/descending`；`highlight` 指定已有分类。跨页比较需显式保持系列颜色、范围和单位一致。

校验拒绝长度不匹配、非数值、NaN/Infinity、全缺失系列、无效气泡面积、不完整 CSV、混合内联/CSV、隐藏数据的坐标范围。缺失值不补零；未通过校验或排版容量不足时不替换已有输出。

独立示例覆盖全部 12 种图型、排序高亮、缺测、CSV 和二图/四图组合。全部是明确标注的示例数据：

```bash
python3 build_deck.py examples/chart_report.json output/图表能力示例_V0.1.pptx
python3 quality_check.py output/图表能力示例_V0.1.pptx
python3 check.py output/图表能力示例_V0.1.pptx
python3 render_ppt.py output/图表能力示例_V0.1.pptx --outdir output/chart-review
python3 -m unittest discover -s . -p 'test_*.py' -q
```

`examples/chart_report.expected.json` 是 CLI 生成结果的无密钥快照：检查可见文本、图型、系列名称与源数值，也记录 XY 坐标和气泡大小。检查器不解析图表内部标签布局，仍须查看渲染页。
