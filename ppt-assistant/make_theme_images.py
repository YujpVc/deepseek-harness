#!/usr/bin/env python3
"""生成柔和暖色主题图（无真人/无AI插画）：清晰扁平爱心 + 干净渐变，避免模糊质感。"""
import math, random
from PIL import Image, ImageDraw


def _lerp(c0, c1, t):
    return tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))


def _gradient(w, h, stops, blend=0.5):
    img = Image.new('RGB', (w, h))
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / w) * blend + (y / h) * (1 - blend)
            col = stops[-1][0]
            for i in range(len(stops) - 1):
                c0, p0 = stops[i]
                c1, p1 = stops[i + 1]
                if t <= p0:
                    col = c0
                    break
                if t <= p1:
                    col = _lerp(c0, c1, (t - p0) / (p1 - p0) if p1 > p0 else 0)
                    break
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


def _soft_circles(img, circles):
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for (cx, cy, r, color, alpha) in circles:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (alpha,))
    return Image.alpha_composite(img.convert('RGBA'), ov)


def _cover(path, w, h):
    img = _gradient(w, h, [((222, 138, 140), 0.0), ((238, 170, 140), 0.42),
                           ((247, 202, 158), 0.72), ((253, 228, 200), 1.0)])
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    # 柔和太阳（同心圆光晕，右下，完整不裁切）
    sx, sy, sr = int(0.73 * w), int(0.52 * h), 170
    rings = [(1.0, 46, (255, 222, 196)), (0.72, 78, (255, 214, 184)),
             (0.48, 128, (255, 202, 170)), (0.30, 205, (255, 232, 208))]
    for (k, a, col) in rings:
        d.ellipse([sx - sr * k, sy - sr * k, sx + sr * k, sy + sr * k], fill=col + (a,))
    # 若干干净半透明圆点装饰
    random.seed(6)
    circles = []
    for _ in range(14):
        cx = random.randint(0, w); cy = random.randint(0, h); r = random.randint(14, 46)
        a = random.randint(18, 38)
        col = random.choice([(255, 238, 222), (255, 218, 200), (250, 182, 158)])
        circles.append((cx, cy, r, col, a))
    img = _soft_circles(img, circles)
    img = Image.alpha_composite(img, lay).convert('RGB')
    img.save(path, 'JPEG', quality=93)
    print('saved', path, (w, h))


def _card(path, w, h, stops, heart_pos):
    img = _gradient(w, h, stops)
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    _draw_heart(d, int(heart_pos[0] * w), int(heart_pos[1] * h), 22, (255, 226, 218, 130))
    # 少量干净圆点
    random.seed(7)
    circles = []
    for _ in range(7):
        cx = random.randint(0, w); cy = random.randint(0, h); r = random.randint(14, 42)
        circles.append((cx, cy, r, (255, 232, 216), random.randint(30, 55)))
    img = _soft_circles(img, circles)
    img = Image.alpha_composite(img, lay).convert('RGB')
    img.save(path, 'JPEG', quality=92)
    print('saved', path, (w, h))


if __name__ == '__main__':
    OUT = '/home/rx01334/ppt-assistant/assets/'
    _cover(OUT + 'theme_cover.jpg', 1920, 1080)
    _card(OUT + 'theme_card_a.jpg', 1200, 800,
          [((238, 156, 138), 0.0), ((247, 205, 178), 0.55), ((253, 236, 219), 1.0)],
          (0.62, 0.40))
    _card(OUT + 'theme_card_b.jpg', 1200, 800,
          [((224, 158, 120), 0.0), ((240, 190, 150), 0.5), ((251, 228, 208), 1.0)],
          (0.35, 0.42))
