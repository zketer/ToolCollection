#!/bin/bash

show_help() {
  echo "用法: $0 <代理列表文件> [--test-url URL]"
  echo "  --test-url U   指定测试URL，默认https://www.google.com"
  echo "  --help         显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

file="$1"
shift
test_url="https://www.google.com"

while [[ $# -gt 0 ]]; do
  case $1 in
    --test-url)
      test_url="$2"
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

while read -r proxy; do
  [[ -z "$proxy" ]] && continue
  code=$(curl -x "$proxy" -s -o /dev/null -w "%{http_code}" --max-time 8 "$test_url")
  echo "$proxy -> $code"
done < "$file" 