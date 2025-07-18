#!/bin/bash
# 目录自动备份工具
# 用法: ./backup_dir.sh <目录> [--keep N] [--help]

show_help() {
  echo "用法: $0 <目录> [--keep N] [--help]"
  echo "将目录压缩备份，文件名带时间戳，自动保留最近N份。"
  exit 0
}

if [[ "$1" == "--help" || "$#" -eq 0 ]]; then
  show_help
fi

dir="$1"; shift
keep=5
while [[ $# -gt 0 ]]; do
  case $1 in
    --keep) keep="$2"; shift 2;;
    *) shift;;
  esac
done

base=$(basename "$dir")
date=$(date +%Y%m%d_%H%M%S)
backup_file="${base}_backup_${date}.tar.gz"
tar -czf "$backup_file" "$dir"
echo "已备份: $backup_file"

# 保留最近N份
ls -1t ${base}_backup_*.tar.gz | tail -n +$((keep+1)) | xargs -r rm -v 