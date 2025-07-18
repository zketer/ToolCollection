#!/bin/bash

show_help() {
  echo "用法: $0 <IP地址或文件>"
  echo "  --help   显示帮助信息"
  echo "说明: 查询单个IP或批量查询（每行一个IP），使用ipinfo.io"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

input="$1"
if [[ -f "$input" ]]; then
  while read -r ip; do
    [[ -z "$ip" ]] && continue
    echo -n "$ip: "
    curl -s "https://ipinfo.io/$ip" | grep -E 'ip|city|region|country' | tr -d '"{},' | xargs
  done < "$input"
else
  curl -s "https://ipinfo.io/$input" | grep -E 'ip|city|region|country' | tr -d '"{},' | xargs
fi 