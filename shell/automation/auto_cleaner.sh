#!/bin/bash

show_help() {
  echo "用法: $0 <目标目录> [--days N] [--pattern PATTERN] [--interval 分钟]"
  echo "  --days N      删除N天前的文件"
  echo "  --pattern P   匹配文件名模式（如 *.log）"
  echo "  --interval N  清理间隔（分钟），默认60"
  echo "  --help        显示帮助信息"
  echo "说明: 持续定时自动清理，基于 find"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

dir="$1"
shift
days=""
pattern="*"
interval=60

while [[ $# -gt 0 ]]; do
  case $1 in
    --days)
      days="$2"
      shift 2
      ;;
    --pattern)
      pattern="$2"
      shift 2
      ;;
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
  echo "[$(date)] 正在清理..."
  if [[ -n "$days" ]]; then
    find "$dir" -name "$pattern" -type f -mtime +$days -delete
  else
    find "$dir" -name "$pattern" -type f -delete
  fi
  sleep $((interval*60))
done 