#!/usr/bin/env python3
# 任务技术路线图模板 —— 行式布局：环节标签 → 内容容器 → 方法容器 → 阶段输出
# 用法：改 TASKS 数据 → python3 template_task.py → draw.io 导出 png/svg
import os
from drawio_common import (Sheet, write, val, HDR, BOXC, LBL, GROUP, COLLB,
                           EDGE_H, numlist, row_h)

PAGE_W = 860
KX, KW = 28, 96          # 环节列
CX, CW = 136, 286        # 研究内容列
MX, MW = 434, 286        # 研究方法列
OX, OW = 732, 100        # 阶段输出列
HDRY, HDRH = 18, 24
VGAP = 40
Y0 = HDRY + HDRH + 24


def build(task):
    s = Sheet()
    for x, w, t in [(KX, KW, "环节"), (CX, CW, "研究内容"),
                    (MX, MW, "研究方法"), (OX, OW, "阶段输出")]:
        s.node(f"h{x}", t, x, HDRY, w, HDRH, COLLB + "fontSize=15;")

    # 行高按内容自适应（消空白）
    row_hs = [row_h(c, m, CW, MW) for _, c, m, _ in task["rows"]]
    ys, acc = [], Y0
    for h in row_hs:
        ys.append(acc); acc += h + VGAP

    for i, (lbl, content, method, out) in enumerate(task["rows"]):
        y, rh = ys[i], row_hs[i]
        s.node(f"k{i}", lbl, KX, y, KW, rh, LBL + "fontSize=15;")
        s.node(f"c{i}", numlist(content), CX, y, CW, rh,
               GROUP + "verticalAlign=middle;align=left;fontSize=14;")
        s.node(f"m{i}", numlist(method), MX, y, MW, rh,
               GROUP + "verticalAlign=middle;align=left;fontSize=14;")
        s.node(f"o{i}", out, OX, y + (rh - 56) // 2, OW, 56, BOXC + "fontSize=14;")
        s.edge(f"e{i}a", f"k{i}", f"c{i}", EDGE_H)
        s.edge(f"e{i}b", f"c{i}", f"m{i}", EDGE_H)
        s.edge(f"e{i}c", f"m{i}", f"o{i}", EDGE_H)
        # 块箭头只画到倒数第二行（最后一行由底部收口箭头承接，别叠两个）
        if i < len(task["rows"]) - 1:
            s.barrow(f"ba{i}", KX + KW // 2, y + rh + (VGAP - 24) // 2, 30, 24)

    fy = ys[-1] + row_hs[-1] + 30
    s.barrow("baF", (KX + OX + OW) // 2, fy - 26, 30, 22)
    s.nodev("final", "&lt;b&gt;任务输出&lt;/b&gt;&lt;br&gt;" + val(task["final"]),
            KX, fy, OX + OW - KX, 56, HDR + "fontSize=15;")
    return s.doc(task["id"], task["title"], PAGE_W, fy + 56 + 20)


# ---- 数据：rows = (环节标签, 研究内容(；分隔并列项), 研究方法, 阶段输出) ----
TASKS = [
    dict(id="task1", title="任务一技术路线",
         rows=[
             ("环节一\n步骤A", "条目1；条目2", "方法1；方法2", "输出X"),
             ("环节二\n步骤B", "条目1；条目2；条目3", "方法1；方法2", "输出Y"),
             ("环节三\n步骤C", "条目1；条目2", "方法1", "输出Z"),
         ],
         final="任务整体输出物描述"),
]

if __name__ == "__main__":
    OUT = os.path.dirname(os.path.abspath(__file__))
    for t in TASKS:
        write(build(t), OUT, f'{t["id"]}.drawio')
