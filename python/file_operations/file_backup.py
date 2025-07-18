#!/usr/bin/env python3
"""
文件备份器

功能：
- 自动备份文件/目录，支持全量和增量备份
- 备份文件带时间戳，支持多版本
- 支持目录和单文件备份

作者: ToolCollection
"""
import argparse
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
import filecmp


def timestamp():
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def full_backup(source, target):
    src = Path(source)
    tgt = Path(target)
    if not tgt.exists():
        tgt.mkdir(parents=True)
    if src.is_file():
        backup_name = f"{src.stem}_{timestamp()}{src.suffix}"
        shutil.copy2(src, tgt / backup_name)
        print(f"✅ 文件已备份: {tgt / backup_name}")
    else:
        backup_dir = tgt / f"{src.name}_backup_{timestamp()}"
        shutil.copytree(src, backup_dir)
        print(f"✅ 目录已备份: {backup_dir}")

def incremental_backup(source, target):
    src = Path(source)
    tgt = Path(target)
    if not tgt.exists():
        tgt.mkdir(parents=True)
    if src.is_file():
        backup_name = f"{src.stem}_inc_{timestamp()}{src.suffix}"
        shutil.copy2(src, tgt / backup_name)
        print(f"✅ 文件已增量备份: {tgt / backup_name}")
    else:
        backup_dir = tgt / f"{src.name}_inc_{timestamp()}"
        backup_dir.mkdir(parents=True)
        for file in src.rglob('*'):
            if file.is_file():
                rel = file.relative_to(src)
                dest = backup_dir / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                # 仅备份新文件或内容有变化的文件
                orig = tgt / rel
                if not orig.exists() or not filecmp.cmp(file, orig, shallow=False):
                    shutil.copy2(file, dest)
        print(f"✅ 目录已增量备份: {backup_dir}")

def main():
    parser = argparse.ArgumentParser(
        description="文件备份器 - 自动备份/增量备份，带时间戳，支持多版本",
        epilog="""
示例：
  # 全量备份
  python file_backup.py source_dir --target backup_dir --mode full
  # 增量备份
  python file_backup.py source_dir --target backup_dir --mode incremental
        """
    )
    parser.add_argument('source', help='待备份的文件或目录')
    parser.add_argument('--target', required=True, help='备份目标目录')
    parser.add_argument('--mode', choices=['full', 'incremental'], default='full', help='备份模式')
    args = parser.parse_args()

    if args.mode == 'full':
        full_backup(args.source, args.target)
    else:
        incremental_backup(args.source, args.target)

if __name__ == "__main__":
    main() 