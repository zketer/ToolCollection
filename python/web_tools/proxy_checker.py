#!/usr/bin/env python3
"""
代理检测器

功能：
- 批量检测HTTP/HTTPS代理可用性
- 支持代理列表文件
- 支持超时设置，输出可用代理

作者: ToolCollection
"""
import argparse
import sys
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def check_proxy(proxy, timeout=5):
    proxies = {
        'http': proxy,
        'https': proxy
    }
    try:
        r = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=timeout)
        if r.status_code == 200:
            return proxy, True
    except Exception:
        pass
    return proxy, False

def main():
    parser = argparse.ArgumentParser(
        description="代理检测器 - 批量检测HTTP/HTTPS代理可用性",
        epilog="""
示例：
  # 检查单个代理
  python proxy_checker.py http://127.0.0.1:8080
  # 检查代理列表
  python proxy_checker.py --file proxies.txt
        """
    )
    parser.add_argument('proxy', nargs='?', help='代理地址（如 http://ip:port）')
    parser.add_argument('--file', help='代理列表文件，每行一个')
    parser.add_argument('--timeout', type=int, default=5, help='超时时间（秒）')
    parser.add_argument('--threads', type=int, default=10, help='并发线程数')
    args = parser.parse_args()

    proxies = []
    if args.proxy:
        proxies.append(args.proxy)
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            proxies += [line.strip() for line in f if line.strip()]
    if not proxies:
        print('请指定代理地址或代理列表文件')
        sys.exit(1)

    print(f'开始检测 {len(proxies)} 个代理...')
    available = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_proxy = {executor.submit(check_proxy, p, args.timeout): p for p in proxies}
        for future in as_completed(future_to_proxy):
            proxy, ok = future.result()
            if ok:
                print(f'✅ 可用: {proxy}')
                available.append(proxy)
            else:
                print(f'❌ 不可用: {proxy}')
    print(f'检测完成，可用代理 {len(available)}/{len(proxies)}')
    if available:
        with open('available_proxies.txt', 'w', encoding='utf-8') as f:
            for p in available:
                f.write(p + '\n')
        print('可用代理已保存到 available_proxies.txt')

if __name__ == "__main__":
    main() 