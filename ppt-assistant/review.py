#!/usr/bin/env python3
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vision_check import ask

Q = ("你是国际会议级的严格设计评审。请用中文点评这张医疗学术PPT页面，重点检查："
     "1) 文字是否有溢出、被截断、被图形遮挡；2) 标题/要点是否出现单字孤行（一行末尾只剩1个汉字）；"
     "3) 次要文字在浅色背景上是否对比度足够（不能太淡）；4) 版式是否均衡、有没有大片空白或内容挤在一起；"
     "5) 插图是否切题、自然、不突兀（有没有像硬贴上去的）；6) 配色是否统一（主色青绿+琥珀，不要出现杂色）。"
     "最后给一句总分(满分10分)，格式：'评分:X/10'，并列出需要修复的问题点（无问题则写'无明显问题'）。")

d = os.path.join(HERE, 'render')
pages = sorted(f for f in os.listdir(d) if f.startswith('pg-') and f.endswith('.png'))
for p in pages:
    path = os.path.join(d, p)
    try:
        r = ask(path, Q)
        print(f"\n===== {p} =====")
        print(r.strip())
    except Exception as e:
        print(f"\n===== {p} ===== ERR {type(e).__name__}: {e}")
    sys.stdout.flush()
