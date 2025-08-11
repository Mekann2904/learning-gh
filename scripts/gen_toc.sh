#!/usr/bin/env bash
set -euo pipefail

# 簡易Markdown目次生成（GitHub想定）
# 使い方:
#   bash scripts/gen_toc.sh README.md > TOC.md
#   # または上書き例（先頭に挿入したい場合は手動で貼り付け）

file=${1:-}
if [[ -z "$file" || ! -f "$file" ]]; then
  echo "Usage: $0 <markdown-file>" >&2
  exit 1
fi

echo "- 目次"
grep -nE '^#{1,4} ' "$file" | awk '
  {
    line=$0
    split(line, a, ":");
    sub(/^.*: /, "", line);
    # 見出しレベルとタイトル抽出
    match(line, /^(#+) (.*)$/, m);
    level=length(m[1]);
    title=m[2];
    # アンカー生成（簡易）: 小文字化＋空白->-、バッククォート除去
    anchor=title;
    gsub(/`/, "", anchor);
    # tolower は awk 実装依存だが多くで利用可
    lower=tolower(anchor);
    gsub(/ /, "-", lower);
    printf("%s- [%s](#%s)\n", (level>1? sprintf("%" (level-1) "s", ""):""), title, lower);
  }'

