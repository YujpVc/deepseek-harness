#!/usr/bin/env python3
"""批量用 terra 视觉模型审查渲染页面，重点查文字溢出/遮挡/图片变形/留白。"""
import sys, time, json
from vision_check import ask

Q = ("你是国际会议PPT终审评委。请用中文，针对这张16:9幻灯片指出【具体问题】："
     "1) 任何文字溢出文本框或被色块/图片遮挡；2) 图片是否拉伸变形/裁切生硬/空白过多；"
     "3) 版式是否失衡、元素是否互相重叠；4) 配色是否协调。"
     "若页面很好请说『无明显问题』。最多4条，每条附位置(如左下/右上)。")

def check(pg):
    path = f'render/pg-{pg:02d}.png'
    for attempt in range(3):
        try:
            return ask(path, Q)
        except Exception as e:
            print(f'  pg{pg} attempt{attempt+1} ERR {type(e).__name__}', flush=True)
            time.sleep(3)
    return f'[FAILED pg{pg}]'

def main():
    pages = [int(a) for a in sys.argv[1:]] or list(range(1, 21))
    out = {}
    for pg in pages:
        print(f'== pg{pg} ==', flush=True)
        r = check(pg)
        out[pg] = r
        print(r, flush=True)
    json.dump(out, open('vision_results.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('saved vision_results.json')

if __name__ == '__main__':
    main()
