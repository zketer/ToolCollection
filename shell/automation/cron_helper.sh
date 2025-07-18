#!/bin/bash

show_help() {
  echo "用法: $0 [--list] [--add '<表达式> <命令>'] [--remove <关键字>]"
  echo "  --list           列出当前用户的所有定时任务"
  echo "  --add EXPR CMD   添加定时任务（需用引号包裹表达式和命令）"
  echo "  --remove KW      删除包含关键字的定时任务"
  echo "  --help           显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

case $1 in
  --list)
    crontab -l
    ;;
  --add)
    shift
    expr_cmd="$1"
    (crontab -l; echo "$expr_cmd") | crontab -
    echo "已添加: $expr_cmd"
    ;;
  --remove)
    shift
    kw="$1"
    crontab -l | grep -v "$kw" | crontab -
    echo "已删除包含: $kw 的定时任务"
    ;;
  *)
    show_help
    ;;
esac 