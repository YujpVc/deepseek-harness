#!/usr/bin/env python3
"""Build an editable deck from JSON and explicit assets, independent of cwd.

Relative image paths resolve beside the specification. Layout and rendering
code live in this package; workspace scripts are never imported or executed.
"""
from __future__ import annotations

import argparse
import io
import json
import math
from pathlib import Path

from PIL import Image, ImageOps
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
from pptx.opc.constants import RELATIONSHIP_TYPE as RT

LAYOUTS = {"cover", "cards", "process", "comparison", "table", "chart",
           "image_split", "image_grid", "closing"}
THEMES = {
    "midnight": {"bg": "0B1324", "panel": "17243B", "text": "F7FBFF",
                 "muted": "B2C2D9", "accent": "48CAE4"},
    "paper": {"bg": "F4F6FA", "panel": "FFFFFF", "text": "15253F",
              "muted": "4D627A", "accent": "176C88"},
}


def validate(spec: dict, base: Path) -> None:
    """Reject unsupported layouts, missing assets and content beyond capacity."""
    if not isinstance(spec, dict) or not isinstance(spec.get("meta"), dict):
        raise ValueError("meta must be an object")
    if not spec["meta"].get("title"):
        raise ValueError("meta.title is required")
    if spec["meta"].get("theme", "midnight") not in THEMES:
        raise ValueError("meta.theme must be midnight or paper")
    slides = spec.get("slides")
    if not isinstance(slides, list) or not slides:
        raise ValueError("slides must be a non-empty array")
    for index, slide in enumerate(slides, 1):
        if not isinstance(slide, dict) or slide.get("layout") not in LAYOUTS:
            raise ValueError(f"slide {index}: unsupported layout")
        layout = slide["layout"]
        if not slide.get("title") and layout not in {"cover", "closing"}:
            raise ValueError(f"slide {index}: title is required")
        if layout in {"cards", "process", "comparison", "image_grid"}:
            items = slide.get("items")
            minimum, maximum = (2, 2) if layout == "comparison" else (2, 4)
            if not isinstance(items, list) or not minimum <= len(items) <= maximum:
                raise ValueError(f"slide {index}: items requires {minimum}–{maximum} entries")
            if any(not isinstance(item, dict) or not item.get("title") for item in items):
                raise ValueError(f"slide {index}: each item requires a title")
        assets = [slide] if layout in {"cover", "image_split"} else []
        if layout == "image_grid":
            assets = slide["items"]
        for asset in assets:
            image = asset.get("image")
            if not image and layout != "cover":
                raise ValueError(f"slide {index}: image is required")
            if image:
                path = (base / image).resolve()
                if not path.is_file():
                    raise ValueError(f"slide {index}: image not found: {path}")
                with Image.open(path) as picture:
                    picture.verify()
        if layout == "table":
            headers, rows = slide.get("headers"), slide.get("rows")
            if (not isinstance(headers, list) or not 2 <= len(headers) <= 5
                    or not isinstance(rows, list) or not 1 <= len(rows) <= 6
                    or any(not isinstance(row, list) or len(row) != len(headers) for row in rows)):
                raise ValueError(f"slide {index}: table requires 2–5 columns and 1–6 complete rows")
        if layout == "chart":
            chart = slide.get("chart", {})
            categories, series = chart.get("categories"), chart.get("series")
            if (chart.get("kind", "column") not in {"column", "bar", "line"}
                    or not isinstance(categories, list) or not 2 <= len(categories) <= 8
                    or not isinstance(series, list) or not 1 <= len(series) <= 3):
                raise ValueError(f"slide {index}: chart requires 2–8 categories and 1–3 series")
            for item in series:
                values = item.get("values", [])
                if (not item.get("name") or len(values) != len(categories)
                        or any(type(v) not in {int, float} or not math.isfinite(v) for v in values)):
                    raise ValueError(f"slide {index}: chart series requires finite numeric values")


