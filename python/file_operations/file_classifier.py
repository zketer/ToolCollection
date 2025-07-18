#!/usr/bin/env python3
"""
文件分类器

功能：
- 按文件类型/扩展名/自定义规则分类整理
- 支持移动或复制文件到目标目录
- 支持自定义规则（如按日期、大小等）

作者: ToolCollection
"""
import argparse
import os
import sys
import shutil
from pathlib import Path
import json
from datetime import datetime


def classify_by_type(src_dir, target_dir, move=False):
    src = Path(src_dir)
    tgt = Path(target_dir)
    for file in src.rglob('*'):
        if file.is_file():
            ext = file.suffix[1:] if file.suffix else 'no_ext'
            dest_dir = tgt / ext
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / file.name
            if move:
                shutil.move(str(file), str(dest))
            else:
                shutil.copy2(file, dest)
    print(f"✅ 按类型分类完成: {target_dir}")

def classify_by_rules(src_dir, target_dir, rules_file, move=False):
    src = Path(src_dir)
    tgt = Path(target_dir)
    with open(rules_file, 'r', encoding='utf-8') as f:
        rules = json.load(f)
    for file in src.rglob('*'):
        if file.is_file():
            matched = False
            for rule in rules.get('rules', []):
                if 'ext' in rule and file.suffix[1:] == rule['ext']:
                    dest_dir = tgt / rule.get('folder', rule['ext'])
                    matched = True
                elif 'contains' in rule and rule['contains'] in file.name:
                    dest_dir = tgt / rule.get('folder', rule['contains'])
                    matched = True
                elif 'date' in rule and datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d') == rule['date']:
                    dest_dir = tgt / rule.get('folder', rule['date'])
                    matched = True
                else:
                    continue
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest = dest_dir / file.name
                if move:
                    shutil.move(str(file), str(dest))
                else:
                    shutil.copy2(file, dest)
                break
            if not matched:
                other_dir = tgt / 'other'
                other_dir.mkdir(parents=True, exist_ok=True)
                dest = other_dir / file.name
                if move:
                    shutil.move(str(file), str(dest))
                else:
                    shutil.copy2(file, dest)
    print(f"✅ 按规则分类完成: {target_dir}")

def main():
    parser = argparse.ArgumentParser(
        description="文件分类器 - 按类型/规则分类整理，支持移动/复制",
        epilog="""
示例：
  # 按类型分类
  python file_classifier.py source_dir --target out_dir
  # 按规则分类
  python file_classifier.py source_dir --target out_dir --rules rules.json
  # 移动而非复制
  python file_classifier.py source_dir --target out_dir --move

规则文件示例（rules.json）：
{
  "rules": [
    {"ext": "jpg", "folder": "images"},
    {"contains": "report", "folder": "reports"},
    {"date": "2024-07-20", "folder": "today"}
  ]
}
        """
    )
    parser.add_argument('source', help='待分类的目录')
    parser.add_argument('--target', required=True, help='分类目标目录')
    parser.add_argument('--rules', help='自定义规则JSON文件')
    parser.add_argument('--move', action='store_true', help='移动文件而非复制')
    args = parser.parse_args()

    if args.rules:
        classify_by_rules(args.source, args.target, args.rules, args.move)
    else:
        classify_by_type(args.source, args.target, args.move)

if __name__ == "__main__":
    main() 