#!/usr/bin/env python3
"""
数据合并器

功能：
- 多源数据合并（支持CSV/Excel/JSON）
- 支持按字段合并、追加、去重
- 支持输出为CSV/Excel/JSON

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

def merge_data(files, on=None, how='outer', dedup=False):
    dfs = [read_data(f) for f in files]
    if on:
        from functools import reduce
        df_merged = reduce(lambda left, right: pd.merge(left, right, on=on, how=how), dfs)
    else:
        df_merged = pd.concat(dfs, ignore_index=True)
    if dedup:
        df_merged = df_merged.drop_duplicates()
    return df_merged

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
    print(f'✅ 已保存合并结果: {output}')

def main():
    parser = argparse.ArgumentParser(
        description="数据合并器 - 多源数据合并，支持按字段合并、追加、去重",
        epilog="""
示例：
  # 合并多个CSV
  python data_merger.py file1.csv file2.csv --output merged.csv
  # 按字段合并
  python data_merger.py file1.csv file2.csv --on id --output merged.csv
  # 合并并去重
  python data_merger.py file1.csv file2.csv --output merged.csv --dedup
        """
    )
    parser.add_argument('inputs', nargs='+', help='待合并的数据文件（CSV/Excel/JSON）')
    parser.add_argument('--on', help='按字段合并')
    parser.add_argument('--how', choices=['outer', 'inner', 'left', 'right'], default='outer', help='合并方式')
    parser.add_argument('--dedup', action='store_true', help='合并后去重')
    parser.add_argument('--output', required=True, help='输出文件（CSV/Excel/JSON）')
    args = parser.parse_args()

    try:
        df = merge_data(args.inputs, args.on, args.how, args.dedup)
        save_data(df, args.output)
    except Exception as e:
        print(f'❌ 合并失败: {e}')
        sys.exit(1)

if __name__ == "__main__":
    main() 