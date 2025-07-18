#!/bin/bash

show_help() {
  echo "用法: $0 <进程名> [--interval 秒]"
  echo "  --interval N   监控间隔秒数，默认5"
  echo "  --help         显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

proc="$1"
shift
interval=5

while [[ $# -gt 0 ]]; do
  case $1 in
    --interval)
      interval="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
 done

while true; do
  date
  ps aux | grep "$proc" | grep -v grep
  echo "---"
  sleep $interval
 done 