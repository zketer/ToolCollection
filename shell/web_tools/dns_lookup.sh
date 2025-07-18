#!/bin/bash

show_help() {
  echo "用法: $0 <域名文件>"
  echo "  --type TYPE   查询类型(A, AAAA, MX, TXT等)，默认A"
  echo "  --help        显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

file="$1"
shift
type="A"

while [[ $# -gt 0 ]]; do
  case $1 in
    --type)
      type="$2"
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

while read -r domain; do
  if [[ -z "$domain" ]]; then continue; fi
  result=$(dig +short "$domain" $type)
  echo "$domain [$type]: $result"
done < "$file" 