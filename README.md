# drawio-roadmap

Devin 插件：生成黑白学术风格的技术路线/逻辑框架/研究框架图——Draw.io XML 可编辑源 + PNG/SVG 导出 + docx 嵌入验证。适合申报书、论文、课题材料中的技术路线图。

## 安装

```bash
devin plugins install AlanLee1017/drawio-roadmap
```

安装后 skill 以 `/drawio-roadmap:drawio-roadmap` 调用（或直接说"画技术路线图"）。

也可以免安装：把 `skills/drawio-roadmap/` 拷到 `~/.config/devin/skills/` 即可。

## 包含

- **三套图式模板**（改数据即用）：
  - `template_logic.py` — 问题层级树（括线/漏斗收口/错开汇入）
  - `template_framework.py` — 三栏研究框架（分层虚线组框、骑线标签）
  - `template_task.py` — 行式任务路线（自适应行高、编号列表）
- **`drawio_common.py`** — 黑白样式库与 XML 构造助手（Sheet/fan_out/fan_in/row_h…）
- **`docx_embed.py`** — docx 嵌图换图 + 完整性验证 CLI

## 设计约定

- 纯黑白，无竖排文字，无图内大标题（图注承担）
- 线型语义统一：实线箭头=流向、块箭头=阶段推进、实线无箭头=并列、**虚线仅作边界**
- 工作流：先设计→改数据→渲染 PNG 过目→确认后才嵌文档

详见 `skills/drawio-roadmap/SKILL.md`。
