#!/bin/bash

show_help() {
  echo "用法: $0 <目录>"
  echo "  --help   显示帮助信息"
  echo "说明: 统计目录及子目录空间占用"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

dir="$1"
if [[ ! -d "$dir" ]]; then
  echo "目录不存在: $dir"
  exit 1
fi

du -sh "$dir"/* 