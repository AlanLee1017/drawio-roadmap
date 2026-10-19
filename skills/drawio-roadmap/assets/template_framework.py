#!/usr/bin/env python3
# 研究框架图模板 —— 三栏：思路链(块箭头竖链) | 内容(题名加粗) | 方法(实线框)
# 分层用虚线组框只包"内容+方法"两列；层名白底骑框上边线居中；层间加宽间隔
import os
from drawio_common import (Sheet, write, val, HDR, BOXC, LBL, COLLB,
                           EDGE_H, FRAME, FONT)

PAGE_W = 800
s = Sheet()
LX, LW = 46, 120     # 思路列
CX, CW = 210, 300    # 内容列
MX, MW = 550, 210    # 方法列
HDRY, HDRH = 20, 36
ROW_H, VGAP = 92, 34
Y0 = HDRY + HDRH + 32
LAYER_GAP = 34       # 层间额外间隔（让两个虚线框明确隔开）

s.node("h1", "研究思路", LX, HDRY, LW, HDRH, HDR + "fontSize=16;fontStyle=1;")
s.node("h2", "研究内容", CX, HDRY, CW, HDRH, HDR + "fontSize=16;fontStyle=1;")
s.node("h3", "研究方法", MX, HDRY, MW, HDRH, HDR + "fontSize=16;fontStyle=1;")
s.edge("he1", "h1", "h2", EDGE_H)
s.edge("he2", "h2", "h3", EDGE_H)

# 层划分：第几行起属于第二层（无分层则 LAYER_AT=None 且 GROUPS 为空）
LAYER_AT = 3
GROUPS = [(0, 2, "上半层名"), (3, 4, "下半层名")]

def y_of(i):
    return Y0 + i * (ROW_H + VGAP) + (LAYER_GAP if LAYER_AT and i >= LAYER_AT else 0)

def group_frame(id_, i0, i1, label):
    y0, y1 = y_of(i0) - 14, y_of(i1) + ROW_H + 14
    gx, gw = CX - 14, MX + MW + 14 - (CX - 14)
    s.node(id_, "", gx, y0, gw, y1 - y0, FRAME)
    s.node(id_ + "t", label, gx + gw // 2 - 70, y0 - 13, 140, 26,
           "text;html=1;align=center;verticalAlign=middle;fontSize=16;fontStyle=1;"
           "strokeColor=none;fillColor=#ffffff;" + FONT)

for gi, (i0, i1, lb) in enumerate(GROUPS):
    group_frame(f"g{gi}", i0, i1, lb)

# rows = (思路环节, 内容题名, 内容描述, 方法)
rows = [
    ("环节一", "任务一：标题", "两行内容\n第二行", "方法要点\n第二行"),
    ("环节二", "任务二：标题", "内容", "方法"),
    ("环节三", "任务三：标题", "内容", "方法"),
    ("环节四", "任务四：标题", "内容", "方法"),
    ("环节五", "任务五：标题", "内容", "方法"),
]
for i, (idea, tname, tdesc, method) in enumerate(rows):
    y = y_of(i)
    s.node(f"l{i}", idea, LX, y + (ROW_H - 48) // 2, LW, 48, LBL + "fontSize=15;")
    s.nodev(f"c{i}", "&lt;b&gt;" + val(tname) + "&lt;/b&gt;&lt;br&gt;" + val(tdesc),
            CX, y, CW, ROW_H, BOXC + "fontSize=14;")
    s.node(f"m{i}", method, MX, y, MW, ROW_H, BOXC + "fontSize=14;")
    s.edge(f"r{i}a", f"l{i}", f"c{i}", EDGE_H)
    s.edge(f"r{i}b", f"c{i}", f"m{i}", EDGE_H)
    if i:
        gap = y - (y_of(i - 1) + ROW_H)
        s.barrow(f"ba{i}", LX + LW // 2, y_of(i - 1) + ROW_H + (gap - 24) // 2, 30, 24)
s.barrow("ba0", LX + LW // 2, Y0 - VGAP + 5, 30, 24)

PAGE_H = y_of(len(rows) - 1) + ROW_H + 30

if __name__ == "__main__":
    write(s.doc("framework", "总体研究框架", PAGE_W, PAGE_H),
          os.path.dirname(os.path.abspath(__file__)), 'framework.drawio')
    print('page', PAGE_W, 'x', PAGE_H)
