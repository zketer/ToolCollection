#!/bin/bash

show_help() {
  echo "用法: $0 <输出文件> <输入文件1> [输入文件2 ...] [--dedup]"
  echo "  --dedup   合并后去重"
  echo "  --help    显示帮助信息"
}

if [[ "$1" == "--help" || $# -lt 3 ]]; then
  show_help
  exit 0
fi

outfile="$1"
shift
dedup=0

for arg in "$@"; do
  if [[ "$arg" == "--dedup" ]]; then
    dedup=1
    set -- "${@/--dedup}"
    break
  fi
 done

cat "$@" > "$outfile"
if [[ $dedup -eq 1 ]]; then
  awk '!a[$0]++' "$outfile" > "$outfile.dedup" && mv "$outfile.dedup" "$outfile"
fi
echo "已合并为: $outfile" 