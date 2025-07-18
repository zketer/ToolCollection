#!/usr/bin/env python3
"""
CSV处理器 - 批量处理CSV文件工具

功能:
- 读取和写入CSV文件
- 数据清洗和转换
- 列重命名和删除
- 数据过滤和排序
- 合并多个CSV文件

作者: ToolCollection Team
版本: 1.0.0
"""

import pandas as pd
import argparse
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CSVProcessor:
    """CSV文件处理器类"""
    
    def __init__(self, input_file: str, output_file: Optional[str] = None):
        """
        初始化CSV处理器
        
        Args:
            input_file: 输入CSV文件路径
            output_file: 输出CSV文件路径，如果为None则自动生成
        """
        self.input_file = Path(input_file)
        self.output_file = Path(output_file) if output_file else self._generate_output_path()
        self.data = None
        
    def _generate_output_path(self) -> Path:
        """生成输出文件路径"""
        stem = self.input_file.stem
        return self.input_file.parent / f"{stem}_processed.csv"
    
    def load_data(self) -> pd.DataFrame:
        """
        加载CSV数据
        
        Returns:
            加载的DataFrame
        """
        try:
            logger.info(f"正在加载CSV文件: {self.input_file}")
            self.data = pd.read_csv(self.input_file)
            logger.info(f"成功加载数据，共 {len(self.data)} 行，{len(self.data.columns)} 列")
            return self.data
        except Exception as e:
            logger.error(f"加载CSV文件失败: {e}")
            raise
    
    def clean_data(self, remove_duplicates: bool = True, fill_na: bool = True) -> pd.DataFrame:
        """
        清洗数据
        
        Args:
            remove_duplicates: 是否删除重复行
            fill_na: 是否填充空值
            
        Returns:
            清洗后的DataFrame
        """
        if self.data is None:
            self.load_data()
            
        logger.info("开始数据清洗...")
        
        # 删除重复行
        if remove_duplicates:
            original_count = len(self.data)
            self.data = self.data.drop_duplicates()
            removed_count = original_count - len(self.data)
            logger.info(f"删除了 {removed_count} 行重复数据")
        
        # 填充空值
        if fill_na:
            self.data = self.data.fillna('')
            logger.info("已填充空值")
        
        return self.data
    
    def rename_columns(self, column_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        重命名列
        
        Args:
            column_mapping: 列名映射字典 {旧列名: 新列名}
            
        Returns:
            重命名后的DataFrame
        """
        if self.data is None:
            self.load_data()
            
        logger.info(f"重命名列: {column_mapping}")
        self.data = self.data.rename(columns=column_mapping)
        return self.data
    
    def filter_data(self, conditions: Dict[str, Any]) -> pd.DataFrame:
        """
        根据条件过滤数据
        
        Args:
            conditions: 过滤条件字典 {列名: 值}
            
        Returns:
            过滤后的DataFrame
        """
        if self.data is None:
            self.load_data()
            
        logger.info(f"应用过滤条件: {conditions}")
        
        for column, value in conditions.items():
            if column in self.data.columns:
                self.data = self.data[self.data[column] == value]
                logger.info(f"过滤列 '{column}' = '{value}'，剩余 {len(self.data)} 行")
        
        return self.data
    
    def sort_data(self, by: List[str], ascending: bool = True) -> pd.DataFrame:
        """
        排序数据
        
        Args:
            by: 排序的列名列表
            ascending: 是否升序排序
            
        Returns:
            排序后的DataFrame
        """
        if self.data is None:
            self.load_data()
            
        logger.info(f"按列排序: {by}, 升序: {ascending}")
        self.data = self.data.sort_values(by=by, ascending=ascending)
        return self.data
    
    def save_data(self, index: bool = False) -> None:
        """
        保存数据到CSV文件
        
        Args:
            index: 是否包含索引
        """
        if self.data is None:
            raise ValueError("没有数据可保存，请先加载或处理数据")
            
        try:
            logger.info(f"保存数据到: {self.output_file}")
            self.data.to_csv(self.output_file, index=index, encoding='utf-8')
            logger.info("数据保存成功")
        except Exception as e:
            logger.error(f"保存数据失败: {e}")
            raise
    
    def get_summary(self) -> Dict[str, Any]:
        """
        获取数据摘要信息
        
        Returns:
            数据摘要字典
        """
        if self.data is None:
            self.load_data()
            
        return {
            'rows': len(self.data),
            'columns': len(self.data.columns),
            'column_names': list(self.data.columns),
            'data_types': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict()
        }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='CSV文件处理器')
    parser.add_argument('input', help='输入CSV文件路径')
    parser.add_argument('-o', '--output', help='输出CSV文件路径')
    parser.add_argument('--clean', action='store_true', help='清洗数据（删除重复行，填充空值）')
    parser.add_argument('--sort', nargs='+', help='按指定列排序')
    parser.add_argument('--filter', nargs=2, action='append', 
                       metavar=('COLUMN', 'VALUE'), help='过滤条件：列名 值')
    parser.add_argument('--rename', nargs=2, action='append',
                       metavar=('OLD_NAME', 'NEW_NAME'), help='重命名列：旧列名 新列名')
    parser.add_argument('--summary', action='store_true', help='显示数据摘要')
    
    args = parser.parse_args()
    
    try:
        # 创建处理器
        processor = CSVProcessor(args.input, args.output)
        
        # 加载数据
        processor.load_data()
        
        # 应用各种操作
        if args.clean:
            processor.clean_data()
        
        if args.filter:
            filter_conditions = {col: val for col, val in args.filter}
            processor.filter_data(filter_conditions)
        
        if args.sort:
            processor.sort_data(args.sort)
        
        if args.rename:
            rename_mapping = {old: new for old, new in args.rename}
            processor.rename_columns(rename_mapping)
        
        # 显示摘要
        if args.summary:
            summary = processor.get_summary()
            print("\n=== 数据摘要 ===")
            print(f"行数: {summary['rows']}")
            print(f"列数: {summary['columns']}")
            print(f"列名: {summary['column_names']}")
            print(f"数据类型: {summary['data_types']}")
            print(f"缺失值: {summary['missing_values']}")
        
        # 保存数据
        processor.save_data()
        
        print(f"处理完成！输出文件: {processor.output_file}")
        
    except Exception as e:
        logger.error(f"处理失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 