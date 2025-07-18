#!/bin/bash

show_help() {
  echo "用法: $0 <主机> [--ports 端口范围]"
  echo "  --ports R   端口范围，如 1-1024，默认1-1024"
  echo "  --help      显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

host="$1"
shift
ports="1-1024"

while [[ $# -gt 0 ]]; do
  case $1 in
    --ports)
      ports="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
 done

IFS='-' read -r start end <<< "$ports"
echo "扫描 $host 端口 $start-$end ..."
for ((p=start; p<=end; p++)); do
  (echo > /dev/tcp/$host/$p) >/dev/null 2>&1 && echo "端口 $p: 开放"
done 