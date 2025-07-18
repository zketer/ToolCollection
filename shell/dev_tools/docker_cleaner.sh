#!/bin/bash

show_help() {
  echo "用法: $0 [--all]"
  echo "  --all   清理所有容器、镜像、网络、卷"
  echo "  --help  显示帮助信息"
  echo "说明: 默认仅清理已停止容器和悬挂镜像"
}

if [[ "$1" == "--help" ]]; then
  show_help
  exit 0
fi

if [[ "$1" == "--all" ]]; then
  docker system prune -a --volumes -f
  echo "已清理所有容器、镜像、网络、卷"
else
  docker container prune -f
  docker image prune -f
  docker network prune -f
  docker volume prune -f
  echo "已清理已停止容器、悬挂镜像、未用网络和卷"
fi 