class DeckBuilder:
    """Own presentation state and layout primitives for one specification."""

    def __init__(self, spec: dict, base: Path):
        self.meta = spec["meta"]
        self.base = base
        self.colors = THEMES[self.meta.get("theme", "midnight")]
        self.font = self.meta.get("font", "Noto Sans CJK SC")
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = Inches(13.333333), Inches(7.5)

    def box(self, slide, x, y, w, h, color="panel", rounded=False):
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(h))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor.from_string(self.colors[color])
        shape.line.fill.background()
        return shape

    def text(self, slide, value, x, y, w, h, size=21, color="text", bold=False):
        """Fit text conservatively; reject dense content instead of shrinking it."""
        value = str(value)
        lines = sum(max(1, math.ceil(sum(1 if ord(c) > 0x2E80 else .55 for c in line)
                                    / (w * 72 / size))) for line in value.split("\n"))
        if lines * size * 1.25 + max(0, len(value.split("\n")) - 1) * 8 > h * 72:
            raise ValueError(f"text exceeds layout capacity; split or shorten: {value[:60]}")
        shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        frame = shape.text_frame
        frame.word_wrap = True
        frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
        for index, line in enumerate(value.split("\n")):
            paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
            paragraph.space_after = Pt(8)
            paragraph.line_spacing = 1.2
            run = paragraph.add_run()
            run.text = line
            run.font.name, run.font.size, run.font.bold = self.font, Pt(size), bold
            run.font.color.rgb = RGBColor.from_string(self.colors[color])
            east_asian = run._r.get_or_add_rPr().makeelement(qn("a:ea"), {"typeface": self.font})
            run._r.get_or_add_rPr().append(east_asian)
        return shape

    def picture(self, slide, filename, x, y, w, h):
        with Image.open(self.base / filename) as source:
            picture = ImageOps.exif_transpose(source).convert("RGB")
            payload = io.BytesIO()
            picture.save(payload, "JPEG", quality=95)
            payload.seek(0)
            ratio = min(w / picture.width, h / picture.height)
            width, height = picture.width * ratio, picture.height * ratio
        slide.shapes.add_picture(payload, Inches(x + (w - width) / 2),
                                Inches(y + (h - height) / 2), Inches(width), Inches(height))

    def new(self, page, index):
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = RGBColor.from_string(self.colors["bg"])
        self.text(slide, page.get("title", self.meta["title"]), .6, .38, 12.1, .95, 30, bold=True)
        if page.get("subtitle"):
            self.text(slide, page["subtitle"], .6, 1.35, 12.1, .65, 17, "muted")
        self.text(slide, self.meta["title"], .6, 7.06, 10.8, .24, 10, "muted")
        self.text(slide, f"{index:02}", 12.0, 7.02, .7, .3, 12, "muted")
        slide.notes_slide.notes_text_frame.text = page.get("notes", "")
        return slide

    def card(self, slide, item, x, y, w, h, number=None):
        self.box(slide, x, y, w, h, rounded=True)
        offset = .25
        if number is not None:
            self.text(slide, f"{number:02}", x + .25, y + .25, w - .5, .55, 28, "accent", True)
            offset = 1.0
        self.text(slide, item["title"], x + .25, y + offset, w - .5, .85, 23, "accent", True)
        self.text(slide, item.get("body", ""), x + .25, y + offset + 1.0,
                  w - .5, h - offset - 1.25, 20)

    def compose(self, slide, page):
        layout = page["layout"]
        if layout in {"cover", "closing"}:
            image = page.get("image")
            width = 7.1 if image else 11.7
            self.text(slide, page.get("body", self.meta.get("subtitle", "")),
                      .8, 2.35, width, 2.5, 32, "accent", True)
            self.text(slide, self.meta.get("author", ""), .8, 5.5, width, .7, 20, "muted")
            if image:
                self.picture(slide, image, 8.3, 1.95, 4.3, 4.75)
        elif layout in {"cards", "comparison"}:
            items = page["items"]
            columns = len(items) if len(items) <= 3 else 2
            rows = math.ceil(len(items) / columns)
            width = (12.1 - .25 * (columns - 1)) / columns
            height = (4.55 - .25 * (rows - 1)) / rows
            for index, item in enumerate(items):
                self.card(slide, item, .6 + (index % columns) * (width + .25),
                          2.05 + (index // columns) * (height + .25), width, height)
        elif layout == "process":
            items = page["items"]
            width = (12.1 - .4 * (len(items) - 1)) / len(items)
            for index, item in enumerate(items):
                x = .6 + index * (width + .4)
                self.card(slide, item, x, 2.25, width, 4.1, index + 1)
                if index < len(items) - 1:
                    shape = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x + width + .07),
                                                  Inches(3.9), Inches(.25), Inches(.45))
                    shape.fill.solid()
                    shape.fill.fore_color.rgb = RGBColor.from_string(self.colors["accent"])
                    shape.line.fill.background()
        elif layout == "image_split":
            self.picture(slide, page["image"], .6, 2.05, 7.1, 4.55)
            self.box(slide, 8.0, 2.05, 4.7, 4.55, rounded=True)
            self.text(slide, page.get("body", ""), 8.3, 2.4, 4.1, 3.8, 22)
        elif layout == "image_grid":
            items = page["items"]
            rows = math.ceil(len(items) / 2)
            height = (4.55 - .2 * (rows - 1)) / rows
            for index, item in enumerate(items):
                x, y = .6 + (index % 2) * 6.2, 2.05 + (index // 2) * (height + .2)
                self.picture(slide, item["image"], x, y, 5.9, height - .6)
                self.text(slide, item["title"], x, y + height - .48, 5.9, .45, 18, "accent", True)
        elif layout == "chart":
            data = CategoryChartData()
            data.categories = page["chart"]["categories"]
            for item in page["chart"]["series"]:
                data.add_series(item["name"], item["values"])
            kind = {"column": XL_CHART_TYPE.COLUMN_CLUSTERED, "bar": XL_CHART_TYPE.BAR_CLUSTERED,
                    "line": XL_CHART_TYPE.LINE}[page["chart"].get("kind", "column")]
            self.box(slide, .6, 2.05, 12.1, 4.55)
            chart = slide.shapes.add_chart(kind, Inches(.85), Inches(2.2),
                                          Inches(11.6), Inches(4.1), data).chart
            chart.has_legend = len(page["chart"]["series"]) > 1
            for axis in (chart.category_axis, chart.value_axis):
                axis.tick_labels.font.name = self.font
                axis.tick_labels.font.size = Pt(16)
                axis.tick_labels.font.color.rgb = RGBColor.from_string(self.colors["text"])
            for index, series in enumerate(chart.series):
                color = RGBColor.from_string(self.colors["accent"] if index == 0 else self.colors["muted"])
                series.format.fill.solid()
                series.format.fill.fore_color.rgb = color
                series.format.line.color.rgb = color
            if chart.has_legend:
                chart.legend.font.size = Pt(14)
                chart.legend.font.color.rgb = RGBColor.from_string(self.colors["text"])
        elif layout == "table":
            headers, rows = page["headers"], page["rows"]
            table = slide.shapes.add_table(len(rows) + 1, len(headers), Inches(.6), Inches(2.1),
                                           Inches(12.1), Inches(4.4)).table
            for row_index, row in enumerate([headers] + rows):
                for column_index, value in enumerate(row):
                    cell = table.cell(row_index, column_index)
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor.from_string(self.colors["accent" if row_index == 0 else "panel"])
                    cell.text = str(value)
                    for paragraph in cell.text_frame.paragraphs:
                        paragraph.font.name = self.font
                        paragraph.font.size = Pt(18)
                        paragraph.font.bold = row_index == 0
                        paragraph.font.color.rgb = RGBColor.from_string(self.colors["bg" if row_index == 0 else "text"])
        if page.get("source"):
            self.text(slide, page["source"], .6, 6.7, 12.1, .27, 11, "muted")


def build(spec: dict, base: Path, output: Path) -> None:
    """Validate and build; only spec assets are read and output is written."""
    validate(spec, base)
    builder = DeckBuilder(spec, base)
    for index, page in enumerate(spec["slides"], 1):
        slide = builder.new(page, index)
        builder.compose(slide, page)
    output.parent.mkdir(parents=True, exist_ok=True)
    builder.prs.save(str(output))


def _template_page_map(spec: dict, base: Path, template: Presentation) -> list[dict]:
    """Validate a one-to-one page map for template-preserving generation."""
    pages = spec.get("slides")
    if not isinstance(pages, list) or len(pages) != len(template.slides):
        raise ValueError("template mode requires one slide spec for every template slide")
    seen: set[int] = set()
    for index, page in enumerate(pages, 1):
        if not isinstance(page, dict):
            raise ValueError(f"slide {index}: template page spec must be an object")
        source_index = page.get("template_slide")
        if type(source_index) is not int or not 1 <= source_index <= len(template.slides):
            raise ValueError(f"slide {index}: template_slide must be a valid 1-based slide number")
        if source_index in seen:
            raise ValueError(f"slide {index}: template_slide {source_index} is used more than once")
        seen.add(source_index)
        for field in ("text", "images"):
            values = page.get(field, {})
            if not isinstance(values, dict) or any(not isinstance(k, str) for k in values):
                raise ValueError(f"slide {index}: {field} must map shape names to values")
        slide = template.slides[source_index - 1]
        shapes = {shape.name: shape for shape in slide.shapes}
        for name, value in page.get("text", {}).items():
            if name not in shapes or not getattr(shapes[name], "has_text_frame", False):
                raise ValueError(f"slide {index}: text target is not a text shape: {name}")
            if not isinstance(value, str):
                raise ValueError(f"slide {index}: text for {name} must be a string")
        for name, filename in page.get("images", {}).items():
            if name not in shapes or shapes[name].shape_type != 13:
                raise ValueError(f"slide {index}: image target is not a picture shape: {name}")
            image_path = (Path(filename) if Path(filename).is_absolute() else base / filename).resolve()
            if not image_path.is_file():
                raise ValueError(f"slide {index}: image not found: {image_path}")
            with Image.open(image_path) as picture:
                picture.verify()
        notes = page.get("notes", "")
        if not isinstance(notes, str):
            raise ValueError(f"slide {index}: notes must be a string")
    if seen != set(range(1, len(template.slides) + 1)):
        raise ValueError("template_slide values must cover every template slide exactly once")
    return pages


def _replace_text(shape, value: str) -> None:
    """Replace text while retaining the first run's font and paragraph styling."""
    frame = shape.text_frame
    runs = [run for paragraph in frame.paragraphs for run in paragraph.runs]
    if runs:
        runs[0].text = value
        for run in runs[1:]:
            run.text = ""
        for paragraph in frame.paragraphs[1:]:
            for run in paragraph.runs:
                run.text = ""
    else:
        frame.paragraphs[0].add_run().text = value


def build_from_template(spec: dict, base: Path, template_path: Path, output: Path) -> None:
    """Edit named text and picture shapes without rebuilding template slides."""
    template = Presentation(str(template_path))
    pages = _template_page_map(spec, base, template)
    for page in pages:
        slide = template.slides[page["template_slide"] - 1]
        shapes = {shape.name: shape for shape in slide.shapes}
        for name, value in page.get("text", {}).items():
            _replace_text(shapes[name], value)
        for name, filename in page.get("images", {}).items():
            shape = shapes[name]
            image_path = (Path(filename) if Path(filename).is_absolute() else base / filename).resolve()
            image_part, _ = slide.part.get_or_add_image_part(str(image_path))
            blip = shape._element.blipFill.blip
            blip.set(qn("r:embed"), slide.part.relate_to(image_part, RT.IMAGE))
        if "notes" in page:
            slide.notes_slide.notes_text_frame.text = page["notes"]
    output.parent.mkdir(parents=True, exist_ok=True)
    template.save(str(output))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--template", type=Path,
                        help="reuse every slide from this PPTX, replacing named text/image shapes")
    args = parser.parse_args()
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        base = args.spec.resolve().parent
        if args.template:
            build_from_template(spec, base, args.template.resolve(), args.output.resolve())
        else:
            build(spec, base, args.output.resolve())
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, f"build_deck: {exc}\n")
    print(f"Generated {len(spec['slides'])} editable slides: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
