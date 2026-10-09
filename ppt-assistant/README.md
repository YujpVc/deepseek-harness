# PPT assistant · Usage guide

English | [中文](README.zh.md)

An end-to-end PPT assistant: provide requirements and data, and the assistant analyzes the request, writes an outline and copy, and delivers an **editable .pptx**. Generators, layouts and checks live in this directory. The user workspace supplies content specifications and explicit asset paths; workspace business scripts are not executed.

Install Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Directory structure

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
├── config.json              # 配置：template + logo + pexels_key(留空,建议用环境变量)
├── analyze_template.py      # 模板拆解工具（分析配色/字体/结构，一般不用跑）
├── sample_work_report.json  # 示例：工作述职内容规格
├── PRD.md                   # 产品需求文档
├── assets/                  # 从模板提取的装饰素材（备用）
└── output/                  # 生成的 pptx + 下载的配图
```

## User templates (preferred for formal delivery)

Use `build_deck.py --template` for an existing PPT template. This mode opens the template, reuses its pages by slide number, and replaces only named text shapes, picture shapes and notes. Masters, themes, backgrounds, logos, decorations, footers and existing layouts remain intact. Scripts in the template directory are not executed.

Template specifications do not require `meta`. Every `slides` entry must cover a template page and use PowerPoint shape names as replacement keys:

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

Generate and verify:

```bash
python3 build_deck.py template-spec.json output/交付.pptx --template /path/to/template.pptx
python3 quality_check.py output/交付.pptx --template /path/to/template.pptx
python3 render_ppt.py output/交付.pptx --outdir output/render
```

`--template` rejects duplicate or missing template pages, nonexistent target shapes and invalid assets. The quality check with `--template` also compares page counts, layouts, shape types and picture counts page by page. Content not listed in `text`/`images` remains unchanged, allowing an established visual design to be inherited before replacing its content.

## Default generator

Complex presentations use the built-in `build_deck.py`, independently of generators, template scripts or business directories in the user workspace:

```bash
python3 build_deck.py 规格.json output/输出名.pptx
python3 quality_check.py output/输出名.pptx
python3 render_ppt.py output/输出名.pptx --outdir output/render
```

Image paths resolve relative to the specification JSON. Supported layouts are `cover`, `cards`, `process`, `comparison`, `image_split`, `image_grid`, `table`, `chart`, `chart_dashboard` and `closing`. Charts are native editable PowerPoint objects.

## Desktop-compatible pptfast engine

The enhanced Desktop pipeline uses `@liustack/pptfast@0.20.0`: semantic IR, `dense` content pacing, image/comparison/step components and geometric `audit`. The repository's `run_pptfast.sh` resolves only the installed runtime; it does not read or execute workspace code:

```bash
bash run_pptfast.sh validate deck项目/
bash run_pptfast.sh render deck项目/ -o output/交付.pptx
bash run_pptfast.sh audit deck项目/
```

The launcher checks `node_modules/@liustack/pptfast` under the engine directory, then the Desktop convention `~/ppt-assistant/node_modules/@liustack/pptfast`. A missing runtime returns 78 with instructions to install it or fall back to built-in `build_deck.py`; it does not silently produce a poor text-only draft.

## Quick start

```bash
python3 generate_ppt.py 规格.json output/输出名.pptx
```

The default template is `assets/base_template.pptx`. Set another template through `config.json` or override it with `--template`.

## Configuration (config.json)

| Field | Meaning |
|------|------|
| `template` | Base `.pptx` template, relative to the script directory; defaults to `assets/base_template.pptx` |
| `logo` | Optional top-left logo for the academic generator; defaults to `assets/logo.png`, remove or clear to omit |
| `pexels_key` | Leave empty; prefer environment variable `PEXELS_API_KEY`. Without a key, fall back to loremflickr/picsum |

> **Background and logo**: generation retains the template's **light-blue master background** and puts its **logo (图片7)** at the upper right of content pages. Layouts remain programmatic and flexible.

## Visual conventions (template design)

| Item | Value |
|----|----|
| Title font | 华文中宋 (bold) |
| Body font | Noto Serif SC |
| Supporting font | 微软雅黑 |
| Dimensions | 16:9 widescreen, 13.33×7.5 inches |
| Background | Light-blue master gradient and upper-right logo |
| Embedded fonts | Retained from the template: 华文中宋 / Noto Serif SC / 等线 / 微软雅黑 |

## Palettes (meta.palette, inspired by Coolors and 2025 colors)

| Value | Name | Primary | Accent | Section marker |
|----|------|------|------|--------|
| `coastal` | Coastal blue (default) | `#1B4965` dark teal | `#E07A5F` coral orange | `#62B6CB` light cyan |
| `ocean` | Deep ocean | `#1D3557` deep blue | `#E63946` coral red | `#457B9D` steel blue |
| `aurora` | Aurora teal | `#2A9D8F` teal | `#E76F51` terracotta | `#48CAE4` light cyan |
| `indigo` | Indigo violet | `#312E81` indigo | `#E11D48` rose red | `#6366F1` light violet |

