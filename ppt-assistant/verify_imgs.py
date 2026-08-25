import sys, os
sys.path.insert(0, "/home/rx01334/ppt-assistant")
import vision_check
checks = [
 ("cover.jpg", "国产电动自行车通勤骑行"),
 ("ebike.jpg", "新国标电动自行车（两轮、有脚踏）"),
 ("emoto.jpg", "电动摩托车/踏板电动车"),
 ("emoto2.jpg", "电动摩托车街道骑行"),
 ("battery.jpg", "电动车锂电池组"),
 ("motor.jpg", "电动自行车轮毂电机"),
 ("helmet.jpg", "骑行头盔"),
 ("charging.jpg", "电动车充电"),
 ("rider.jpg", "骑电动车通勤的人（背影/剪影）"),
 ("showroom.jpg", "电动车专卖店展厅"),
]
for fn, kw in checks:
    p = os.path.join("commute_ebike/assets", fn)
    if not os.path.exists(p):
        print(f"### {fn} MISSING\n"); continue
    try:
        r = vision_check.ask(p, f"这张图片的内容是什么？请用一句话概括，并判断它是否贴合主题「{kw}」（只答：贴合 / 勉强 / 不贴合，再补一句理由）。")
        print(f"### {fn} [{kw}]\n{r.strip()}\n")
    except Exception as e:
        print(f"### {fn} ERROR {type(e).__name__} {e}\n")
