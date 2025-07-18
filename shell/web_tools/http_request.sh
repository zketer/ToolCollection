#!/bin/bash

show_help() {
  echo "用法: $0 <URL> [--method GET|POST|PUT|DELETE] [--data DATA] [--header 'K:V'] [--help]"
  echo "  --method M   HTTP 方法，默认GET"
  echo "  --data D     POST/PUT 数据"
  echo "  --header H   自定义请求头，可多次"
  echo "  --help       显示帮助信息"
}

if [[ "$1" == "--help" || $# -eq 0 ]]; then
  show_help
  exit 0
fi

url="$1"
shift
method="GET"
data=""
headers=()

while [[ $# -gt 0 ]]; do
  case $1 in
    --method)
      method="$2"
      shift 2
      ;;
    --data)
      data="$2"
      shift 2
      ;;
    --header)
      headers+=("-H" "$2")
      shift 2
      ;;
    *)
      shift
      ;;
  esac
 done

cmd=(curl -s -X "$method" "${headers[@]}" "$url")
if [[ -n "$data" ]]; then
  cmd+=( -d "$data" )
fi
echo "请求: ${cmd[*]}"
"${cmd[@]}" 