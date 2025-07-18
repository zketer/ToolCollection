#!/bin/bash

show_help() {
  echo "用法: $0 <输出文件>"
  echo "  --help   显示帮助信息"
  echo "说明: 导出当前 shell 环境变量为 .env 文件"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

outfile="$1"
printenv | awk -F= '{print $1"="\""$2"\""}' > "$outfile"
echo "已导出到: $outfile" 