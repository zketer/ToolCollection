#!/bin/bash
# 网络测速工具
# 用法: ./net_speed_test.sh [--help]

show_help() {
  echo "用法: $0 [--help]"
  echo "测速本机到互联网的下载/上传速度。"
  echo "依赖: curl 或 speedtest-cli"
  exit 0
}

if [[ "$1" == "--help" ]]; then
  show_help
fi

if command -v speedtest &>/dev/null; then
  speedtest
else
  echo "未检测到 speedtest-cli，使用 curl 进行简单下载测速..."
  url="http://speedtest.tele2.net/10MB.zip"
  tmpfile="/tmp/speedtest_$$.bin"
  start=$(date +%s)
  curl -o "$tmpfile" -s "$url"
  end=$(date +%s)
  size=10 # MB
  duration=$((end-start))
  if [[ $duration -gt 0 ]]; then
    speed=$((size*8/duration))
    echo "下载速度: $speed Mbps (10MB/$duration 秒)"
  else
    echo "测速失败"
  fi
  rm -f "$tmpfile"
fi 