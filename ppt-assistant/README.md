# PPT 助手 · 使用说明

一个「一条龙」PPT 生成助手：你说需求 + 给数据 → 我（助手）分析需求、写大纲和文案 → 套用你指定的模板风格 → 生成**可编辑 .pptx** 交付。

## 目录结构

```
ppt-assistant/
├── generate_ppt.py          # 生成引擎（套模板视觉规范，按 JSON 规格产出 pptx）
├── ingest.py                # 文件摄取：读 .pptx / .pdf / 图片（扫描版自动 OCR）
├── image_fetch.py           # 联网取图：Pexels 语义搜图 → loremflickr → picsum
├── restyle.py               # 原地重排：把已有 PPT 统一为模板字体/配色
├── check.py                 # 检查器：排版一致性 + 文字遮挡/溢出
├── config.json              # 配置：template + logo + pexels_key(留空,建议用环境变量)
├── analyze_template.py      # 模板拆解工具（分析配色/字体/结构，一般不用跑）
├── sample_work_report.json  # 示例：工作述职内容规格
├── PRD.md                   # 产品需求文档
├── assets/                  # 从模板提取的装饰素材（备用）
└── output/                  # 生成的 pptx + 下载的配图
```

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

## 使用流程（怎么用这个助手）

1. 你在这里直接告诉我：**主题、给谁看、讲多久、页数、有哪些原始数据**（也可以给现有 PPT/PDF 的路径让我摄取）。
2. 我分析需求，必要时追问补缺口。
3. 我生成大纲 + 逐页文案，写成规格 JSON。
4. 运行引擎产出 .pptx，你在 GUI 里直接下载。

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
