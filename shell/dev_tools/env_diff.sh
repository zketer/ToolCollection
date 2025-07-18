#!/bin/bash

show_help() {
  echo "用法: $0 <env1文件> <env2文件>"
  echo "  --help   显示帮助信息"
  echo "说明: 比较两个 .env 文件的差异（按 KEY）"
}

if [[ "$1" == "--help" || $# -lt 2 ]]; then
  show_help
  exit 0
fi

file1="$1"
file2="$2"

if [[ ! -f "$file1" || ! -f "$file2" ]]; then
  echo "文件不存在: $file1 或 $file2"
  exit 1
fi

keys1=$(grep -v '^#' "$file1" | grep '=' | cut -d= -f1 | sort)
keys2=$(grep -v '^#' "$file2" | grep '=' | cut -d= -f1 | sort)

echo "仅 $file1 有的 KEY:"
comm -23 <(echo "$keys1") <(echo "$keys2")

echo "仅 $file2 有的 KEY:"
comm -13 <(echo "$keys1") <(echo "$keys2") 