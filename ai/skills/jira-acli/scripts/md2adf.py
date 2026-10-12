#!/usr/bin/env python3
"""Markdown to ADF (Atlassian Document Format) converter.

Why this exists: the help text of acli's --body / --body-file / --description-file
says "plain text or ADF", but plain markdown is not rendered. Tested on
2026-09-18 (acli 1.3.36): markdown sent as plain text ends up in a single
paragraph with a single text node, and `##`, `**`, and backticks all show up
as literal characters. To get formatting you must send ADF JSON.

Usage:
    python3 md2adf.py < comment.md > comment.adf.json
    python3 md2adf.py -i comment.md -o comment.adf.json
    acli jira workitem comment create --key PROJ-1 --body-file comment.adf.json

Supported: headings (# to ######), paragraphs, bold, italic, strikethrough,
inline code, links, bullet lists, ordered lists (one nested level), code
blocks (with language tag), blockquotes, horizontal rules.

Not supported: tables, images, mentions, panels. Write ADF by hand for those.
"""

import argparse
import json
import re
import sys

# Inline syntax. Order matters: code first (no ** parsing inside it), strong before em.
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


def text_node(value, marks=None):
    node = {"type": "text", "text": value}
    if marks:
        node["marks"] = marks
    return node


def parse_inline(line):
    """Convert one line of markdown into an array of ADF inline nodes."""
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
    """Run inline parsing again on content that gets a mark, so stacked forms like **`code`** work."""
    out = []
    for node in parse_inline(inner) or [text_node(inner)]:
        marks = node.get("marks", [])
        if not any(mk["type"] == mark["type"] for mk in marks):
            marks = marks + [mark]
        node["marks"] = marks
        out.append(node)
    return out


def paragraph(lines):
    """Merge several lines into one paragraph, joined by hardBreak."""
    content = []
    for i, line in enumerate(lines):
        if i:
            content.append({"type": "hardBreak"})
        content.extend(parse_inline(line))
    return {"type": "paragraph", "content": content} if content else {"type": "paragraph"}


def list_item(text):
    return {"type": "listItem", "content": [paragraph([text])]}


def convert(markdown):
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    content = []
    buffer = []          # paragraph lines collected so far
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
            i += 1  # consume the closing fence
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
    """Parse a list. Supports one nested level, detected by indentation."""
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
    ap = argparse.ArgumentParser(description="Markdown to ADF (for acli)")
    ap.add_argument("-i", "--input", help="input markdown file (default: stdin)")
    ap.add_argument("-o", "--output", help="output ADF JSON file (default: stdout)")
    ap.add_argument("--compact", action="store_true", help="write compact single-line JSON")
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
