#!/bin/bash

show_help() {
  echo "用法: $0 <文件> [--algo md5|sha1|sha256]"
  echo "  --algo A   哈希算法，默认md5"
  echo "  --help     显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

file="$1"
shift
algo="md5"

while [[ $# -gt 0 ]]; do
  case $1 in
    --algo)
      algo="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
 done

if [[ ! -f "$file" ]]; then
  echo "文件不存在: $file"
  exit 1
fi

case $algo in
  md5)
    md5sum "$file"
    ;;
  sha1)
    sha1sum "$file"
    ;;
  sha256)
    sha256sum "$file"
    ;;
  *)
    echo "不支持的算法: $algo"
    exit 2
    ;;
esac 