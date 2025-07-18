#!/bin/bash
# 日志清理与归档工具
# 用法: ./log_cleaner.sh <目录> [--days N] [--size M] [--archive] [--help]

show_help() {
  echo "用法: $0 <目录> [--days N] [--size M] [--archive] [--help]"
  echo "清理指定目录下N天前或大于M MB的日志文件，可自动归档。"
  exit 0
}

if [[ "$1" == "--help" || "$#" -eq 0 ]]; then
  show_help
fi

dir="$1"; shift
days=0; size=0; archive=0
while [[ $# -gt 0 ]]; do
  case $1 in
    --days) days="$2"; shift 2;;
    --size) size="$2"; shift 2;;
    --archive) archive=1; shift;;
    *) shift;;
  esac
done

cd "$dir" || exit 1
if [[ $archive -eq 1 ]]; then
  mkdir -p archive
fi
for f in *.log; do
  [[ -f "$f" ]] || continue
  del=0
  if [[ $days -gt 0 ]]; then
    if [[ $(find "$f" -mtime +$days) ]]; then del=1; fi
  fi
  if [[ $size -gt 0 ]]; then
    fsize=$(du -m "$f" | cut -f1)
    if [[ $fsize -gt $size ]]; then del=1; fi
  fi
  if [[ $del -eq 1 ]]; then
    if [[ $archive -eq 1 ]]; then
      mv "$f" archive/
      echo "已归档: $f"
    else
      rm "$f"
      echo "已删除: $f"
    fi
  fi
done 