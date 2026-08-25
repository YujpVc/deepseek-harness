import sys, os
sys.path.insert(0, "/home/rx01334/ppt-assistant")
import vision_check
Q = "你是国际会议PPT的严格评审。请给这张页面打分（0-10），重点看：1)饱满度（内容是否填满、有无大片空白）；2)版式是否美观有变化、不单调；3)有无文字溢出、遮挡、重叠、被截断；4)配色对比是否清晰。先给一个总分（格式：X/10），再用一句话指出最需要改进的一点（若很好就说'无明显问题'）。"
pages = sorted(f for f in os.listdir("commute_ebike/render") if f.endswith('.png'))
for p in pages:
    fp = os.path.join("commute_ebike/render", p)
    try:
        r = vision_check.ask(fp, Q)
        print(f"### {p}\n{r.strip()}\n")
    except Exception as e:
        print(f"### {p} ERROR {type(e).__name__} {e}\n")
