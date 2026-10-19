#!/usr/bin/env python3
# docx 图片嵌入/替换助手 —— 用 python-docx 标准路径，保证 wp:extent == a:ext
#
# 典型用法（在已有 drawing 的位置换图、或在段落里插图）：
#   from docx.shared import Inches
#   run = paragraph.add_run()
#   run.add_picture('fig.png', width=Inches(5.7))
#
# 替换已有图片（保位置换媒体+更新尺寸）：
#   python3 docx_embed.py replace 文档.docx --order 1,2,3 --files a.png,b.png,c.png --widths 6.1,5.7,5.7
#
# 安全宽度：正文区 ≤6.1in（版心≈6.3in）；表格单元格内 ≤5.7in
import sys, zipfile, re, shutil, os
from PIL import Image

EMU = 914400

def extent_for(png, width_in):
    w, h = Image.open(png).size
    return int(width_in * EMU), int(width_in * h / w * EMU)

def replace_in_order(docx_path, pngs, widths):
    """按文档中 drawing 出现顺序替换媒体+尺寸。"""
    bak = docx_path + '.bak'
    shutil.copy(docx_path, bak)
    zin = zipfile.ZipFile(bak)
    items = {n: zin.read(n) for n in zin.namelist()}
    zin.close()
    doc = items['word/document.xml'].decode('utf-8')
    rels = items['word/_rels/document.xml.rels'].decode('utf-8')

    embed_ids = re.findall(r'r:embed="(rId\d+)"', doc)
    rmap = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="media/([^"]+)"', rels))
    assert len(embed_ids) >= len(pngs), 'drawing 数量不足'

    new = doc
    wp = list(re.finditer(r'wp:extent cx="\d+" cy="\d+"', doc))
    for i, png in enumerate(pngs):
        cx, cy = extent_for(png, widths[i])
        m = wp[i]
        new = new[:m.start()] + f'wp:extent cx="{cx}" cy="{cy}"' + new[m.end():]
        ma = list(re.finditer(r'<a:ext cx="\d+" cy="\d+"', new))[i]
        new = new[:ma.start()] + f'<a:ext cx="{cx}" cy="{cy}"' + new[ma.end():]
        items['word/media/' + rmap[embed_ids[i]]] = open(png, 'rb').read()

    items['word/document.xml'] = new.encode('utf-8')
    with zipfile.ZipFile(docx_path, 'w', zipfile.ZIP_DEFLATED) as zo:
        for n, b in items.items():
            zo.writestr(n, b)
    verify(docx_path)
    print('replaced', len(pngs), 'images ->', docx_path, '(backup:', bak + ')')

def verify(docx_path):
    z = zipfile.ZipFile(docx_path)
    doc = z.read('word/document.xml').decode('utf-8')
    wp = re.findall(r'wp:extent cx="(\d+)" cy="(\d+)"', doc)
    ax = re.findall(r'<a:ext cx="(\d+)" cy="(\d+)"', doc)
    assert wp == ax, f'extent 不一致: {wp} vs {ax}'
    rels = z.read('word/_rels/document.xml.rels').decode('utf-8')
    for t in re.findall(r'Target="(media/[^"]+)"', rels):
        assert 'word/' + t in z.namelist(), f'缺媒体 {t}'
        Image.open(z.open('word/' + t)).verify()
    import docx as dx
    dx.Document(docx_path)
    print('verify OK:', len(wp), 'drawings, extents consistent, media valid')

if __name__ == '__main__':
    # 简易 CLI：python3 docx_embed.py replace a.docx --files x.png,y.png --widths 6.1,5.7
    args = sys.argv[1:]
    if len(args) >= 5 and args[0] == 'replace':
        docx_path = args[1]
        files = args[args.index('--files') + 1].split(',')
        widths = [float(x) for x in args[args.index('--widths') + 1].split(',')]
        assert len(files) == len(widths)
        replace_in_order(docx_path, files, widths)
    elif args and args[0] == 'verify':
        verify(args[1])
    else:
        print(__doc__)
