#!/bin/bash

show_help() {
  echo "用法: $0 <git目录>"
  echo "  --help   显示帮助信息"
  echo "说明: 自动 git pull 并显示更新摘要"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

dir="$1"
if [[ ! -d "$dir/.git" ]]; then
  echo "不是有效的 git 仓库: $dir"
  exit 1
fi

cd "$dir"
git fetch
git status
git pull 