import sys, os
sys.path.insert(0, "/home/rx01334/ppt-assistant")
import vision_check
checks = [
 ("cover.jpg", "城市街头骑行电动踏板车/电摩"),
 ("rider.jpg", "男性骑电动踏板车通勤"),
 ("ebike.jpg", "电动自行车（两轮、带脚踏）"),
 ("emoto.jpg", "踏板摩托车/电摩"),
 ("emoto2.jpg", "骑电动踏板车/摩托、带头盔"),
 ("motor.jpg", "车轮/轮毂特写"),
 ("showroom.jpg", "自行车/电动车专卖店展厅"),
 ("charging.jpg", "电动车充电"),
]
for fn, kw in checks:
    p = os.path.join("commute_ebike/assets", fn)
    try:
        r = vision_check.ask(p, f"这张图片的内容是什么？用一句话概括，并判断是否贴合主题「{kw}」（只答：贴合/勉强/不贴合，再补一句理由）。")
        print(f"### {fn} [{kw}]\n{r.strip()}\n")
    except Exception as e:
        print(f"### {fn} ERROR {type(e).__name__} {e}\n")
