#!/bin/bash
# 批量文件重命名工具
# 用法: ./batch_rename.sh <目录> [--prefix xxx] [--suffix xxx] [--regex 's/old/new/'] [--number] [--help]

show_help() {
  echo "用法: $0 <目录> [--prefix xxx] [--suffix xxx] [--regex 's/old/new/'] [--number] [--help]"
  echo "批量重命名目录下的文件，支持前缀、后缀、正则替换、序号。"
  exit 0
}

if [[ "$1" == "--help" || "$#" -eq 0 ]]; then
  show_help
fi

dir="$1"; shift
prefix=""; suffix=""; regex=""; number=0
while [[ $# -gt 0 ]]; do
  case $1 in
    --prefix) prefix="$2"; shift 2;;
    --suffix) suffix="$2"; shift 2;;
    --regex) regex="$2"; shift 2;;
    --number) number=1; shift;;
    *) shift;;
  esac
done

cd "$dir" || exit 1
count=1
for f in *; do
  [[ -f "$f" ]] || continue
  new="$f"
  if [[ -n "$regex" ]]; then
    new=$(echo "$new" | sed "$regex")
  fi
  if [[ $number -eq 1 ]]; then
    ext="${f##*.}"; base="${f%.*}"
    new="${prefix}${base}_$count${suffix}.${ext}"
  else
    new="${prefix}${new}${suffix}"
  fi
  if [[ "$f" != "$new" ]]; then
    mv -v "$f" "$new"
  fi
  ((count++))
done 