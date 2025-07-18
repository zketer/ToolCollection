#!/bin/bash

show_help() {
  echo "用法: $0 <源目录> <目标目录> [--interval 分钟]"
  echo "  --interval N   备份间隔（分钟），默认60"
  echo "  --help         显示帮助信息"
  echo "说明: 持续定时自动备份，基于 rsync"
}

if [[ "$1" == "--help" || $# -lt 2 ]]; then
  show_help
  exit 0
fi

src="$1"
dst="$2"
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

if [[ ! -d "$src" || ! -d "$dst" ]]; then
  echo "目录不存在: $src 或 $dst"
  exit 1
fi

while true; do
  echo "[$(date)] 正在备份..."
  rsync -av "$src/" "$dst/"
  sleep $((interval*60))
done 