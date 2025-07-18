#!/usr/bin/env python3
"""
数据采样器

功能：
- 数据采样（随机采样、分层采样、比例采样）
- 支持CSV/Excel/JSON
- 支持采样输出为CSV/Excel/JSON

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
    print(f'✅ 已保存采样结果: {output}')

def random_sample(df, n=None, frac=None, stratify=None, random_state=42):
    if stratify:
        # 分层采样
        sampled = df.groupby(stratify, group_keys=False).apply(
            lambda x: x.sample(n=min(len(x), n) if n else int(len(x)*frac), random_state=random_state)
        )
        return sampled.reset_index(drop=True)
    else:
        return df.sample(n=n, frac=frac, random_state=random_state)

def main():
    parser = argparse.ArgumentParser(
        description="数据采样器 - 支持随机/分层/比例采样，输出多格式",
        epilog="""
示例：
  # 随机采样100条
  python data_sampler.py data.csv --n 100 --output sample.csv
  # 按比例采样10%
  python data_sampler.py data.csv --frac 0.1 --output sample.csv
  # 分层采样
  python data_sampler.py data.csv --n 10 --stratify label --output sample.csv
        """
    )
    parser.add_argument('input', help='输入数据文件（CSV/Excel/JSON）')
    parser.add_argument('--n', type=int, help='采样数量')
    parser.add_argument('--frac', type=float, help='采样比例')
    parser.add_argument('--stratify', help='分层采样字段')
    parser.add_argument('--output', required=True, help='输出文件（CSV/Excel/JSON）')
    parser.add_argument('--random-state', type=int, default=42, help='随机种子')
    args = parser.parse_args()

    try:
        df = read_data(args.input)
        sampled = random_sample(df, n=args.n, frac=args.frac, stratify=args.stratify, random_state=args.random_state)
        save_data(sampled, args.output)
    except Exception as e:
        print(f'❌ 采样失败: {e}')
        sys.exit(1)

if __name__ == "__main__":
    main() 