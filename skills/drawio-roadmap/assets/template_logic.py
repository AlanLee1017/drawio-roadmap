#!/usr/bin/env python3
# 构思逻辑图模板 —— 问题层级树：前提括线 → 核心问题 → 并列子问题 → 综合问题 → 成果
# 结构可按需增删层；括线/漏斗用 s.fan_out / s.fan_in
import os
from drawio_common import (Sheet, write, val, HDR, BOXC, COLLB,
                           EDGE_S, LINE)

PAGE_W = 860
s = Sheet()

# ---- 第一层：括注 + 括线 → 前提框 ----
s.node("cap", "现实背景与双重约束", 280, 14, 300, 22, COLLB + "fontSize=15;")
s.node("p1", "前提一（需求侧）", 110, 56, 300, 60, BOXC + "fontSize=14;")
s.node("p2", "前提二（供给侧）", 450, 56, 300, 60, BOXC + "fontSize=14;")
s.fan_out("a", "cap", [("p1", 260), ("p2", 600)], 46)

# ---- 第二层：核心科学问题（前提斜线汇入，汇入点对称错开） ----
s.nodev("q", "&lt;b&gt;核心科学问题&lt;/b&gt;&lt;br&gt;" + val("……一句话总问题……"),
        110, 150, 640, 88, HDR + "fontSize=16;")
s.edge("pq1", "p1", "q", EDGE_S.replace("entryX=0.5;", "entryX=0.42;"))
s.edge("pq2", "p2", "q", EDGE_S.replace("entryX=0.5;", "entryX=0.58;"))

# ---- 第三层：并列子问题（等高顶对齐等间距，实线横连=并列） ----
s.barrow("ba1", PAGE_W // 2, 246)
r1y, qw, qxs = 284, 250, [40, 305, 570]
qs = [("q1", "子问题一\n（任务一）"), ("q2", "子问题二\n（任务二）"),
      ("q3", "子问题三\n（任务三）")]
for i, (id_, txt) in enumerate(qs):
    s.node(id_, txt, qxs[i], r1y, qw, 92, BOXC + "fontSize=14;")
for a, b in [("q1", "q2"), ("q2", "q3")]:
    s.edge("ch" + a + b, a, b, LINE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")

# ---- 第四层：综合问题（上层直线斜汇入；垂直关系尽量对准中心保直线） ----
r2y = r1y + 92 + 48
s.node("q4", "综合问题一\n（任务四）", 142, r2y, 300, 92, BOXC + "fontSize=14;")
s.node("q5", "综合问题二\n（任务五）", 545, r2y, 300, 92, BOXC + "fontSize=14;")
s.edge("cd1", "q1", "q4", EDGE_S.replace("entryX=0.5;", "entryX=0.38;"))
s.edge("cd2", "q2", "q4", EDGE_S.replace("entryX=0.5;", "entryX=0.62;"))
s.edge("cd3", "q3", "q5", EDGE_S)          # q5 中心 695 = q3 中心 695，严格垂直
s.edge("ch45", "q4", "q5", LINE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")

# ---- 第五层：成果（漏斗收口 → 块箭头 → 成果带） ----
cy = r2y + 92 + 16
cv = s.fan_in("b", [("q4", 292), ("q5", 695)], bar_y=cy, cx=PAGE_W // 2)
s.barrow("ba2", PAGE_W // 2, cy + 6)
gy = cy + 6 + 22 + 14
s.nodev("goal", "&lt;b&gt;预期成果&lt;/b&gt;&lt;br&gt;" + val("成果A · 成果B · 成果C"),
        100, gy, 660, 60, HDR + "fontSize=15;")

PAGE_H = gy + 60 + 18

if __name__ == "__main__":
    write(s.doc("logic", "研究构思与逻辑框架", PAGE_W, PAGE_H),
          os.path.dirname(os.path.abspath(__file__)), 'logic.drawio')
    print('page', PAGE_W, 'x', PAGE_H)
