import sys, os
sys.path.insert(0, "/home/rx01334/ppt-assistant")
import image_fetch as m

jobs = [
 ("cover.jpg",   "electric scooter city"),
 ("rider.jpg",   "electric scooter rider"),
 ("ebike.jpg",   "electric bicycle"),
 ("emoto.jpg",   "electric scooter"),
 ("emoto2.jpg",  "electric motorcycle"),
 ("motor.jpg",   "bicycle wheel close up"),
 ("showroom.jpg","bicycle shop"),
 ("charging.jpg","ev charging station"),
]
for fn, kw in jobs:
    out = os.path.join("commute_ebike/assets", fn)
    try:
        ph = m.search_pexels(kw, per_page=2, orientation='landscape')
        if not ph:
            print(f"### {fn} [{kw}] NO RESULT"); continue
        # pick second result if first is same as a previous? just take first
        src = ph['src'].get('large2x') or ph['src'].get('large') or ph['src'].get('original')
        m._download(src, out, via_proxy=True)
        alt = ph.get('alt','')[:60]
        print(f"### {fn} [{kw}] -> {alt} | {os.path.getsize(out)}B")
    except Exception as e:
        print(f"### {fn} [{kw}] ERROR {type(e).__name__} {e}")
