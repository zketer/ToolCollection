#!/bin/bash

show_help() {
  echo "用法: $0 <文件> <列号> [--delim 分隔符]"
  echo "  --delim D   指定分隔符，默认逗号(,)
  echo "  --help      显示帮助信息"
}

if [[ "$1" == "--help" || $# -lt 2 ]]; then
  show_help
  exit 0
fi

file="$1"
col="$2"
shift 2
delim=','

while [[ $# -gt 0 ]]; do
  case $1 in
    --delim)
      delim="$2"
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

awk -F"$delim" -v c="$col" '{print $c}' "$file" 