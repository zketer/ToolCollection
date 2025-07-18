#!/bin/bash

show_help() {
  echo "用法: $0 <url文件> [--dir 目录] [--help]"
  echo "  --dir DIR   下载到指定目录，默认当前目录"
  echo "  --help      显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

file="$1"
shift
dir="."

while [[ $# -gt 0 ]]; do
  case $1 in
    --dir)
      dir="$2"
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

mkdir -p "$dir"
while read -r url; do
  if [[ -z "$url" ]]; then continue; fi
  echo "下载: $url"
  curl -L -o "$dir/$(basename "$url")" "$url"
done < "$file" 