Specify `"palette": "aurora"` in `meta`.

## Content specification (JSON)

Two top-level fields:

```json
{
  "meta": { "title": "...", "subtitle": "...", "author": "...", "org": "...", "date": "..." },
  "slides": [ { ... }, { ... } ]
}
```

Each slide is an object whose `type` selects its layout:

| type | Purpose | Key fields |
|------|------|----------|
| `cover` | Cover | Uses `meta` fields |
| `toc` | Table of contents | `title`, `items[]` |
| `section` | Content sections and points; automatic two columns | `chapter`, `title`, `blocks[]`, each with `heading` + `points[]` |
| `bullets` | Numbered entries | `chapter`, `title`, `intro`, `items[]`, each with `head` + `text` |
| `table` | Table | `chapter`, `title`, `headers[]`, `rows[][]` |
| `process` | Process or step cards | `chapter`, `title`, `steps[]`, each with `n` + `head` + `text` |
| `closing` | Ending | `text`, `subtitle` |

See `sample_work_report.json` for a complete example.

## Input files (PPT / PDF / images)

The assistant accepts existing `.pptx`, `.pdf` and images by **file path**:

```bash
python3 ingest.py /path/to/文件.pptx   # .pptx / .pdf / .png / .jpg
```

- **Scanned PDFs / images**: automatic OCR through pdftoppm rendering and tesseract `chi_sim+eng`.
- Uses: restyle existing presentations, convert PDFs into presentations, or extract content and visual references.

**Note**: GUI attachments currently accept images only. Supply a **file path** for other files, or select one from the workspace file tree.

## Images (online search and filling)

The `image` layout supports two sources:

- **Local path**: `"image": "/path/to/x.jpg"`
- **Keyword search**: `"keyword": "modern office"` → Pexels semantic search with attribution → loremflickr → picsum fallback

```bash
python3 image_fetch.py "办公室 会议" output/img/office.jpg 1600 900
```

Pexels credentials resolve first from `PEXELS_API_KEY`, then `config.json`'s `pexels_key`. An empty key uses the keyless loremflickr/picsum fallback.

## Modify an existing PPT

```bash
# 原地统一字体/配色为模板风格
python3 restyle.py 已有.pptx 输出.pptx
```

For deeper content or layout changes, extract through `ingest.py`, rewrite the specification, then regenerate with `generate_ppt.py`.

## Checks (layout consistency and obstruction)

```bash
python3 check.py 输出.pptx
```

Checks cover fonts, colors, title alignment, **text obstruction**, overflow and out-of-bounds shapes. Run them after generation and before delivery.

Complex decks also require the structural quality check and page-by-page rendering:

```bash
python3 quality_check.py 输出.pptx
python3 render_ppt.py 输出.pptx --outdir 工作区/.render
```

`quality_check.py` rejects text-only drafts with five or more pages, too few images/charts, insufficient layout variety or incorrect page proportions. `render_ppt.py` prefers system `soffice`, then user-scoped LibreOffice, without requiring root.

## Workflow (using the assistant)

1. Provide **topic, audience, presentation duration, page count and raw data**, or paths to existing PPT/PDF inputs.
2. The assistant analyzes the request and asks only for missing information.
3. It drafts an outline and page copy as a JSON specification.
4. The engine generates a .pptx for download through the GUI.

## Complete probation presentations from reference templates

