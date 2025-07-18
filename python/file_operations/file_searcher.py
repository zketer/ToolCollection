#!/usr/bin/env python3
"""
文件搜索器

功能：
- 按文件名/内容递归搜索
- 支持正则表达式
- 支持多目录
- 支持结果高亮

作者: ToolCollection
"""
import argparse
import os
import re
import sys
from pathlib import Path
from typing import List


def search_by_name(pattern: str, path: Path, regex: bool = False) -> List[Path]:
    matches = []
    if regex:
        pat = re.compile(pattern)
        for file in path.rglob('*'):
            if file.is_file() and pat.search(file.name):
                matches.append(file)
    else:
        for file in path.rglob(f'*{pattern}*'):
            if file.is_file():
                matches.append(file)
    return matches

def search_by_content(pattern: str, path: Path, regex: bool = False, encoding: str = 'utf-8') -> List[Path]:
    matches = []
    if regex:
        pat = re.compile(pattern)
    for file in path.rglob('*'):
        if file.is_file():
            try:
                with open(file, 'r', encoding=encoding, errors='ignore') as f:
                    for line in f:
                        if (regex and pat.search(line)) or (not regex and pattern in line):
                            matches.append(file)
                            break
            except Exception:
                continue
    return matches

def highlight(text, pattern, regex=False):
    if regex:
        return re.sub(pattern, lambda m: f'\033[31m{m.group(0)}\033[0m', text)
    else:
        return text.replace(pattern, f'\033[31m{pattern}\033[0m')

def main():
    parser = argparse.ArgumentParser(
        description="文件搜索器 - 按文件名/内容递归搜索，支持正则和多目录",
        epilog="""
示例：
  # 按文件名搜索
  python file_searcher.py pattern --path .
  # 按内容搜索
  python file_searcher.py pattern --path . --content
  # 正则搜索
  python file_searcher.py "\\.py$" --path src --regex
        """
    )
    parser.add_argument('pattern', help='搜索模式（文件名或内容）')
    parser.add_argument('--path', default='.', nargs='+', help='搜索路径（可多个）')
    parser.add_argument('--content', action='store_true', help='按内容搜索')
    parser.add_argument('--regex', action='store_true', help='使用正则表达式')
    parser.add_argument('--encoding', default='utf-8', help='文件编码')
    args = parser.parse_args()

    all_matches = set()
    for p in args.path:
        p = Path(p)
        if not p.exists():
            print(f'❌ 路径不存在: {p}')
            continue
        if args.content:
            matches = search_by_content(args.pattern, p, args.regex, args.encoding)
        else:
            matches = search_by_name(args.pattern, p, args.regex)
        for m in matches:
            all_matches.add(m.resolve())

    if not all_matches:
        print('未找到匹配项。')
        return
    print(f'共找到 {len(all_matches)} 个匹配文件：')
    for file in sorted(all_matches):
        print(highlight(str(file), args.pattern, args.regex))

if __name__ == "__main__":
    main() 