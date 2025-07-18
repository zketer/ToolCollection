#!/bin/bash

show_help() {
  echo "用法: $0 <消息内容>"
  echo "  --help   显示帮助信息"
  echo "说明: 支持 macOS (osascript)、Linux (notify-send)" 
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

msg="$1"
if command -v osascript >/dev/null 2>&1; then
  osascript -e "display notification \"$msg\" with title \"通知\""
elif command -v notify-send >/dev/null 2>&1; then
  notify-send "通知" "$msg"
else
  echo "$msg"
fi 