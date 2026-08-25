#!/usr/bin/env python3
"""生成一组柔和暖色主题图（无真人/无AI插画）：渐变 + 爱心 + 光晕 + 圆点，色调多样。"""
import math, random
from PIL import Image, ImageDraw

def _lerp(c0, c1, t):
    return tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))

def _gradient(w, h, stops):
    img = Image.new('RGB', (w, h))
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / w) * 0.55 + (y / h) * 0.45
            col = stops[-1][0]
            for i in range(len(stops) - 1):
                c0, p0 = stops[i]; c1, p1 = stops[i + 1]
                if t <= p0:
                    col = c0; break
                if t <= p1:
                    col = _lerp(c0, c1, (t - p0) / (p1 - p0) if p1 > p0 else 0); break
            px[x, y] = col
    return img

def _heart_points(cx, cy, s):
    pts = []
    for i in range(160):
        a = i / 160 * 2 * math.pi
        x = 16 * math.sin(a) ** 3
        y = 13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)
        pts.append((cx + x * s, cy - y * s))
    return pts

def _draw_heart(d, cx, cy, s, fill):
    d.polygon(_heart_points(cx, cy, s), fill=fill)

def make(path, w, h, stops, heart=((0.6, 0.4), 22, (255, 226, 218, 130)), glow=None, seed=7):
    img = _gradient(w, h, stops)
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    if glow:
        gx, gy, gr, gcol, galpha = glow
        for k, a in ((1.0, galpha), (0.7, int(galpha * 0.7)), (0.45, int(galpha * 0.5))):
            d.ellipse([gx - gr * k, gy - gr * k, gx + gr * k, gy + gr * k], fill=gcol + (a,))
    (hx, hy), hs, hc = heart
    _draw_heart(d, int(hx * w), int(hy * h), hs, hc)
    random.seed(seed)
    circles = []
    for _ in range(9):
        cx = random.randint(0, w); cy = random.randint(0, h); r = random.randint(14, 46)
        circles.append((cx, cy, r, (255, 232, 216), random.randint(26, 50)))
    img = _soft_circles(img, circles)
    img = Image.alpha_composite(img, lay).convert('RGB')
    img.save(path, 'JPEG', quality=92)
    print('saved', path)

def _soft_circles(img, circles):
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for (cx, cy, r, color, alpha) in circles:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (alpha,))
    return Image.alpha_composite(img.convert('RGBA'), ov)

if __name__ == '__main__':
    OUT = '/home/rx01334/ppt-assistant/assets/'
    W, H = 1200, 800
    variants = [
        ('rose',  [((232,148,156),0.0), ((240,176,168),0.5), ((250,224,205),1.0)], ((0.55,0.38),24,(255,230,220,135)), None),
        ('peach', [((240,164,132),0.0), ((247,199,162),0.5), ((253,233,205),1.0)], ((0.4,0.45),26,(255,236,220,140)), None),
        ('coral', [((238,132,132),0.0), ((247,178,150),0.48), ((252,222,196),1.0)], ((0.68,0.42),28,(255,222,200,135)), None),
        ('blush', [((240,150,164),0.0), ((248,190,182),0.52), ((254,232,214),1.0)], ((0.35,0.4),22,(255,232,220,140)), None),
        ('apricot',[((240,170,120),0.0), ((249,203,150),0.5), ((254,234,205),1.0)], ((0.6,0.5),24,(255,240,216,140)), None),
        ('sunset', [((226,120,140),0.0), ((244,158,140),0.45), ((252,210,170),1.0)], ((0.5,0.38),30,(255,214,184,150)), None),
        ('glow',   [((222,150,150),0.0), ((240,180,158),0.5), ((252,224,200),1.0)], ((0.6,0.45),22,(255,224,205,140)), (0.72,0.3,140,(255,240,215),90)),
        ('mauve',  [((214,150,168),0.0), ((236,180,182),0.5), ((250,224,210),1.0)], ((0.45,0.42),26,(255,232,222,140)), None),
    ]
    for name, stops, heart, glow in variants:
        make(OUT + f'theme_{name}.jpg', W, H, stops, heart=heart, glow=glow, seed=len(name))
