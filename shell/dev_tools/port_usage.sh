#!/bin/bash

show_help() {
  echo "用法: $0 <端口号>"
  echo "  --help   显示帮助信息"
  echo "说明: 查询指定端口被哪个进程占用"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

port="$1"
if lsof -i :$port | grep LISTEN; then
  lsof -i :$port
else
  echo "端口 $port 未被占用"
fi 