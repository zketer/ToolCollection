#!/bin/bash

show_help() {
  echo "用法: $0 <文件> --lines N [--prefix 前缀]"
  echo "  --lines N    每个分割文件的行数"
  echo "  --prefix P   输出文件前缀，默认split_"
  echo "  --help       显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

file="$1"
shift
lines=""
prefix="split_"

while [[ $# -gt 0 ]]; do
  case $1 in
    --lines)
      lines="$2"
      shift 2
      ;;
    --prefix)
      prefix="$2"
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

if [[ -z "$lines" ]]; then
  echo "必须指定 --lines 参数"
  show_help
  exit 1
fi

split -l "$lines" "$file" "$prefix"
echo "已分割为: ${prefix}*" 