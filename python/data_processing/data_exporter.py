#!/usr/bin/env python3
"""
数据导出器

功能：
- 多格式数据导出（CSV/Excel/JSON）
- 支持字段选择、过滤、排序
- 支持CSV/Excel/JSON输入

作者: ToolCollection
"""
import argparse
import sys
import pandas as pd
from pathlib import Path


def read_data(file):
    file = Path(file)
    if file.suffix.lower() in ['.csv']:
        return pd.read_csv(file)
    elif file.suffix.lower() in ['.xlsx', '.xls']:
        return pd.read_excel(file)
    elif file.suffix.lower() in ['.json']:
        return pd.read_json(file)
    else:
        raise ValueError(f'不支持的文件类型: {file}')

def save_data(df, output):
    out = Path(output)
    if out.suffix.lower() == '.csv':
        df.to_csv(out, index=False)
    elif out.suffix.lower() in ['.xlsx', '.xls']:
        df.to_excel(out, index=False)
    elif out.suffix.lower() == '.json':
        df.to_json(out, orient='records', force_ascii=False, indent=2)
    else:
        raise ValueError(f'不支持的输出格式: {out}')
    print(f'✅ 已导出数据: {output}')

def main():
    parser = argparse.ArgumentParser(
        description="数据导出器 - 多格式导出，支持字段选择、过滤、排序",
        epilog="""
示例：
  # 导出为CSV
  python data_exporter.py data.json --output out.csv
  # 只导出部分字段
  python data_exporter.py data.csv --fields id name --output out.csv
  # 过滤
  python data_exporter.py data.csv --filter "age>30" --output out.csv
  # 排序
  python data_exporter.py data.csv --sort age --output out.csv
        """
    )
    parser.add_argument('input', help='输入数据文件（CSV/Excel/JSON）')
    parser.add_argument('--fields', nargs='+', help='导出字段')
    parser.add_argument('--filter', help='过滤条件，如 age>30')
    parser.add_argument('--sort', help='排序字段')
    parser.add_argument('--output', required=True, help='输出文件（CSV/Excel/JSON）')
    args = parser.parse_args()

    try:
        df = read_data(args.input)
        if args.fields:
            df = df[args.fields]
        if args.filter:
            df = df.query(args.filter)
        if args.sort:
            df = df.sort_values(by=args.sort)
        save_data(df, args.output)
    except Exception as e:
        print(f'❌ 导出失败: {e}')
        sys.exit(1)

if __name__ == "__main__":
    main() 