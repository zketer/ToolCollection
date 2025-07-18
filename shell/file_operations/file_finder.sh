#!/bin/bash

show_help() {
  echo "用法: $0 <目录> [--name 关键字] [--ext 扩展名] [--size +N/-N] [--help]"
  echo "  --name KW   文件名包含关键字"
  echo "  --ext EXT   指定扩展名(如 txt)"
  echo "  --size +N/-N 文件大小大于(+N)或小于(-N)字节"
  echo "  --help      显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

dir="$1"
shift
name=""
ext=""
size=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --name)
      name="$2"
      shift 2
      ;;
    --ext)
      ext="$2"
      shift 2
      ;;
    --size)
      size="$2"
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

find_cmd=(find "$dir" -type f)
if [[ -n "$name" ]]; then
  find_cmd+=( -name "*$name*" )
fi
if [[ -n "$ext" ]]; then
  find_cmd+=( -name "*.$ext" )
fi
if [[ -n "$size" ]]; then
  find_cmd+=( -size "$size"c )
fi

"${find_cmd[@]}" 