#!/usr/bin/env python3
"""
DNS查询器

功能：
- 查询A/AAAA/MX/CNAME/TXT等DNS记录
- 支持批量域名查询
- 支持自定义DNS服务器

作者: ToolCollection
"""
import argparse
import sys
import dns.resolver


def query_dns(domain, record_type, dns_server=None):
    resolver = dns.resolver.Resolver()
    if dns_server:
        resolver.nameservers = [dns_server]
    try:
        answers = resolver.resolve(domain, record_type)
        return [str(r) for r in answers]
    except Exception as e:
        return [f'❌ 查询失败: {e}']

def main():
    parser = argparse.ArgumentParser(
        description="DNS查询器 - 查询A/AAAA/MX/CNAME/TXT等记录，支持批量域名",
        epilog="""
示例：
  # 查询A记录
  python dns_lookup.py example.com --type A
  # 查询MX记录
  python dns_lookup.py example.com --type MX
  # 批量查询
  python dns_lookup.py --file domains.txt --type A
  # 指定DNS服务器
  python dns_lookup.py example.com --type A --dns 8.8.8.8
        """
    )
    parser.add_argument('domain', nargs='?', help='要查询的域名')
    parser.add_argument('--file', help='批量域名文件，每行一个')
    parser.add_argument('--type', default='A', help='记录类型（A, AAAA, MX, CNAME, TXT等）')
    parser.add_argument('--dns', help='自定义DNS服务器')
    args = parser.parse_args()

    domains = []
    if args.domain:
        domains.append(args.domain)
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            domains += [line.strip() for line in f if line.strip()]
    if not domains:
        print('请指定域名或域名文件')
        sys.exit(1)

    for domain in domains:
        print(f'🔍 {domain} [{args.type}]')
        results = query_dns(domain, args.type, args.dns)
        for r in results:
            print(f'  {r}')

if __name__ == "__main__":
    main() 