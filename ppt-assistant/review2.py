#!/usr/bin/env python3
import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vision_check import ask

Q = ("你是国际会议级严格设计评审。请用中文简短点评这张医疗学术PPT页面，重点：1)文字溢出/截断/遮挡；"
     "2)单字孤行(行末只剩1个汉字)；3)次要文字对比度；4)版式均衡/大片空白；5)配色是否统一(青绿+琥珀)。"
     "最后给一句评分(满分10分)，格式'评分:X/10'，并列出需修复问题(无则写'无明显问题')。")

d = os.path.join(HERE, 'render')
pages = [f'pg-{i:02d}.png' for i in range(7, 21)]
for p in pages:
    path = os.path.join(d, p)
    for attempt in range(2):
        try:
            r = ask(path, Q)
            print(f"\n===== {p} =====")
            print(r.strip())
            break
        except Exception as e:
            if attempt == 1:
                print(f"\n===== {p} ===== ERR {type(e).__name__}: {e}")
            else:
                time.sleep(3)
    sys.stdout.flush()
