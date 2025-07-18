#!/bin/bash

show_help() {
  echo "用法: $0 <json文件>"
  echo "  --help   显示帮助信息"
  echo "  --check  仅校验JSON格式，不输出内容"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

file="$1"
shift
check_only=0

while [[ $# -gt 0 ]]; do
  case $1 in
    --check)
      check_only=1
      shift
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

if ! command -v jq >/dev/null 2>&1; then
  echo "需要安装 jq 工具 (brew install jq 或 apt install jq)"
  exit 2
fi

if [[ $check_only -eq 1 ]]; then
  if jq empty "$file" 2>/dev/null; then
    echo "JSON 格式正确"
  else
    echo "JSON 格式错误"
    exit 1
  fi
else
  jq . "$file"
fi 