#!/bin/bash

show_help() {
  echo "用法: $0 <输入文件> [--dedup] [--trim] [--nonempty] [--output 输出文件]"
  echo "  --dedup      去重（只保留唯一行）"
  echo "  --trim       去除每行首尾空白"
  echo "  --nonempty   去除空行"
  echo "  --output F   输出到指定文件，默认覆盖原文件"
  echo "  --help       显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

infile="$1"
shift
outfile="$infile"
dedup=0
trim=0
nonempty=0

while [[ $# -gt 0 ]]; do
  case $1 in
    --dedup)
      dedup=1
      shift
      ;;
    --trim)
      trim=1
      shift
      ;;
    --nonempty)
      nonempty=1
      shift
      ;;
    --output)
      outfile="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
 done

tmpfile=$(mktemp)
cp "$infile" "$tmpfile"

if [[ $trim -eq 1 ]]; then
  sed -i '' 's/^ *//;s/ *$//' "$tmpfile"
fi
if [[ $nonempty -eq 1 ]]; then
  sed -i '' '/^$/d' "$tmpfile"
fi
if [[ $dedup -eq 1 ]]; then
  awk '!a[$0]++' "$tmpfile" > "$tmpfile.dedup" && mv "$tmpfile.dedup" "$tmpfile"
fi
mv "$tmpfile" "$outfile"
echo "已处理: $outfile" 