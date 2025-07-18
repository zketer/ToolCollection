#!/bin/bash

show_help() {
  echo "用法: $0 <源目录> <目标目录> [--delete]"
  echo "  --delete   目标目录中源目录没有的文件也会被删除"
  echo "  --help     显示帮助信息"
  echo "说明: 基于 rsync 实现，需预装 rsync"
}

if [[ "$1" == "--help" || $# -lt 2 ]]; then
  show_help
  exit 0
fi

src="$1"
dst="$2"
shift 2
delete_flag=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --delete)
      delete_flag="--delete"
      shift
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

rsync -av $delete_flag "$src/" "$dst/" 