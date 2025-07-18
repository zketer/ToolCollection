#!/usr/bin/env python3
"""
端口扫描器

功能：
- 多线程端口扫描
- 支持端口范围、常用端口
- 简单服务识别

作者: ToolCollection
"""
import argparse
import sys
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_PORTS = {
    21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS', 80: 'HTTP', 110: 'POP3',
    143: 'IMAP', 443: 'HTTPS', 3306: 'MySQL', 3389: 'RDP', 6379: 'Redis', 5432: 'PostgreSQL',
    8080: 'HTTP-Alt', 27017: 'MongoDB', 1521: 'Oracle', 5900: 'VNC', 8000: 'HTTP-Dev'
}

def scan_port(host, port, timeout=1):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port, True
    except Exception:
        return port, False

def main():
    parser = argparse.ArgumentParser(
        description="端口扫描器 - 多线程端口扫描，支持端口范围、服务识别",
        epilog="""
示例：
  # 扫描常用端口
  python port_scanner.py example.com
  # 扫描端口范围
  python port_scanner.py example.com --ports 1-1024
  # 指定超时和线程数
  python port_scanner.py example.com --ports 20-100 --timeout 2 --threads 50
        """
    )
    parser.add_argument('host', help='目标主机')
    parser.add_argument('--ports', help='端口范围，如1-1000，默认常用端口')
    parser.add_argument('--timeout', type=float, default=1.0, help='超时时间（秒）')
    parser.add_argument('--threads', type=int, default=50, help='并发线程数')
    args = parser.parse_args()

    if args.ports:
        if '-' in args.ports:
            start, end = map(int, args.ports.split('-'))
            ports = list(range(start, end+1))
        else:
            ports = [int(p) for p in args.ports.split(',')]
    else:
        ports = list(COMMON_PORTS.keys())

    print(f'开始扫描 {args.host} 的 {len(ports)} 个端口...')
    open_ports = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_port = {executor.submit(scan_port, args.host, port, args.timeout): port for port in ports}
        for future in as_completed(future_to_port):
            port, ok = future.result()
            if ok:
                service = COMMON_PORTS.get(port, '')
                print(f'✅ 端口 {port} 开放 {service}')
                open_ports.append(port)
            else:
                pass  # 可选：print(f'❌ 端口 {port} 关闭')
    print(f'扫描完成，开放端口 {len(open_ports)}/{len(ports)}')
    if open_ports:
        print('开放端口列表:', ', '.join(map(str, sorted(open_ports))))

if __name__ == "__main__":
    main() 