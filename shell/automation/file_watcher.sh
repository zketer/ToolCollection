#!/bin/bash

show_help() {
  echo "用法: $0 <目录>"
  echo "  --help   显示帮助信息"
  echo "说明: 依赖 inotifywait (Linux) 或 fswatch (macOS)" 
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

if command -v inotifywait >/dev/null 2>&1; then
  echo "使用 inotifywait 监控 $dir ..."
  inotifywait -m -r "$dir"
elif command -v fswatch >/dev/null 2>&1; then
  echo "使用 fswatch 监控 $dir ..."
  fswatch -r "$dir"
else
  echo "请安装 inotify-tools (Linux) 或 fswatch (macOS)"
  exit 2
fi 