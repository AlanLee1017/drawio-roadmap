---
name: drawio-roadmap
description: 设计并生成黑白学术风格的技术路线/逻辑框架/研究框架图（Draw.io XML 源文件 + PNG/SVG 导出），可直接嵌入 Word/申报书
argument-hint: "[图类型：logic|framework|task] [输出目录]"
allowed-tools:
  - read
  - write
  - edit
  - exec
  - glob
  - grep
---

# Draw.io 学术路线图生成器

为用户生成**可编辑、风格统一、可直接嵌入申报书**的技术路线图。核心原则：先设计再生成，Draw.io XML 是唯一真源，PNG 嵌入用、SVG 归档用。

## 快速开始

```bash
# 1. 把本 skill 的 assets（与 SKILL.md 同级）复制到工作目录
#    全局安装位置：~/.config/devin/skills/drawio-roadmap/assets/*.py
#    插件安装位置：插件目录 skills/drawio-roadmap/assets/*.py
cp <skill目录>/assets/*.py 工作目录/

# 2. 选模板改数据（三个模板各自含示例数据，改 TASKS / rows / qs 即可）
python3 template_task.py        # → task1.drawio  行式任务路线
python3 template_logic.py       # → logic.drawio  问题层级树
python3 template_framework.py   # → framework.drawio  三栏研究框架

# 3. 渲染（macOS Draw.io Desktop）
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -s 2 -o out.png in.drawio
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f svg  -o out.svg in.drawio
# task_policy_set 警告可忽略；无 GUI 环境可 -x -f pdf 或 brew install drawio

# 4. 目检 PNG 给用户确认后，再嵌入 docx
python3 docx_embed.py replace 文档.docx --files a.png,b.png --widths 6.1,5.7
python3 docx_embed.py verify 文档.docx
```

## 工作流（严格执行）

1. **先设计**：与用户确认图式（问题树/三栏框架/环节行布局）、内容层级、文字措辞——不要上来就画
2. **生成器写 XML**：以 assets 模板为底改数据；改坐标/措辞后重跑脚本重渲染
3. **先出 PNG 给用户过目，确认后才嵌入目标文档**
4. **嵌入 Word**：正文区图宽 ≤6.1in（版心≈6.3in）；**表格单元格内 ≤5.7in**（单元格内边距会裁 6.1in 的图）

## 全局线型语义（硬性约定）

| 线型 | 唯一含义 |
|---|---|
| 实线箭头（细，endArrow=block） | 有方向的推导/数据流向 |
| 块箭头（shape=singleArrow 空心粗箭头） | 阶段间主链推进 |
| 实线无箭头（endArrow=none） | 并列/组成：括线、同层横连、漏斗收口 |
| 虚线 | **只作边界/围合**：分组框、条目容器；绝不用作连接线（DASH_H 已弃用） |
| 实线直角框 | 节点/标签/输出元素 |

## 版式与对齐规则

- **纯黑白**：fillColor=#ffffff、strokeColor=#000000；无灰阶无配色（除非用户另要）
- **无竖排文字**：所有标签横排；竖脊/竖排层名要歪头看，禁用
- **无图内大标题**：图注承担标题职责
- **层/组名标签**：白底 text 节点骑在虚线组框上边线正中（fieldset 图例式），fontSize 15-16 粗体；相邻两个组框之间留足间隔（≥30px），否则标签归属不清
- **字号基准**：画布内容 14-15、标签/列头 15-16、核心框 16；嵌入后有效字号 ≈ 画布字号 × 嵌入宽度/画布宽度，目标 ≥7.5pt
- **对齐**：同层框等高顶对齐等间距；多线汇入同一框用对称错开 entryX（0.38/0.62）；块箭头列内水平居中；能垂直/水平的线不许斜
- **括线收放**：多用 `s.fan_out()`（标签→横线→垂直落多框）和 `s.fan_in()`（多框底→横线→收点）；比斜线尖角收敛美观，且上下呼应
- **行高自适应**：`row_h(content, method, CW, MW)` 按条目数估算；别用统一行高造成大片空白
- **容器内列表**：并列条目用 "1. 2. 3." 编号（`numlist()` 自动把 `；` 分隔转编号）
- **分隔符**：并列短项用"·"、连接/范围用"—"、分句用"；"

## 三种图式要点

- **logic（构思逻辑图）**：括注+括线→前提框→斜线汇入核心问题→块箭头→并列子问题(实线横连)→汇入综合问题→fan_in漏斗→块箭头→成果带；无外框、无层名标签
- **framework（研究框架图）**：列头顶部一次；思路列块箭头竖链留在层框外（避免箭头穿虚线框）；虚线组框只包内容+方法列；方法框用实线（虚线里套虚线太吵）
- **task（任务路线图）**：行间块箭头只画到倒数第二行；最后一行由底部"任务输出"带上的居中块箭头承接——别在末行下再叠一个

## 嵌入 docx 验证清单（docx_embed.py verify 自动检查）

- `wp:extent` 与内层 `a:ext` 一致（不一致=Word 报图片异常/裁切）
- 每个 drawing 的 r:embed → rels Target 存在且指向正确 media
- 包内 PNG 逐个 PIL 解码；python-docx 能正常打开
- 插图用 `run.add_picture()` 标准路径；**不要手写 XML 克隆 drawing 段落**

## assets

| 文件 | 用途 |
|---|---|
| `drawio_common.py` | 样式常量（BOX/HDR/GROUP/LBL/COLLB/BARROW/FRAME/DOT、EDGE/EDGE_H/EDGE_S/LINE）、Sheet（node/nodev/edge/barrow/point/fan_out/fan_in）、val/numlist/est_lines/row_h |
| `template_task.py` | 行式任务路线模板（自适应行高、编号列表、底部输出带） |
| `template_logic.py` | 问题层级树模板（括线/漏斗/错开汇入） |
| `template_framework.py` | 三栏框架模板（分层虚线组框、骑线标签、层间加宽） |
| `docx_embed.py` | docx 嵌图/换图 + 完整性验证 CLI |
