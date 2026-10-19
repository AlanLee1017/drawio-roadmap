#!/usr/bin/env python3
# drawio 公共样式与构造助手 —— 纯黑白 · Songti SC · 参考文档图式语言
import html, os

FONT = "fontFamily=Songti SC;"

# ---- 节点样式 ----
# 实心白底内容框
BOX = ("rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"
       "strokeWidth=1;fontSize=11;align=left;verticalAlign=middle;spacing=6;" + FONT)
# 居中内容框
BOXC = BOX.replace("align=left;", "align=center;")
# 加粗居中标题框（核心问题/成果等强调框）
HDR = ("rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"
       "strokeWidth=1;fontSize=12;align=center;verticalAlign=middle;spacing=6;" + FONT)
# 虚线圆角分组容器（装子框/列表）
GROUP = ("rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#ffffff;"
         "strokeColor=#000000;strokeWidth=1;dashed=1;dashPattern=4 4;"
         "fontSize=10;verticalAlign=top;align=center;spacing=9;" + FONT)
# 环节标签框（每行左侧）
LBL = ("rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"
       "strokeWidth=1;fontSize=11;fontStyle=1;align=center;verticalAlign=middle;spacing=4;" + FONT)
# 左竖脊（竖排文字）
SPINE = ("rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"
         "strokeWidth=1;fontSize=11;fontStyle=1;horizontal=0;"
         "align=center;verticalAlign=middle;spacing=4;" + FONT)
# 列头文字（无边框）
COLLB = ("text;html=1;align=center;verticalAlign=middle;fontSize=11;fontStyle=1;"
         "strokeColor=none;fillColor=none;" + FONT)
# 图内大标题
TITLE = ("text;html=1;align=center;verticalAlign=middle;fontSize=15;fontStyle=1;"
         "strokeColor=none;fillColor=none;" + FONT)
# 小注/图例
NOTE = ("text;html=1;align=left;verticalAlign=middle;fontSize=9;"
        "strokeColor=none;fillColor=none;" + FONT)
# 块箭头（主干流程）—— 白底黑边填充块箭头
BARROW = ("shape=singleArrow;direction=south;whiteSpace=wrap;html=1;"
          "fillColor=#ffffff;strokeColor=#000000;strokeWidth=1;" + FONT)
# 虚线外框
FRAME = ("rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;"
         "strokeWidth=1;dashed=1;dashPattern=4 4;" + FONT)

# ---- 边样式 ----
# 细实线·竖向（主连接，块箭头之外的次级连接）
EDGE = ("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;"
        "strokeColor=#000000;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;"
        "entryX=0.5;entryY=0;entryDx=0;entryDy=0;")
# 细实线·横向
EDGE_H = ("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;"
          "strokeColor=#000000;strokeWidth=1;")
# 细实线·直线（斜拉，无正交弯折）
EDGE_S = ("edgeStyle=none;rounded=0;html=1;endArrow=block;"
          "strokeColor=#000000;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;"
          "entryX=0.5;entryY=0;entryDx=0;entryDy=0;")
# 无箭头直线（括线/分组线用）
LINE = ("edgeStyle=none;rounded=0;html=1;endArrow=none;startArrow=none;"
        "strokeColor=#000000;strokeWidth=1;")
# 虚线·右缘引出（跨任务接口）
DASH = ("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;"
        "strokeColor=#000000;strokeWidth=1;dashed=1;dashPattern=4 4;"
        "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;fontSize=9;")
# 虚线·右缘引出（跨任务接口）——注意：按"虚线仅作边界"语义约定，慎用
DASH = ("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;"
        "strokeColor=#000000;strokeWidth=1;dashed=1;dashPattern=4 4;"
        "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;fontSize=9;")
# 虚线·横向相连 ——【已弃用】虚线不作连接线；并列关系改用 LINE
DASH_H = ("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=none;startArrow=none;"
          "strokeColor=#000000;strokeWidth=1;dashed=1;dashPattern=4 4;")
# 不可见锚点（括线/漏斗的节点）
DOT = "shape=point;whiteSpace=wrap;html=1;fillColor=none;strokeColor=none;" + FONT


def val(t):
    """文本转 XML 属性值：按行转 <br>，引号感知转义。"""
    return "&lt;br&gt;".join(html.escape(l, quote=True) for l in t.split("\n"))


