#!/usr/bin/env python3
# Mermaid風コードブロックの静的検証（依存なし簡易版）
# 目的: docs配下のMarkdown/MDXに含まれる```mermaid```ブロックの妥当性を最低限チェック
# 制約: mermaid-cli不使用。厳密構文ではなくヒューリスティック検証を行う。

import sys
import re
from pathlib import Path

SUPPORTED = {
    "flowchart",
    "graph",
    "sequenceDiagram",
    "classDiagram",
    "stateDiagram",
    "stateDiagram-v2",
    "erDiagram",
    "journey",
    "gantt",
    "pie",
    "timeline",
    "mindmap",
    "quadrantChart",
    "sankey-beta",
    "requirementDiagram",
    "gitGraph",
    "c4context",
    "c4container",
    "c4component",
    "c4deployment",
}

FENCE_OPEN_RE = re.compile(r"^`{3,}\s*mermaid(\s|$)")
FENCE_CLOSE_RE = re.compile(r"^`{3,}\s*$")


def first_meaningful(lines):
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        # comment line
        if s.startswith("%%"):
            continue
        # init directive like %%{init: ...}%%
        if s.startswith("%%{") and s.endswith("}%%"):
            continue
        return s
    return ""


def validate_block(content_lines):
    errors = []
    head = first_meaningful(content_lines)
    if not head:
        errors.append("空の図ブロック")
        return errors

    # diagram type detection
    head_token = head.split()[0]
    if head_token not in SUPPORTED:
        errors.append(f"未知のダイアグラム種別: {head_token}")
        return errors

    body = "\n".join(content_lines)

    def has(pattern):
        return re.search(pattern, body, re.MULTILINE) is not None

    if head_token in ("graph", "flowchart"):
        # 要件: 少なくとも1つのエッジを含む
        if not has(r"(-\.-\>|--\>|===|==\>|---)"):
            errors.append("flowchart/graphにエッジが不足")
    elif head_token == "sequenceDiagram":
        if not has(r"^[ \t]*(participant|actor)\s+\S+"):
            errors.append("sequenceDiagramにparticipantが不足")
        if not has(r"-{1,2}>{1,2}"):
            errors.append("sequenceDiagramにメッセージが不足")
    elif head_token == "classDiagram":
        if not has(r"^[ \t]*class\s+\w+") and not has(r"\w+\s+<\|--\s+\w+"):
            errors.append("classDiagramにclass/関連定義が不足")
    elif head_token.startswith("stateDiagram"):
        if not has(r"--\>") and not has(r"^[ \t]*state\s+\w+"):
            errors.append("stateDiagramに状態/遷移が不足")
    elif head_token == "erDiagram":
        # 単純チェック: エンティティ定義 or 関連線
        if not (has(r"^[ \t]*\w+[ \t]*\{") or has(r"[|}{o]+--[|}{o]+")):
            errors.append("erDiagramにエンティティ/関連が不足")
    elif head_token in ("journey",):
        if not has(r"^[ \t]*section\s") and not has(r":\s*\d+"):
            errors.append("journeyにsection/ステップが不足")
    elif head_token == "gantt":
        if not has(r"^[ \t]*dateFormat\s") and not has(r"^[ \t]*section\s"):
            errors.append("ganttにdateFormat/sectionが不足")
    elif head_token in ("pie", "timeline"):
        if not has(r":\s*\d+") and not has(r":\s*\d+\.\d+"):
            errors.append(f"{head_token}にラベル:値の行が不足")
    elif head_token in ("mindmap", "quadrantChart", "sankey-beta", "requirementDiagram", "gitGraph", "c4context", "c4container", "c4component", "c4deployment"):
        # 軽量チェックのみ（先頭行種別検出を以て最低限OK）
        pass

    return errors


def extract_blocks(text):
    lines = text.splitlines()
    i = 0
    blocks = []
    while i < len(lines):
        if FENCE_OPEN_RE.match(lines[i]):
            i += 1
            buf = []
            while i < len(lines) and not FENCE_CLOSE_RE.match(lines[i]):
                buf.append(lines[i])
                i += 1
            # skip closing fence if present
            if i < len(lines) and FENCE_CLOSE_RE.match(lines[i]):
                i += 1
            blocks.append(buf)
        else:
            i += 1
    return blocks


def scan_dir(root):
    root_p = Path(root)
    targets = list(root_p.rglob("*.md")) + list(root_p.rglob("*.markdown")) + list(root_p.rglob("*.mdx"))
    results = {}
    for path in sorted(targets):
        text = path.read_text(encoding="utf-8", errors="ignore")
        blocks = extract_blocks(text)
        file_errors = []
        for idx, block in enumerate(blocks, start=1):
            errs = validate_block(block)
            if errs:
                for e in errs:
                    file_errors.append(f"{path}:{idx}: {e}")
        if file_errors:
            results[str(path)] = file_errors
    return results


def main():
    if len(sys.argv) != 2:
        print("使い方: validate_mermaid.py <docsディレクトリ>", file=sys.stderr)
        return 2
    root = sys.argv[1]
    errors = scan_dir(root)
    if not errors:
        print(f"Mermaid syntax OK: {root}")
        return 0
    count = 0
    for f, msgs in errors.items():
        for m in msgs:
            print(m)
            count += 1
    print(f"失敗件数: {len(errors)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
