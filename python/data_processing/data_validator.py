#!/usr/bin/env python3
"""
数据验证器

功能：
- 数据质量检查（空值、唯一性、类型）
- 支持CSV/Excel/JSON
- 支持自定义规则校验（JSON配置）

作者: ToolCollection
"""
import argparse
import sys
import pandas as pd
import json
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

def check_nulls(df):
    nulls = df.isnull().sum()
    print('空值统计:')
    print(nulls[nulls > 0])
    return nulls

def check_unique(df, columns):
    for col in columns:
        if not df[col].is_unique:
            print(f'❌ 列 {col} 存在重复值')
        else:
            print(f'✅ 列 {col} 唯一')

def check_types(df, types):
    for col, typ in types.items():
        if col not in df.columns:
            print(f'⚠️ 列 {col} 不存在')
            continue
        if typ == 'int' and not pd.api.types.is_integer_dtype(df[col]):
            print(f'❌ 列 {col} 不是整数类型')
        elif typ == 'float' and not pd.api.types.is_float_dtype(df[col]):
            print(f'❌ 列 {col} 不是浮点类型')
        elif typ == 'str' and not pd.api.types.is_string_dtype(df[col]):
            print(f'❌ 列 {col} 不是字符串类型')
        else:
            print(f'✅ 列 {col} 类型为 {typ}')

def apply_custom_rules(df, rules_file):
    with open(rules_file, 'r', encoding='utf-8') as f:
        rules = json.load(f)
    if 'unique' in rules:
        check_unique(df, rules['unique'])
    if 'types' in rules:
        check_types(df, rules['types'])
    if 'not_null' in rules:
        for col in rules['not_null']:
            if df[col].isnull().any():
                print(f'❌ 列 {col} 存在空值')
            else:
                print(f'✅ 列 {col} 无空值')

def main():
    parser = argparse.ArgumentParser(
        description="数据验证器 - 数据质量检查，支持自定义规则",
        epilog="""
示例：
  # 检查空值
  python data_validator.py data.csv --nulls
  # 检查唯一性
  python data_validator.py data.csv --unique id
  # 检查类型
  python data_validator.py data.csv --types '{"age": "int", "name": "str"}'
  # 按规则校验
  python data_validator.py data.csv --rules rules.json

规则文件示例（rules.json）：
{
  "unique": ["id"],
  "types": {"age": "int", "name": "str"},
  "not_null": ["id", "name"]
}
        """
    )
    parser.add_argument('input', help='输入数据文件（CSV/Excel/JSON）')
    parser.add_argument('--nulls', action='store_true', help='检查空值')
    parser.add_argument('--unique', nargs='+', help='检查唯一性列')
    parser.add_argument('--types', help='检查类型，JSON字符串')
    parser.add_argument('--rules', help='自定义规则JSON文件')
    args = parser.parse_args()

    try:
        df = read_data(args.input)
        if args.rules:
            apply_custom_rules(df, args.rules)
        else:
            if args.nulls:
                check_nulls(df)
            if args.unique:
                check_unique(df, args.unique)
            if args.types:
                types = json.loads(args.types)
                check_types(df, types)
    except Exception as e:
        print(f'❌ 校验失败: {e}')
        sys.exit(1)

if __name__ == "__main__":
    main() 