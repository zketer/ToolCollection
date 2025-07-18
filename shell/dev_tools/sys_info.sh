#!/bin/bash
# 系统信息一键查看工具
# 用法: ./sys_info.sh [--help]

if [[ "$1" == "--help" ]]; then
  echo "用法: $0 [--help]"
  echo "显示主机名、操作系统、CPU、内存、磁盘、网络等信息"
  exit 0
fi

echo "===== 主机名 ====="
hostname

echo "===== 操作系统 ====="
uname -a

echo "===== CPU 信息 ====="
if command -v lscpu &>/dev/null; then
  lscpu | grep -E 'Model name|Socket|Thread|Core|CPU\(' || true
else
  sysctl -a | grep machdep.cpu || true
fi

echo "===== 内存信息 ====="
if command -v free &>/dev/null; then
  free -h
else
  vm_stat || true
fi

echo "===== 磁盘信息 ====="
df -h

echo "===== 网络信息 ====="
ifconfig || ip addr 