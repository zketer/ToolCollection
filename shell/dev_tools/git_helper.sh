#!/bin/bash

show_help() {
  echo "用法: $0 [--status] [--pull] [--push] [--log N] [--help]"
  echo "  --status   显示当前仓库状态"
  echo "  --pull     拉取最新代码"
  echo "  --push     推送本地提交"
  echo "  --log N    显示最近N条提交记录"
  echo "  --help     显示帮助信息"
}

if [[ $# -eq 0 || "$1" == "--help" ]]; then
  show_help
  exit 0
fi

case $1 in
  --status)
    git status
    ;;
  --pull)
    git pull
    ;;
  --push)
    git push
    ;;
  --log)
    shift
    git log -n "$1" --oneline
    ;;
  *)
    show_help
    ;;
esac 