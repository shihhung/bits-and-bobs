#!/usr/bin/env python3
"""markdown → ADF（Atlassian Document Format）轉換器。

為什麼需要：acli 的 --body / --body-file / --description-file 雖然文件說
「plain text or ADF」，但餵 markdown 不會渲染。實測 2026-09-18（acli 1.3.36）：
送 markdown 純文字進 Jira，整段會塞進單一 paragraph 的單一 text node，
`##`、`**`、反引號全部變成字面文字。要有格式就必須送 ADF JSON。

用法：
    python3 md2adf.py < comment.md > comment.adf.json
    python3 md2adf.py -i comment.md -o comment.adf.json
    acli jira workitem comment create --key PER-1 --body-file comment.adf.json

支援：heading（#～######）、段落、粗體、斜體、刪除線、inline code、
連結、無序清單、有序清單（含一層巢狀）、code block（含語言標記）、
blockquote、水平線、表格（GFM 寫法：表頭列＋分隔列；第一列轉表頭，
欄數以表頭為準，對齊標記忽略；儲存格內反斜線跳脫的 | 或 inline code 裡的 | 不分欄）。

不支援：圖片、mention、panel。需要這些請直接手寫 ADF。
"""

import argparse
import json
import re
import sys

# inline 語法。順序重要：code 最先（其中的 ** 不再解析），strong 先於 em。
INLINE_RE = re.compile(
    r"(?P<code>`[^`\n]+`)"
    r"|(?P<link>\[[^\]\n]+\]\([^)\s]+\))"
    r"|(?P<strong>\*\*[^\n]+?\*\*)"
    r"|(?P<strike>~~[^\n]+?~~)"
    r"|(?P<em>(?<![\w*])\*[^*\n]+?\*(?![\w*]))"
)

