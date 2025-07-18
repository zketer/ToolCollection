#!/bin/bash

show_help() {
  echo "用法: $0 <目标目录> <报告文件> [--interval 分钟]"
  echo "  --interval N   生成间隔（分钟），默认60"
  echo "  --help         显示帮助信息"
  echo "说明: 持续定时生成目录/文件报告"
}

if [[ "$1" == "--help" || $# -lt 2 ]]; then
  show_help
  exit 0
fi

dir="$1"
report="$2"
shift 2
interval=60

while [[ $# -gt 0 ]]; do
  case $1 in
    --interval)
      interval="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
 done

if [[ ! -d "$dir" ]]; then
  echo "目录不存在: $dir"
  exit 1
fi

while true; do
  echo "[$(date)] 生成报告..."
  du -sh "$dir"/* > "$report"
  sleep $((interval*60))
done 