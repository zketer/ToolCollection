#!/bin/bash

show_help() {
  echo "用法: $0 [--zip <目录/文件> <压缩包名>] [--unzip <压缩包> <目标目录>]"
  echo "  --zip SRC ZIPFILE     压缩 SRC 为 ZIPFILE.zip"
  echo "  --unzip ZIPFILE DIR   解压 ZIPFILE.zip 到 DIR"
  echo "  --help               显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

if [[ "$1" == "--zip" && $# -eq 3 ]]; then
  src="$2"
  zipfile="$3"
  zip -r "$zipfile.zip" "$src"
  exit $?
fi

if [[ "$1" == "--unzip" && $# -eq 3 ]]; then
  zipfile="$2"
  dstdir="$3"
  unzip "$zipfile" -d "$dstdir"
  exit $?
fi

echo "参数错误！"
show_help
exit 1 