class Sheet:
    def __init__(self):
        self.cells = []

    def node(self, id, text, x, y, w, h, style):
        self.cells.append(
            f'<mxCell id="{id}" value="{val(text)}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

    def nodev(self, id, raw_value, x, y, w, h, style):
        """value 已是转义后的 HTML（可含 <b> 等内联标签）。"""
        self.cells.append(
            f'<mxCell id="{id}" value="{raw_value}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

    def edge(self, id, s, t, st, label=""):
        self.cells.append(
            f'<mxCell id="{id}" value="{html.escape(label, quote=True)}" style="{st}" '
            f'edge="1" parent="1" source="{s}" target="{t}">'
            f'<mxGeometry relative="1" as="geometry"/></mxCell>')

    def barrow(self, id, cx, y, w=34, h=22):
        """块箭头节点，cx 为水平中心。"""
        self.node(id, "", cx - w // 2, y, w, h, BARROW)

    def point(self, id, x, y):
        """不可见锚点（括线拐角/漏斗收点）。"""
        self.node(id, "", x, y, 1, 1, DOT)

    def fan_out(self, pfx, cap_id, anchors, bar_y):
        """括线：cap_id 底部中点 → bar_y 横线 → 垂直到各目标框顶。
        anchors = [(target_id, 目标框顶中心x), ...]，按横坐标排序。"""
        xs = [x for _, x in anchors]
        mid = (min(xs) + max(xs)) // 2
        self.point(pfx + "M", mid, bar_y)
        self.edge(pfx + "v", cap_id, pfx + "M",
                  LINE + "exitX=0.5;exitY=1;entryX=0.5;entryY=0.5;")
        for i, (tid, x) in enumerate(anchors):
            self.point(pfx + str(i), x, bar_y)
            self.edge(pfx + "h" + str(i), pfx + "M", pfx + str(i), LINE)
            self.edge(pfx + "d" + str(i), pfx + str(i), tid,
                      LINE + "entryX=0.5;entryY=0;")

    def fan_in(self, pfx, sources, bar_y, cx):
        """倒括线（漏斗）：各源框底中心 → bar_y 横线 → 垂直到 cx（收点）。
        sources = [(source_id, 源框底中心x), ...]；返回收点 id（接块箭头/下个框）。"""
        for i, (sid, x) in enumerate(sources):
            self.point(pfx + str(i), x, bar_y)
            self.edge(pfx + "u" + str(i), sid, pfx + str(i),
                      LINE + "exitX=0.5;exitY=1;entryX=0.5;entryY=0.5;")
            self.edge(pfx + "h" + str(i), pfx + str(i), pfx + "M", LINE)
        self.point(pfx + "M", cx, bar_y)
        return pfx + "M"

    def doc(self, id_, name, page_w, page_h):
        return (f'<mxfile host="app.diagrams.net" type="device"><diagram id="{id_}" name="{name}">'
                f'<mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" '
                f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{page_w}" '
                f'pageHeight="{page_h}" math="0" shadow="0"><root><mxCell id="0"/>'
                f'<mxCell id="1" parent="0"/>{"".join(self.cells)}</root></mxGraphModel>'
                f'</diagram></mxfile>')


def write(sheet_doc, outdir, fname):
    import xml.etree.ElementTree as ET
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, fname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(sheet_doc)
    ET.parse(path)  # well-formedness check
    print('written', path)
    return path


def numlist(text):
    """把'；'分隔的并列项转成编号列表行。"""
    parts = [p.strip() for p in text.split('；') if p.strip()]
    if len(parts) <= 1:
        return text
    return "\n".join(f"{i+1}. {p}" for i, p in enumerate(parts))


def est_lines(text, w, fs=14, sp=9):
    """估算编号列表在 w 宽度、字号 fs、内边距 sp 下的行数（中文按字宽≈fs）。"""
    import math
    cpl = max(8, (w - 2 * sp) // fs)
    n = 0
    for seg in text.split("\n"):
        for it in [p.strip() for p in seg.split('；') if p.strip()]:
            n += max(1, math.ceil((len(it) + 2) / cpl))
    return max(1, n)


def row_h(text_a, text_b, w_a, w_b, fs=14, min_h=76, line_h=22, pad=16):
    """由内容/方法两列的文本估算行高（取较大者）。"""
    return max(min_h, max(est_lines(text_a, w_a, fs), est_lines(text_b, w_b, fs)) * line_h + pad)
