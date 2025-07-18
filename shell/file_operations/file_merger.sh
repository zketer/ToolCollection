#!/bin/bash

show_help() {
  echo "用法: $0 <输出文件> <输入文件1> [输入文件2 ...]"
  echo "  --help   显示帮助信息"
  echo "说明: 按顺序合并多个文件为一个文件"
}

if [[ "$1" == "--help" || $# -lt 3 ]]; then
  show_help
  exit 0
fi

outfile="$1"
shift
cat "$@" > "$outfile"
echo "已合并为: $outfile" 