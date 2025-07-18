#!/bin/bash

show_help() {
  echo "用法: $0 <url文件>"
  echo "  --timeout N   设置超时时间(秒)，默认5"
  echo "  --help       显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

file="$1"
shift
timeout=5

while [[ $# -gt 0 ]]; do
  case $1 in
    --timeout)
      timeout="$2"
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

while read -r url; do
  if [[ -z "$url" ]]; then continue; fi
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time $timeout "$url")
  echo "$url -> $code"
done < "$file" 