When a template supplies cover artwork and a visual reference while the body needs expansion, use `build_deck.py <spec.json> <out.pptx> --template <template.pptx> --probation` with `"deck_mode": "native_v2"` and `"theme": "paper"` in `meta`. This mode supports 13.333 × 7.5 inch templates, keeps the first cover unchanged, composes native text, shapes and editable charts, and uses the cover master background for the ending. The first specification entry is `{"type": "cover"}`. Body fields are defined by `DeckBuilder.compose_probation_v2()`; see [test_build_deck.py](test_build_deck.py) for CLI examples. Body photographs outside the template are deduplicated by file content. Pre-rendered full-page charts do not replace native body layouts.

Layouts include directories, responsibility tables, timelines, algorithm flows, troubleshooting, candidate comparisons, performance results, paired site photographs, WRC photographs and responsibilities, voice flows, operating checklists, personal summaries, improvement tables, growth plans and thanks. Use original photographs or experiment details, with numeric `before` / `after` arrays in `evidence.charts`. Expanded bodies differ in page count from the reference, so run ordinary `quality_check.py`, not its equal-page-count `--template` check. At the repository root, `python3 -m unittest discover -s ppt-assistant -p 'test_build_deck.py'` verifies unchanged covers, chart data, photograph deduplication and invalid specifications.

Experiment details reference original images: `evidence.image_crop` and `root_cause.images[].crop` use source-pixel coordinates `[left, top, right, bottom]`. The generator crops and embeds in memory without preview directories or intermediate image files. Crops beyond the source bounds fail.

Paired grasp results use `depth_pair` and `grasp_comparison`. The former reads two equally sized depth `.npy` arrays with a shared `crop` and `limits_m`, producing atomic depth images and a native scale. The latter's three `frames` reference `image`, `calibration`, `before` and `after`, projecting six native gripper wireframes from camera calibration and recorded selected poses. `before_opening_mm` / `after_opening_mm` can validate pose/statistic agreement. One round's source photograph may appear in both comparison panels; unrelated rounds or scenes cannot replace it. Poses and openings come from records; display finger length, width and thickness do not establish collision or gripper-calibration results. Without `image`, `evidence` uses two horizontal editable charts. `research_plan` shows four directions; `application_plan` combines advanced models and local algorithms. Run all related tests with `python3 -m unittest discover -s ppt-assistant -p 'test_*.py'`.

`visual_gallery` takes three `items`, each with source `image`, transparent `layers`, pixel `crop`, `title` and `body`. Images and layers must come from the same saved frame, have identical dimensions, and use RGBA layers. They are embedded separately at matching positions and scales for editing or removal in PowerPoint, rather than flattened into a full-page image. `data_table` embeds editable tables from `headers`, `rows` and `note`. Candidate-filter records, site effects and statistics from separate experiments are explained separately; assessment requirements and completed work are distinguished.

Compact cases use `depth_case`, `pose_case` and `efficiency_case` to show the prior result, solution and updated result on one page. `depth_case` references two same-frame inference responses, source photographs, calibration and depth arrays; response candidate counts must match the specification, with the top three candidates ranked by score. `pose_case` keeps three rounds of paired photographs, real openings and filtering statistics; `native_gallery` draws other scenes from saved poses. All native grippers share geometry, colors and line widths. Body generation clears template placeholders and omits empty text boxes; the original cover remains unchanged.

`pose_case` can read all candidates from each round's execution record, overlaying accepted candidates in blue and rejected candidates in red. Dense candidates are composited in memory with the same geometry to avoid excessive shapes. The `slides` specification controls the order; site projects before algorithm improvements are recommended. Performance pages use `after_detail` for segmentation, depth completion, grasp-candidate generation timings and parallelism. Growth plans use `roadmap`'s near-, mid- and long-term columns.

## Permission instructions

When a session already reports `danger-full-access`, do not pass `sandbox_permissions` again for Bash, Write or rendering commands. Re-requesting maximum permissions, or changing a call to `workspace-write`, is rejected by the tool layer. This is a call-argument error rather than a lack of read/write access to the materials directory.

## Defaults

