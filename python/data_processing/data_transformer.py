#!/usr/bin/env python3
"""
数据转换器 - 数据格式转换和预处理工具

功能:
- 多种数据格式转换 (CSV, JSON, XML, YAML, Excel)
- 数据编码转换
- 数据类型转换
- 数据标准化和归一化
- 特征工程
- 数据采样和分割

作者: ToolCollection Team
版本: 1.0.0
"""

import pandas as pd
import numpy as np
import json
import yaml
import xml.etree.ElementTree as ET
from pathlib import Path
import argparse
import sys
from typing import Dict, List, Any, Optional, Union
import logging
from datetime import datetime
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import hashlib
import re

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DataTransformer:
    """数据转换器类"""
    
    def __init__(self, data: Optional[Union[pd.DataFrame, Dict, List]] = None):
        """
        初始化数据转换器
        
        Args:
            data: 输入数据
        """
        self.data = data
        self.transformers = {}
    
    def load_data(self, file_path: str, **kwargs) -> Union[pd.DataFrame, Dict, List]:
        """
        加载数据
        
        Args:
            file_path: 数据文件路径
            **kwargs: 读取参数
            
        Returns:
            加载的数据
        """
        try:
            file_path = Path(file_path)
            
            if file_path.suffix.lower() == '.csv':
                self.data = pd.read_csv(file_path, **kwargs)
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                self.data = pd.read_excel(file_path, **kwargs)
            elif file_path.suffix.lower() == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            elif file_path.suffix.lower() in ['.yaml', '.yml']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.data = yaml.safe_load(f)
            elif file_path.suffix.lower() == '.xml':
                tree = ET.parse(file_path)
                root = tree.getroot()
                self.data = self._xml_to_dict(root)
            elif file_path.suffix.lower() == '.parquet':
                self.data = pd.read_parquet(file_path, **kwargs)
            elif file_path.suffix.lower() == '.pickle':
                self.data = pd.read_pickle(file_path, **kwargs)
            else:
                raise ValueError(f"不支持的文件格式: {file_path.suffix}")
            
            logger.info(f"成功加载数据: {file_path}")
            return self.data
        except Exception as e:
            logger.error(f"加载数据失败: {e}")
            raise
    
    def _xml_to_dict(self, element: ET.Element) -> Dict[str, Any]:
        """XML元素转换为字典"""
        result = {}
        for child in element:
            if len(child) == 0:
                result[child.tag] = child.text
            else:
                result[child.tag] = self._xml_to_dict(child)
        return result
    
    def save_data(self, output_path: str, format_type: Optional[str] = None, **kwargs) -> None:
        """
        保存数据
        
        Args:
            output_path: 输出文件路径
            format_type: 输出格式
            **kwargs: 保存参数
        """
        try:
            output_path = Path(output_path)
            
            if format_type:
                output_path = output_path.with_suffix(f'.{format_type}')
            
            if output_path.suffix.lower() == '.csv':
                if isinstance(self.data, pd.DataFrame):
                    self.data.to_csv(output_path, index=False, **kwargs)
                else:
                    pd.DataFrame(self.data).to_csv(output_path, index=False, **kwargs)
            
            elif output_path.suffix.lower() in ['.xlsx', '.xls']:
                if isinstance(self.data, pd.DataFrame):
                    self.data.to_excel(output_path, index=False, **kwargs)
                else:
                    pd.DataFrame(self.data).to_excel(output_path, index=False, **kwargs)
            
            elif output_path.suffix.lower() == '.json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=2, **kwargs)
            
            elif output_path.suffix.lower() in ['.yaml', '.yml']:
                with open(output_path, 'w', encoding='utf-8') as f:
                    yaml.dump(self.data, f, default_flow_style=False, allow_unicode=True, **kwargs)
            
            elif output_path.suffix.lower() == '.xml':
                if isinstance(self.data, dict):
                    root = self._dict_to_xml(self.data)
                    tree = ET.ElementTree(root)
                    tree.write(output_path, encoding='utf-8', xml_declaration=True, **kwargs)
            
            elif output_path.suffix.lower() == '.parquet':
                if isinstance(self.data, pd.DataFrame):
                    self.data.to_parquet(output_path, **kwargs)
                else:
                    pd.DataFrame(self.data).to_parquet(output_path, **kwargs)
            
            elif output_path.suffix.lower() == '.pickle':
                if isinstance(self.data, pd.DataFrame):
                    self.data.to_pickle(output_path, **kwargs)
                else:
                    pd.DataFrame(self.data).to_pickle(output_path, **kwargs)
            
            else:
                raise ValueError(f"不支持的输出格式: {output_path.suffix}")
            
            logger.info(f"数据已保存到: {output_path}")
        except Exception as e:
            logger.error(f"保存数据失败: {e}")
            raise
    
    def _dict_to_xml(self, data: Dict[str, Any], root_name: str = 'root') -> ET.Element:
        """字典转换为XML元素"""
        root = ET.Element(root_name)
        for key, value in data.items():
            child = ET.SubElement(root, key)
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    sub_child = ET.SubElement(child, sub_key)
                    sub_child.text = str(sub_value)
            else:
                child.text = str(value)
        return root
    
    def convert_encoding(self, source_encoding: str, target_encoding: str = 'utf-8') -> None:
        """
        转换数据编码
        
        Args:
            source_encoding: 源编码
            target_encoding: 目标编码
        """
        if isinstance(self.data, str):
            self.data = self.data.encode(source_encoding).decode(target_encoding)
        elif isinstance(self.data, pd.DataFrame):
            for col in self.data.select_dtypes(include=['object']):
                self.data[col] = self.data[col].astype(str).str.encode(source_encoding).str.decode(target_encoding)
        
        logger.info(f"编码转换完成: {source_encoding} -> {target_encoding}")
    
    def convert_data_types(self, type_mapping: Dict[str, str]) -> None:
        """
        转换数据类型
        
        Args:
            type_mapping: 类型映射字典
        """
        if not isinstance(self.data, pd.DataFrame):
            self.data = pd.DataFrame(self.data)
        
        for column, dtype in type_mapping.items():
            if column in self.data.columns:
                try:
                    if dtype == 'datetime':
                        self.data[column] = pd.to_datetime(self.data[column])
                    elif dtype == 'category':
                        self.data[column] = self.data[column].astype('category')
                    else:
                        self.data[column] = self.data[column].astype(dtype)
                    logger.info(f"列 {column} 类型转换为 {dtype}")
                except Exception as e:
                    logger.warning(f"列 {column} 类型转换失败: {e}")
    
    def normalize_data(self, method: str = 'standard', columns: Optional[List[str]] = None) -> None:
        """
        数据标准化/归一化
        
        Args:
            method: 标准化方法 ('standard', 'minmax', 'robust')
            columns: 要标准化的列名
        """
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("数据必须是DataFrame格式")
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        numeric_data = self.data[columns].dropna()
        
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'robust':
            from sklearn.preprocessing import RobustScaler
            scaler = RobustScaler()
        else:
            raise ValueError(f"不支持的标准化方法: {method}")
        
        scaled_data = scaler.fit_transform(numeric_data)
        self.data[columns] = scaled_data
        
        self.transformers[f'{method}_scaler'] = scaler
        logger.info(f"数据标准化完成: {method}")
    
    def encode_categorical(self, columns: Optional[List[str]] = None, 
                          method: str = 'label') -> None:
        """
        分类变量编码
        
        Args:
            columns: 要编码的列名
            method: 编码方法 ('label', 'onehot', 'hash')
        """
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("数据必须是DataFrame格式")
        
        if columns is None:
            columns = self.data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if method == 'label':
            for col in columns:
                if col in self.data.columns:
                    le = LabelEncoder()
                    self.data[col] = le.fit_transform(self.data[col].astype(str))
                    self.transformers[f'label_encoder_{col}'] = le
        
        elif method == 'onehot':
            self.data = pd.get_dummies(self.data, columns=columns, prefix=columns)
        
        elif method == 'hash':
            for col in columns:
                if col in self.data.columns:
                    self.data[f'{col}_hash'] = self.data[col].astype(str).apply(
                        lambda x: int(hashlib.md5(x.encode()).hexdigest(), 16) % 1000
                    )
        
        logger.info(f"分类变量编码完成: {method}")
    
    def feature_engineering(self, operations: Dict[str, Dict[str, Any]]) -> None:
        """
        特征工程
        
        Args:
            operations: 特征工程操作字典
        """
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("数据必须是DataFrame格式")
        
        for feature_name, operation in operations.items():
            op_type = operation.get('type')
            columns = operation.get('columns', [])
            
            if op_type == 'sum':
                self.data[feature_name] = self.data[columns].sum(axis=1)
            
            elif op_type == 'mean':
                self.data[feature_name] = self.data[columns].mean(axis=1)
            
            elif op_type == 'ratio':
                if len(columns) == 2:
                    self.data[feature_name] = self.data[columns[0]] / self.data[columns[1]]
            
            elif op_type == 'difference':
                if len(columns) == 2:
                    self.data[feature_name] = self.data[columns[0]] - self.data[columns[1]]
            
            elif op_type == 'product':
                self.data[feature_name] = self.data[columns].prod(axis=1)
            
            elif op_type == 'extract_date':
                date_col = columns[0]
                extract_type = operation.get('extract_type', 'year')
                if extract_type == 'year':
                    self.data[feature_name] = pd.to_datetime(self.data[date_col]).dt.year
                elif extract_type == 'month':
                    self.data[feature_name] = pd.to_datetime(self.data[date_col]).dt.month
                elif extract_type == 'day':
                    self.data[feature_name] = pd.to_datetime(self.data[date_col]).dt.day
                elif extract_type == 'weekday':
                    self.data[feature_name] = pd.to_datetime(self.data[date_col]).dt.weekday
            
            elif op_type == 'text_length':
                text_col = columns[0]
                self.data[feature_name] = self.data[text_col].astype(str).str.len()
            
            elif op_type == 'word_count':
                text_col = columns[0]
                self.data[feature_name] = self.data[text_col].astype(str).str.split().str.len()
            
            elif op_type == 'regex_extract':
                text_col = columns[0]
                pattern = operation.get('pattern', r'\d+')
                self.data[feature_name] = self.data[text_col].astype(str).str.extract(pattern)[0]
            
            logger.info(f"特征工程完成: {feature_name} ({op_type})")
    
    def sample_data(self, method: str = 'random', **kwargs) -> None:
        """
        数据采样
        
        Args:
            method: 采样方法 ('random', 'systematic', 'stratified')
            **kwargs: 采样参数
        """
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("数据必须是DataFrame格式")
        
        if method == 'random':
            sample_size = kwargs.get('sample_size', 1000)
            self.data = self.data.sample(n=min(sample_size, len(self.data)), random_state=42)
        
        elif method == 'systematic':
            step = kwargs.get('step', 10)
            self.data = self.data.iloc[::step]
        
        elif method == 'stratified':
            column = kwargs.get('column')
            sample_size = kwargs.get('sample_size', 1000)
            if column and column in self.data.columns:
                self.data = self.data.groupby(column, group_keys=False).apply(
                    lambda x: x.sample(min(len(x), sample_size // len(self.data[column].unique())))
                )
        
        logger.info(f"数据采样完成: {method}")
    
    def split_data(self, target_column: str, test_size: float = 0.2, 
                   validation_size: float = 0.1, random_state: int = 42) -> Dict[str, pd.DataFrame]:
        """
        数据分割
        
        Args:
            target_column: 目标列名
            test_size: 测试集比例
            validation_size: 验证集比例
            random_state: 随机种子
            
        Returns:
            分割后的数据集
        """
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("数据必须是DataFrame格式")
        
        if target_column not in self.data.columns:
            raise ValueError(f"目标列 {target_column} 不存在")
        
        # 分离特征和目标
        X = self.data.drop(columns=[target_column])
        y = self.data[target_column]
        
        # 分割训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y if len(y.unique()) < 10 else None
        )
        
        # 分割训练集和验证集
        if validation_size > 0:
            val_size = validation_size / (1 - test_size)
            X_train, X_val, y_train, y_val = train_test_split(
                X_train, y_train, test_size=val_size, random_state=random_state,
                stratify=y_train if len(y_train.unique()) < 10 else None
            )
        
        # 重建DataFrame
        train_data = pd.concat([X_train, y_train], axis=1)
        test_data = pd.concat([X_test, y_test], axis=1)
        
        result = {
            'train': train_data,
            'test': test_data
        }
        
        if validation_size > 0:
            val_data = pd.concat([X_val, y_val], axis=1)
            result['validation'] = val_data
        
        logger.info(f"数据分割完成: 训练集 {len(train_data)}, 测试集 {len(test_data)}")
        return result
    
    def get_data_info(self) -> Dict[str, Any]:
        """
        获取数据信息
        
        Returns:
            数据信息字典
        """
        if isinstance(self.data, pd.DataFrame):
            info = {
                'shape': self.data.shape,
                'columns': list(self.data.columns),
                'dtypes': self.data.dtypes.to_dict(),
                'missing_values': self.data.isnull().sum().to_dict(),
                'memory_usage': self.data.memory_usage(deep=True).sum(),
                'numeric_columns': list(self.data.select_dtypes(include=[np.number]).columns),
                'categorical_columns': list(self.data.select_dtypes(include=['object', 'category']).columns)
            }
        else:
            info = {
                'type': type(self.data).__name__,
                'length': len(self.data) if hasattr(self.data, '__len__') else None
            }
        
        return info


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='数据格式转换和预处理工具')
    parser.add_argument('input', help='输入数据文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--format', help='输出格式 (csv, json, xml, yaml, excel, parquet)')
    parser.add_argument('--encoding', nargs=2, metavar=('SOURCE', 'TARGET'), 
                       help='编码转换')
    parser.add_argument('--types', help='数据类型转换JSON文件路径')
    parser.add_argument('--normalize', choices=['standard', 'minmax', 'robust'], 
                       help='数据标准化')
    parser.add_argument('--encode', choices=['label', 'onehot', 'hash'], 
                       help='分类变量编码')
    parser.add_argument('--features', help='特征工程配置JSON文件路径')
    parser.add_argument('--sample', nargs=2, metavar=('METHOD', 'SIZE'), 
                       help='数据采样')
    parser.add_argument('--split', nargs=2, metavar=('TARGET', 'TEST_SIZE'), 
                       help='数据分割')
    parser.add_argument('--info', action='store_true', help='显示数据信息')
    
    args = parser.parse_args()
    
    try:
        # 创建转换器
        transformer = DataTransformer()
        
        # 加载数据
        transformer.load_data(args.input)
        
        # 显示数据信息
        if args.info:
            info = transformer.get_data_info()
            print("数据信息:")
            for key, value in info.items():
                print(f"  {key}: {value}")
        
        # 编码转换
        if args.encoding:
            transformer.convert_encoding(args.encoding[0], args.encoding[1])
        
        # 数据类型转换
        if args.types:
            with open(args.types, 'r', encoding='utf-8') as f:
                type_mapping = json.load(f)
            transformer.convert_data_types(type_mapping)
        
        # 数据标准化
        if args.normalize:
            transformer.normalize_data(args.normalize)
        
        # 分类变量编码
        if args.encode:
            transformer.encode_categorical(method=args.encode)
        
        # 特征工程
        if args.features:
            with open(args.features, 'r', encoding='utf-8') as f:
                operations = json.load(f)
            transformer.feature_engineering(operations)
        
        # 数据采样
        if args.sample:
            method, size = args.sample
            transformer.sample_data(method, sample_size=int(size))
        
        # 数据分割
        if args.split:
            target_col, test_size = args.split
            split_result = transformer.split_data(target_col, float(test_size))
            for name, data in split_result.items():
                output_file = f"{args.output or 'data'}_{name}.csv"
                data.to_csv(output_file, index=False)
                print(f"{name}集已保存到: {output_file}")
        
        # 保存数据
        if args.output:
            transformer.save_data(args.output, args.format)
        
    except Exception as e:
        logger.error(f"转换失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 