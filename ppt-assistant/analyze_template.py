#!/usr/bin/env python3
"""解析模板 pptx 的结构：每页/每个版式的形状、文本、位置、字体、颜色。"""
import sys, os, glob
import xml.etree.ElementTree as ET

BASE = "/tmp/ppt_template_inspect/ppt"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

def local(tag):
    return tag.split('}')[-1]

def text_of(sp):
    """提取一个形状里的全部文本（按段落）。"""
    paras = []
    for txBody in sp.iter():
        if local(txBody.tag) != 'txBody':
            continue
        for p in txBody.findall(A + 'p'):
            runs = []
            for r in p.iter(A + 'r'):
                t = r.find(A + 't')
                if t is not None and t.text:
                    runs.append(t.text)
            if runs:
                paras.append(''.join(runs))
    return paras

def fonts_of(sp):
    fonts = set()
    for r in sp.iter(A + 'r'):
        rPr = r.find(A + 'rPr')
        if rPr is not None:
            for tag in ('latin', 'ea', 'cs'):
                e = rPr.find(A + tag)
                if e is not None and e.get('typeface'):
                    fonts.add(e.get('typeface'))
    return fonts

def colors_of(sp):
    colors = set()
    for el in sp.iter():
        srgb = el.get('srgbClr')
        if srgb:
            pass
    # proper way
    for srgb in sp.iter():
        if local(srgb.tag) == 'srgbClr':
            colors.add(srgb.get('val'))
    for scheme in sp.iter():
        if local(scheme.tag) == 'schemeClr':
            colors.add('scheme:' + (scheme.get('val') or '?'))
    return colors

def xfrm_of(sp):
    spPr = sp.find(P + 'spPr') or sp.find(A + 'spPr')
    if spPr is None:
        return None
    xfrm = spPr.find(A + 'xfrm')
    if xfrm is None:
        return None
    off = xfrm.find(A + 'off')
    ext = xfrm.find(A + 'ext')
    return (off.get('x'), off.get('y'), ext.get('cx'), ext.get('cy'))

def shape_kind(sp):
    # picture / chart / table / group vs plain shape
    nv = sp.find(P + 'nvSpPr') or sp.find(A + 'nvSpPr')
    return local(sp.tag)

def analyze_file(path):
    tree = ET.parse(path)
    root = tree.getroot()
    spTree = None
    for cSld in root.iter(P + 'cSld'):
        spTree = cSld.find(P + 'spTree')
        break
    if spTree is None:
        return []
    out = []
    for child in spTree:
        tag = local(child.tag)
        if tag in ('nvGrpSpPr', 'grpSpPr'):
            continue
        name_el = child.find('.//' + P + 'cNvPr')
        name = name_el.get('name') if name_el is not None else ''
        text = text_of(child)
        xfrm = xfrm_of(child)
        fonts = fonts_of(child)
        colors = colors_of(child)
        has_img = tag == 'pic' or (child.find('.//' + A + 'blip') is not None)
        has_chart = tag == 'graphicFrame' and (child.find('.//' + A + 'chart') is not None or child.find('.//{http://schemas.openxmlformats.org/drawingml/2006/chart}chart') is not None)
        out.append({
            'tag': tag, 'name': name, 'xfrm': xfrm,
            'text': text, 'fonts': sorted(fonts), 'colors': sorted(colors),
            'img': has_img, 'chart': has_chart,
        })
    return out

def dump_slides():
    files = sorted(glob.glob(os.path.join(BASE, 'slides', 'slide*.xml')),
                   key=lambda p: int(os.path.basename(p).replace('slide','').replace('.xml','')))
    for f in files:
        n = os.path.basename(f)
        print('=' * 70)
        print(f"### {n}")
        for item in analyze_file(f):
            if not item['text'] and not item['img'] and not item['chart']:
                continue
            txt = ' | '.join(item['text'])[:80] if item['text'] else ''
            extra = []
            if item['img']: extra.append('IMG')
            if item['chart']: extra.append('CHART')
            print(f"  [{item['tag']}] name={item['name']!r} xfrm={item['xfrm']} fonts={item['fonts']} colors={item['colors']} {'/'.join(extra)}")
            if txt:
                print(f"      text: {txt}")

def dump_layouts():
    files = sorted(glob.glob(os.path.join(BASE, 'slideLayouts', 'slideLayout*.xml')),
                   key=lambda p: int(os.path.basename(p).replace('slideLayout','').replace('.xml','')))
    print('\n' + '#' * 70)
    print('### SLIDE LAYOUTS (版式)')
    for f in files:
        n = os.path.basename(f)
        items = analyze_file(f)
        texts = [t for it in items for t in it['text']]
        print(f"  {n}: shapes={len(items)} text_sample={texts[:3]}")

if __name__ == '__main__':
    dump_slides()
    dump_layouts()
