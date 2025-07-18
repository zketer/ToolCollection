#!/bin/bash

show_help() {
  echo "用法: $0 <文件> [--upper] [--lower] [--replace A B] [--dedup] [--output 输出文件]"
  echo "  --upper        全部转大写"
  echo "  --lower        全部转小写"
  echo "  --replace A B  批量替换A为B"
  echo "  --dedup        去重"
  echo "  --output F     输出到指定文件，默认覆盖原文件"
  echo "  --help         显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

infile="$1"
shift
outfile="$infile"
upper=0
lower=0
replace_a=""
replace_b=""
dedup=0

while [[ $# -gt 0 ]]; do
  case $1 in
    --upper)
      upper=1
      shift
      ;;
    --lower)
      lower=1
      shift
      ;;
    --replace)
      replace_a="$2"
      replace_b="$3"
      shift 3
      ;;
    --dedup)
      dedup=1
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

if [[ $upper -eq 1 ]]; then
  awk '{print toupper($0)}' "$tmpfile" > "$tmpfile.upper" && mv "$tmpfile.upper" "$tmpfile"
fi
if [[ $lower -eq 1 ]]; then
  awk '{print tolower($0)}' "$tmpfile" > "$tmpfile.lower" && mv "$tmpfile.lower" "$tmpfile"
fi
if [[ -n "$replace_a" && -n "$replace_b" ]]; then
  sed -i '' "s/$replace_a/$replace_b/g" "$tmpfile"
fi
if [[ $dedup -eq 1 ]]; then
  awk '!a[$0]++' "$tmpfile" > "$tmpfile.dedup" && mv "$tmpfile.dedup" "$tmpfile"
fi
mv "$tmpfile" "$outfile"
echo "已处理: $outfile" 