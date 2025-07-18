#!/usr/bin/env python3
"""
JSON处理器 - JSON数据处理和转换工具

功能:
- JSON文件验证和格式化
- JSON数据转换（美化、压缩）
- JSON路径查询和提取
- JSON数据合并和比较
- 支持多种输出格式

作者: ToolCollection Team
版本: 1.0.0
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class JSONProcessor:
    """JSON处理器类"""
    
    def __init__(self, input_file: Optional[str] = None):
        """
        初始化JSON处理器
        
        Args:
            input_file: 输入JSON文件路径
        """
        self.input_file = Path(input_file) if input_file else None
        self.data = None
    
    def load_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        从文件加载JSON数据
        
        Args:
            file_path: JSON文件路径
            
        Returns:
            加载的JSON数据
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            logger.info(f"成功加载JSON文件: {file_path}")
            return self.data
        except Exception as e:
            logger.error(f"加载JSON文件失败: {e}")
            raise
    
    def load_from_string(self, json_string: str) -> Dict[str, Any]:
        """
        从字符串加载JSON数据
        
        Args:
            json_string: JSON字符串
            
        Returns:
            加载的JSON数据
        """
        try:
            self.data = json.loads(json_string)
            logger.info("成功解析JSON字符串")
            return self.data
        except Exception as e:
            logger.error(f"解析JSON字符串失败: {e}")
            raise
    
    def validate_json(self, data: Optional[Dict[str, Any]] = None) -> bool:
        """
        验证JSON数据
        
        Args:
            data: 要验证的数据，如果为None则使用已加载的数据
            
        Returns:
            验证结果
        """
        if data is None:
            data = self.data
        
        if data is None:
            logger.error("没有数据可验证")
            return False
        
        try:
            # 尝试重新序列化来验证
            json.dumps(data)
            logger.info("JSON数据验证通过")
            return True
        except Exception as e:
            logger.error(f"JSON数据验证失败: {e}")
            return False
    
    def format_json(self, data: Optional[Dict[str, Any]] = None, 
                   indent: int = 2, sort_keys: bool = False) -> str:
        """
        格式化JSON数据
        
        Args:
            data: 要格式化的数据
            indent: 缩进空格数
            sort_keys: 是否排序键
            
        Returns:
            格式化后的JSON字符串
        """
        if data is None:
            data = self.data
        
        if data is None:
            raise ValueError("没有数据可格式化")
        
        return json.dumps(data, ensure_ascii=False, indent=indent, sort_keys=sort_keys)
    
    def minify_json(self, data: Optional[Dict[str, Any]] = None) -> str:
        """
        压缩JSON数据
        
        Args:
            data: 要压缩的数据
            
        Returns:
            压缩后的JSON字符串
        """
        if data is None:
            data = self.data
        
        if data is None:
            raise ValueError("没有数据可压缩")
        
        return json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    
    def get_value_by_path(self, path: str, data: Optional[Dict[str, Any]] = None) -> Any:
        """
        根据路径获取JSON值
        
        Args:
            path: 路径，如 "user.name" 或 "items[0].title"
            data: 要查询的数据
            
        Returns:
            找到的值
        """
        if data is None:
            data = self.data
        
        if data is None:
            raise ValueError("没有数据可查询")
        
        try:
            # 解析路径
            keys = []
            current = ""
            in_bracket = False
            
            for char in path:
                if char == '.' and not in_bracket:
                    if current:
                        keys.append(current)
                        current = ""
                elif char == '[':
                    if current:
                        keys.append(current)
                        current = ""
                    in_bracket = True
                elif char == ']' and in_bracket:
                    keys.append(int(current))
                    current = ""
                    in_bracket = False
                else:
                    current += char
            
            if current:
                keys.append(current)
            
            # 遍历路径
            result = data
            for key in keys:
                if isinstance(result, dict):
                    result = result[key]
                elif isinstance(result, list) and isinstance(key, int):
                    result = result[key]
                else:
                    raise KeyError(f"无法访问路径: {path}")
            
            return result
        except Exception as e:
            logger.error(f"路径查询失败 {path}: {e}")
            raise
    
    def find_keys(self, search_key: str, data: Optional[Dict[str, Any]] = None, 
                  path: str = "") -> List[str]:
        """
        查找包含指定键的所有路径
        
        Args:
            search_key: 要搜索的键名
            data: 要搜索的数据
            path: 当前路径
            
        Returns:
            找到的路径列表
        """
        if data is None:
            data = self.data
        
        if data is None:
            return []
        
        found_paths = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                
                if key == search_key:
                    found_paths.append(current_path)
                
                # 递归搜索
                found_paths.extend(self.find_keys(search_key, value, current_path))
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{path}[{i}]"
                found_paths.extend(self.find_keys(search_key, item, current_path))
        
        return found_paths
    
    def merge_json(self, other_data: Dict[str, Any], 
                   strategy: str = "replace") -> Dict[str, Any]:
        """
        合并JSON数据
        
        Args:
            other_data: 要合并的数据
            strategy: 合并策略 ("replace", "deep", "append")
            
        Returns:
            合并后的数据
        """
        if self.data is None:
            self.data = other_data
            return self.data
        
        if strategy == "replace":
            # 简单替换
            self.data.update(other_data)
        elif strategy == "deep":
            # 深度合并
            self.data = self._deep_merge(self.data, other_data)
        elif strategy == "append":
            # 追加到列表
            if isinstance(self.data, list):
                if isinstance(other_data, list):
                    self.data.extend(other_data)
                else:
                    self.data.append(other_data)
            else:
                logger.warning("当前数据不是列表，无法追加")
        
        return self.data
    
    def _deep_merge(self, dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
        """深度合并两个字典"""
        result = dict1.copy()
        
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def compare_json(self, other_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        比较两个JSON数据
        
        Args:
            other_data: 要比较的数据
            
        Returns:
            比较结果
        """
        if self.data is None:
            raise ValueError("没有基准数据可比较")
        
        result = {
            'added': [],
            'removed': [],
            'modified': [],
            'unchanged': []
        }
        
        self._compare_dicts(self.data, other_data, "", result)
        
        return result
    
    def _compare_dicts(self, dict1: Dict[str, Any], dict2: Dict[str, Any], 
                      path: str, result: Dict[str, List[str]]):
        """递归比较字典"""
        all_keys = set(dict1.keys()) | set(dict2.keys())
        
        for key in all_keys:
            current_path = f"{path}.{key}" if path else key
            
            if key not in dict1:
                result['added'].append(current_path)
            elif key not in dict2:
                result['removed'].append(current_path)
            elif dict1[key] != dict2[key]:
                if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                    self._compare_dicts(dict1[key], dict2[key], current_path, result)
                else:
                    result['modified'].append(current_path)
            else:
                result['unchanged'].append(current_path)
    
    def save_to_file(self, output_file: str, data: Optional[Dict[str, Any]] = None,
                    indent: int = 2, sort_keys: bool = False) -> None:
        """
        保存JSON数据到文件
        
        Args:
            output_file: 输出文件路径
            data: 要保存的数据
            indent: 缩进空格数
            sort_keys: 是否排序键
        """
        if data is None:
            data = self.data
        
        if data is None:
            raise ValueError("没有数据可保存")
        
        try:
            formatted_json = self.format_json(data, indent, sort_keys)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(formatted_json)
            logger.info(f"JSON数据已保存到: {output_file}")
        except Exception as e:
            logger.error(f"保存JSON文件失败: {e}")
            raise
    
    def get_summary(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        获取JSON数据摘要
        
        Args:
            data: 要分析的数据
            
        Returns:
            数据摘要
        """
        if data is None:
            data = self.data
        
        if data is None:
            return {}
        
        def analyze_structure(obj, path=""):
            if isinstance(obj, dict):
                return {
                    'type': 'object',
                    'keys': list(obj.keys()),
                    'count': len(obj),
                    'children': {k: analyze_structure(v, f"{path}.{k}" if path else k) 
                               for k, v in obj.items()}
                }
            elif isinstance(obj, list):
                return {
                    'type': 'array',
                    'count': len(obj),
                    'children': [analyze_structure(item, f"{path}[{i}]") 
                               for i, item in enumerate(obj[:5])]  # 只分析前5个
                }
            else:
                return {
                    'type': type(obj).__name__,
                    'value': str(obj)[:50]  # 限制长度
                }
        
        return {
            'structure': analyze_structure(data),
            'size_bytes': len(json.dumps(data, ensure_ascii=False)),
            'depth': self._get_max_depth(data)
        }
    
    def _get_max_depth(self, obj, current_depth=0):
        """获取JSON的最大深度"""
        if isinstance(obj, dict):
            return max([self._get_max_depth(v, current_depth + 1) for v in obj.values()], 
                      default=current_depth)
        elif isinstance(obj, list):
            return max([self._get_max_depth(item, current_depth + 1) for item in obj], 
                      default=current_depth)
        else:
            return current_depth


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='JSON数据处理和转换工具')
    parser.add_argument('input', nargs='?', help='输入JSON文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--format', action='store_true', help='格式化JSON')
    parser.add_argument('--minify', action='store_true', help='压缩JSON')
    parser.add_argument('--indent', type=int, default=2, help='缩进空格数')
    parser.add_argument('--sort-keys', action='store_true', help='排序键')
    parser.add_argument('--validate', action='store_true', help='验证JSON')
    parser.add_argument('--summary', action='store_true', help='显示数据摘要')
    parser.add_argument('--path', help='获取指定路径的值')
    parser.add_argument('--find-key', help='查找包含指定键的路径')
    parser.add_argument('--merge', help='合并的JSON文件路径')
    parser.add_argument('--merge-strategy', choices=['replace', 'deep', 'append'], 
                       default='replace', help='合并策略')
    parser.add_argument('--compare', help='比较的JSON文件路径')
    
    args = parser.parse_args()
    
    try:
        # 创建处理器
        processor = JSONProcessor()
        
        # 加载数据
        if args.input:
            processor.load_from_file(args.input)
        else:
            # 从标准输入读取
            json_string = sys.stdin.read()
            processor.load_from_string(json_string)
        
        # 验证数据
        if args.validate:
            if not processor.validate_json():
                sys.exit(1)
        
        # 获取路径值
        if args.path:
            value = processor.get_value_by_path(args.path)
            print(json.dumps(value, ensure_ascii=False, indent=2))
            return
        
        # 查找键
        if args.find_key:
            paths = processor.find_keys(args.find_key)
            if paths:
                print("找到的路径:")
                for path in paths:
                    print(f"  {path}")
            else:
                print(f"未找到键: {args.find_key}")
            return
        
        # 合并数据
        if args.merge:
            with open(args.merge, 'r', encoding='utf-8') as f:
                other_data = json.load(f)
            processor.merge_json(other_data, args.merge_strategy)
        
        # 比较数据
        if args.compare:
            with open(args.compare, 'r', encoding='utf-8') as f:
                other_data = json.load(f)
            result = processor.compare_json(other_data)
            print("比较结果:")
            for category, items in result.items():
                if items:
                    print(f"\n{category}:")
                    for item in items:
                        print(f"  {item}")
            return
        
        # 显示摘要
        if args.summary:
            summary = processor.get_summary()
            print("JSON数据摘要:")
            print(f"大小: {summary['size_bytes']} 字节")
            print(f"最大深度: {summary['depth']}")
            print(f"结构类型: {summary['structure']['type']}")
            if summary['structure']['type'] == 'object':
                print(f"键数量: {summary['structure']['count']}")
                print(f"键列表: {', '.join(summary['structure']['keys'][:10])}")
            elif summary['structure']['type'] == 'array':
                print(f"元素数量: {summary['structure']['count']}")
            return
        
        # 格式化或压缩
        if args.minify:
            result = processor.minify_json()
        else:
            result = processor.format_json(indent=args.indent, sort_keys=args.sort_keys)
        
        # 输出结果
        if args.output:
            processor.save_to_file(args.output, indent=args.indent, sort_keys=args.sort_keys)
        else:
            print(result)
        
    except Exception as e:
        logger.error(f"处理失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 