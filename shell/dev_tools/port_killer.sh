#!/bin/bash
# 端口查杀工具
# 用法: ./port_killer.sh <端口> [--help]

show_help() {
  echo "用法: $0 <端口> [--help]"
  echo "查找并kill指定端口的进程。"
  exit 0
}

if [[ "$1" == "--help" || "$#" -eq 0 ]]; then
  show_help
fi

port="$1"
if [[ "$OSTYPE" == "darwin"* ]]; then
  pid=$(lsof -ti tcp:$port)
else
  pid=$(lsof -t -i:$port)
fi
if [[ -z "$pid" ]]; then
  echo "未找到占用端口 $port 的进程"
  exit 0
fi
echo "杀死进程: $pid (端口: $port)"
kill -9 $pid 