FENCE_RE = re.compile(r"^\s*```(\w+)?\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_RE = re.compile(r"^(\s*)[-*+]\s+(.*)$")
ORDERED_RE = re.compile(r"^(\s*)\d+[.)]\s+(.*)$")
QUOTE_RE = re.compile(r"^>\s?(.*)$")
RULE_RE = re.compile(r"^\s*(-{3,}|_{3,}|\*{3,})\s*$")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")


def text_node(value, marks=None):
    node = {"type": "text", "text": value}
    if marks:
        node["marks"] = marks
    return node


def parse_inline(line):
    """把一行 markdown 轉成 ADF inline node 陣列。"""
    nodes = []
    pos = 0
    for m in INLINE_RE.finditer(line):
        if m.start() > pos:
            nodes.append(text_node(line[pos:m.start()]))
        kind = m.lastgroup
        raw = m.group(kind)
        if kind == "code":
            nodes.append(text_node(raw[1:-1], [{"type": "code"}]))
        elif kind == "strong":
            nodes.extend(_wrap(raw[2:-2], {"type": "strong"}))
        elif kind == "strike":
            nodes.extend(_wrap(raw[2:-2], {"type": "strike"}))
        elif kind == "em":
            nodes.extend(_wrap(raw[1:-1], {"type": "em"}))
        elif kind == "link":
            label, href = re.match(r"\[([^\]]+)\]\(([^)\s]+)\)", raw).groups()
            nodes.append(text_node(label, [{"type": "link", "attrs": {"href": href}}]))
        pos = m.end()
    if pos < len(line):
        nodes.append(text_node(line[pos:]))
    return nodes


def _wrap(inner, mark):
    """對已知要加 mark 的內容再跑一次 inline 解析，讓 **[連結](url)** 這種疊加生效。

    ADF 的 code mark 只能和 link 並存：**`code`** 若同時帶 strong，Jira 回
    INVALID_INPUT（2026-10-27 GOGOLIFE-189 實測）。所以 code 節點不再疊加其他 mark。
    """
    out = []
    for node in parse_inline(inner) or [text_node(inner)]:
        marks = node.get("marks", [])
        if any(mk["type"] == "code" for mk in marks):
            out.append(node)
            continue
        if not any(mk["type"] == mark["type"] for mk in marks):
            marks = marks + [mark]
        node["marks"] = marks
        out.append(node)
    return out


def paragraph(lines):
    """多行合併成一個 paragraph，行間用 hardBreak。"""
    content = []
    for i, line in enumerate(lines):
        if i:
            content.append({"type": "hardBreak"})
        content.extend(parse_inline(line))
    return {"type": "paragraph", "content": content} if content else {"type": "paragraph"}


def split_cells(line):
    """切一列表格的儲存格：`\\|` 與 inline code 裡的 | 不當分隔。"""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    cells, cur, in_code, i = [], [], False, 0
    while i < len(body):
        ch = body[i]
        if ch == "\\" and i + 1 < len(body) and body[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
        i += 1
    cells.append("".join(cur).strip())
    return cells


def is_table_start(lines, i):
    return (TABLE_ROW_RE.match(lines[i]) is not None
            and i + 1 < len(lines) and TABLE_SEP_RE.match(lines[i + 1]) is not None)


def parse_table(lines, i):
    """表頭列＋分隔列＋資料列 → ADF table。欄數以表頭為準，多補空格、少截掉。"""
    header = split_cells(lines[i])
    width = len(header)
    rows = [header]
    i += 2  # 跳過表頭與分隔列
    while i < len(lines) and TABLE_ROW_RE.match(lines[i]):
        row = split_cells(lines[i])
        rows.append((row + [""] * width)[:width])
        i += 1
    table_rows = []
    for r, row in enumerate(rows):
        kind = "tableHeader" if r == 0 else "tableCell"
        table_rows.append({"type": "tableRow", "content": [
            {"type": kind, "content": [paragraph([cell])]} for cell in row]})
    return {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": False, "layout": "default"},
        "content": table_rows,
    }, i


def list_item(text):
    return {"type": "listItem", "content": [paragraph([text])]}


def convert(markdown):
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    content = []
    buffer = []          # 累積中的段落行
    i = 0

    def flush():
        if buffer:
            content.append(paragraph(buffer))
            buffer.clear()

    while i < len(lines):
        line = lines[i]

        fence = FENCE_RE.match(line)
        if fence:
            flush()
            lang = fence.group(1)
            i += 1
            code_lines = []
            while i < len(lines) and not FENCE_RE.match(lines[i]):
                code_lines.append(lines[i])
                i += 1
            i += 1  # 吃掉收尾的 fence
            node = {"type": "codeBlock", "content": [text_node("\n".join(code_lines))]}
            if lang:
                node["attrs"] = {"language": lang}
            content.append(node)
            continue

        if not line.strip():
            flush()
            i += 1
            continue

        if RULE_RE.match(line):
            flush()
            content.append({"type": "rule"})
            i += 1
            continue

        heading = HEADING_RE.match(line)
        if heading:
            flush()
            level = len(heading.group(1))
            content.append({
                "type": "heading",
                "attrs": {"level": level},
                "content": parse_inline(heading.group(2)),
            })
            i += 1
            continue

        if QUOTE_RE.match(line):
            flush()
            quoted = []
            while i < len(lines) and QUOTE_RE.match(lines[i]):
                quoted.append(QUOTE_RE.match(lines[i]).group(1))
                i += 1
            content.append({"type": "blockquote", "content": [paragraph(quoted)]})
            continue

        if is_table_start(lines, i):
            flush()
            node, i = parse_table(lines, i)
            content.append(node)
            continue

        if BULLET_RE.match(line) or ORDERED_RE.match(line):
            flush()
            node, i = parse_list(lines, i)
            content.append(node)
            continue

        buffer.append(line)
        i += 1

    flush()
    if not content:
        content = [{"type": "paragraph"}]
    return {"type": "doc", "version": 1, "content": content}


def parse_list(lines, i):
    """解析一段清單，支援一層巢狀（以縮排判斷）。"""
    first = BULLET_RE.match(lines[i]) or ORDERED_RE.match(lines[i])
    ordered = ORDERED_RE.match(lines[i]) is not None
    base_indent = len(first.group(1).expandtabs(4))
    items = []

    while i < len(lines):
        m = ORDERED_RE.match(lines[i]) or BULLET_RE.match(lines[i])
        if not m:
            break
        indent = len(m.group(1).expandtabs(4))
        if indent < base_indent:
            break
        if indent > base_indent:
            child, i = parse_list(lines, i)
            if items:
                items[-1]["content"].append(child)
            else:
                items.append({"type": "listItem", "content": [child]})
            continue
        is_ordered = ORDERED_RE.match(lines[i]) is not None
        if is_ordered != ordered:
            break
        items.append(list_item(m.group(2)))
        i += 1

    return {
        "type": "orderedList" if ordered else "bulletList",
        "content": items or [list_item("")],
    }, i


def main():
    ap = argparse.ArgumentParser(description="markdown → ADF（給 acli 用）")
    ap.add_argument("-i", "--input", help="輸入 markdown 檔（預設讀 stdin）")
    ap.add_argument("-o", "--output", help="輸出 ADF JSON 檔（預設寫 stdout）")
    ap.add_argument("--compact", action="store_true", help="輸出壓縮成一行")
    args = ap.parse_args()

    src = open(args.input, encoding="utf-8").read() if args.input else sys.stdin.read()
    doc = convert(src)
    dumped = json.dumps(doc, ensure_ascii=False, indent=None if args.compact else 2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(dumped + "\n")
    else:
        sys.stdout.write(dumped + "\n")


if __name__ == "__main__":
    main()
