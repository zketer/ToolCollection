#!/bin/bash

show_help() {
  echo "用法: $0 <目录>"
  echo "  --help   显示帮助信息"
  echo "说明: 查找空文件和空目录"
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

find "$dir" -type f -empty -print
find "$dir" -type d -empty -print 