- **Pages**: 20 by default; configurable.
- **Data**: prefer user-supplied raw data; otherwise use and label reasonable example data.
- **Images**: combine real photographs first with AI fallback; this is a planned enhancement and is not connected yet.

## Roadmap

- ✅ M0/M1: Template analysis, generation engine and all layouts (cover/directory/content/table/process/ending)
- ⬜ M2: Native editable charts, icons and more layouts
- ⬜ M3: Online photographs, AI fallback and attribution
- ⬜ M4: Per-page edits, theme switching and versioning
- ⬜ M5: Multiple scenarios and PDF export

## Native charts and data comparisons

`charts.py` is shared by default generation and `native_v2` reference-template expansion. Charts are native PowerPoint objects with data in embedded workbooks. Their graphics and data are editable in PowerPoint/WPS. Visual review uses LibreOffice; interactive WPS editing has not been verified item by item.

| Relationship | `kind` | Data requirements |
| --- | --- | --- |
| Category and before/after comparisons | `column` | Consistent categories and series |
| Rankings and long category names | `bar` | Single-series sorting and highlighting |
| Time trends | `line` | Ordered categories; missing measurements are `null` |
| Scale changes | `area` | Ordered categories and zero baseline |
| Total composition | `stacked_column` / `stacked_bar` | Components share units |
| Composition percentages | `percent_column` / `percent_bar` | Complete nonnegative data; positive category totals |
| One whole's composition | `donut` / `pie` | One series, at most 8 categories, nonnegative with positive total |
| Two numeric variables | `scatter` | `points: [[x, y], ...]`, unconnected |
| Three numeric variables | `bubble` | `points: [[x, y, size], ...]`, positive area sizes |

`chart` places one chart on a page. `chart_dashboard` accepts 2–4 charts in `charts`; three charts give the bottom chart a full-width panel. Charts accept `title`, `unit`, `source` and `takeaway`; pages also accept `source`, `takeaway` and `notes`. Keep on-page annotations short and put detailed scope and calculation definitions in notes. Text beyond capacity is rejected.

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

For CSV input, replace `categories` and `series[].values` with these fields. Paths are relative to the JSON specification, UTF-8/BOM are supported, and empty cells remain missing measurements:

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

Category charts accept 1–40 categories and 1–6 series; XY charts allow at most 500 points per series. Readable capacity depends on panel dimensions; dense bars are rejected and need separate pages. `x_axis.label_interval` sets category-tick spacing; otherwise width determines sparse ticks. `x_axis/y_axis.font_size` accepts 9–18pt. `title` identifies axis units. Value axes support `min/max/major_unit/number_format`. Horizontal bars also configure their value axis through `y_axis`. Column, bar and area axes must include zero and cannot hide measured values or stacked totals.

`number_format` uses Excel formatting; `series[].color` is a six-digit RGB value. `data_labels` controls numeric labels. Percentage stacks retain source counts, use a 0–1 axis displayed as 0–100%, and omit count labels by default. Explicit labels display source counts; percentage formatting belongs only in `y_axis.number_format`. Pie/donut charts show percentages. `sort` accepts `ascending/descending` for single-series `column/bar`; `highlight` identifies existing categories. Cross-page comparisons must explicitly preserve series colors, ranges and units.

Validation rejects mismatched lengths, nonnumeric values, NaN/Infinity, entirely missing series, invalid bubble sizes, malformed CSV, mixed inline/CSV input and axes hiding data. Missing measurements are not filled with zero. Invalid specifications or excess layout density leave existing output untouched.

The independent example covers all 12 chart types, sorting, highlighting, gaps, CSV, and two-/four-chart panels. All values are labeled example data:

```bash
python3 build_deck.py examples/chart_report.json output/图表能力示例_V0.1.pptx
python3 quality_check.py output/图表能力示例_V0.1.pptx
python3 check.py output/图表能力示例_V0.1.pptx
python3 render_ppt.py output/图表能力示例_V0.1.pptx --outdir output/chart-review
python3 -m unittest discover -s . -p 'test_*.py' -q
```

`examples/chart_report.expected.json` is a keyless CLI-output snapshot checking visible text, chart types, series names and values, plus XY coordinates and bubble sizes. Checkers do not parse internal chart-label layouts; rendered pages still need inspection.
