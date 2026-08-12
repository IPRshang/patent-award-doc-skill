#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Safe rewrite of a single table cell in a .docx via lxml.

Bypasses python-docx merged-cell segfault. Preserves any nested <w:tbl>
inside the cell (appends new paragraphs after it). Syncs multiple copies
and verifies MD5 consistency.

Usage:
  python edit_cell.py --docx FILE.docx --table 1 --row 3 --col 1 --text paras.txt \
      [--sync COPY1 COPY2 ...]

paras.txt: one paragraph per non-empty line.
"""
import argparse, zipfile, copy, hashlib, lxml.etree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
def q(n):
    return W + n

def make_para(tc, bp_p, bp_rpr, text):
    p = ET.SubElement(tc, q('p'))
    if bp_p is not None:
        p.append(copy.deepcopy(bp_p))
    r = ET.SubElement(p, q('r'))
    if bp_rpr is not None:
        r.append(copy.deepcopy(bp_rpr))
    t = ET.SubElement(r, q('t'))
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text
    return p

def edit_cell(raw_bytes, table_idx, row_idx, col_idx, paras):
    root = ET.fromstring(raw_bytes)
    body = root.find(q('body'))
    tops = [c for c in body if c.tag == q('tbl')]
    t = tops[table_idx]
    row = t.findall(q('tr'))[row_idx]
    tc = row.findall(q('tc'))[col_idx]
    old_ps = tc.findall(q('p'))
    bp_p = old_ps[0].find(q('pPr')) if old_ps else None
    bp_r = old_ps[0].find(q('r')) if old_ps else None
    bp_rpr = bp_r.find(q('rPr')) if bp_r is not None else None
    # remove only <w:p> children; keep any nested <w:tbl>
    for p in old_ps:
        tc.remove(p)
    for text in paras:
        make_para(tc, bp_p, bp_rpr, text)
    return ET.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

def repackage(src, dst, new_doc_xml_bytes):
    with zipfile.ZipFile(src, 'r') as z:
        data = {i.filename: z.read(i.filename) for i in z.infolist()}
    data['word/document.xml'] = new_doc_xml_bytes
    names = sorted(data.keys(), key=lambda n: (n != '[Content_Types].xml', n))
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in names:
            z.writestr(n, data[n])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--docx', required=True)
    ap.add_argument('--table', type=int, required=True)
    ap.add_argument('--row', type=int, required=True)
    ap.add_argument('--col', type=int, required=True)
    ap.add_argument('--text', required=True, help='paragraphs file (one paragraph per line)')
    ap.add_argument('--sync', nargs='*', default=[], help='extra copies to sync (same edit)')
    args = ap.parse_args()
    paras = [l.rstrip('\n') for l in open(args.text, encoding='utf-8') if l.strip() != '']
    targets = [args.docx] + args.sync
    md5s = []
    for p in targets:
        with zipfile.ZipFile(p, 'r') as z:
            raw = z.read('word/document.xml')
        new_xml = edit_cell(raw, args.table, args.row, args.col, paras)
        repackage(p, p, new_xml)
        md5s.append(hashlib.md5(open(p, 'rb').read()).hexdigest())
    ok = len(set(md5s)) == 1
    print(f'edited table{args.table} row{args.row} col{args.col} with {len(paras)} paragraphs')
    print('MD5 consistent:', ok, '|', (md5s[0] if ok else md5s))

if __name__ == '__main__':
    main()
