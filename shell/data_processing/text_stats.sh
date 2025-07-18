#!/bin/bash

show_help() {
  echo "用法: $0 <文本文件>"
  echo "  --help   显示帮助信息"
  echo "说明: 输出行数、词数、字符数"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

file="$1"
if [[ ! -f "$file" ]]; then
  echo "文件不存在: $file"
  exit 1
fi

lines=$(wc -l < "$file")
words=$(wc -w < "$file")
chars=$(wc -m < "$file")
echo "行数: $lines"
echo "词数: $words"
echo "字符数: $chars" 