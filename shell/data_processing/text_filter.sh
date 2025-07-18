#!/bin/bash

show_help() {
  echo "用法: $0 <文件> [--include 关键字] [--exclude 关键字] [--regex 正则]"
  echo "  --include KW   只保留包含关键字的行"
  echo "  --exclude KW   排除包含关键字的行"
  echo "  --regex RE     只保留匹配正则的行"
  echo "  --help         显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

file="$1"
shift
inc=""
exc=""
regex=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --include)
      inc="$2"
      shift 2
      ;;
    --exclude)
      exc="$2"
      shift 2
      ;;
    --regex)
      regex="$2"
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
if [[ -n "$inc" ]]; then
  cmd="$cmd | grep '$inc'"
fi
if [[ -n "$exc" ]]; then
  cmd="$cmd | grep -v '$exc'"
fi
if [[ -n "$regex" ]]; then
  cmd="$cmd | grep -E '$regex'"
fi
eval $cmd 