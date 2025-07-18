#!/bin/bash

show_help() {
  echo "用法: $0 <csv文件> [--head N] [--col 列号]"
  echo "  --head N   只显示前N行"
  echo "  --col NUM  只显示第NUM列 (从1开始)"
  echo "  --help     显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

file="$1"
shift
head_n=""
col_num=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --head)
      head_n="$2"
      shift 2
      ;;
    --col)
      col_num="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
 done

if [[ ! -f "$file" ]]; then
  echo "文件不存在: $file"
  exit 1
fi

cmd="cat '$file'"
if [[ -n "$head_n" ]]; then
  cmd="$cmd | head -n $head_n"
fi
if [[ -n "$col_num" ]]; then
  cmd="$cmd | awk -F, '{print \$$col_num}'"
fi
eval $cmd 