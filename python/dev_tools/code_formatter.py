#!/usr/bin/env python3
"""
代码格式化器 - 自动格式化Python代码

功能:
- 使用Black格式化Python代码
- 使用Flake8检查代码风格
- 批量处理文件和目录
- 支持递归处理
- 生成格式化报告
- 支持配置文件

作者: ToolCollection Team
版本: 1.0.0
"""

import subprocess
import sys
import argparse
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
import json
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CodeFormatter:
    """代码格式化器类"""
    
    def __init__(self):
        """初始化代码格式化器"""
        self.results = {
            'formatted_files': [],
            'checked_files': [],
            'errors': [],
            'warnings': []
        }
    
    def check_black_installed(self) -> bool:
        """检查Black是否已安装"""
        try:
            subprocess.run(['black', '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def check_flake8_installed(self) -> bool:
        """检查Flake8是否已安装"""
        try:
            subprocess.run(['flake8', '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def format_with_black(self, file_path: str, check_only: bool = False) -> Dict[str, Any]:
        """
        使用Black格式化文件
        
        Args:
            file_path: 文件路径
            check_only: 是否只检查不修改
            
        Returns:
            格式化结果
        """
        result = {
            'file': file_path,
            'formatted': False,
            'error': None
        }
        
        try:
            cmd = ['black']
            if check_only:
                cmd.append('--check')
            cmd.append(file_path)
            
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            if process.returncode == 0:
                if check_only:
                    result['formatted'] = True
                    logger.info(f"✓ {file_path} 格式正确")
                else:
                    result['formatted'] = True
                    logger.info(f"✓ {file_path} 格式化完成")
            else:
                if check_only:
                    result['error'] = "需要格式化"
                    logger.warning(f"⚠ {file_path} 需要格式化")
                else:
                    result['error'] = process.stderr
                    logger.error(f"✗ {file_path} 格式化失败: {process.stderr}")
        
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"✗ {file_path} 格式化异常: {e}")
        
        return result
    
    def check_with_flake8(self, file_path: str) -> Dict[str, Any]:
        """
        使用Flake8检查代码风格
        
        Args:
            file_path: 文件路径
            
        Returns:
            检查结果
        """
        result = {
            'file': file_path,
            'issues': [],
            'error': None
        }
        
        try:
            cmd = ['flake8', '--format=json', file_path]
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            if process.returncode == 0:
                logger.info(f"✓ {file_path} 代码风格检查通过")
            else:
                try:
                    # 解析JSON输出
                    issues = json.loads(process.stdout)
                    result['issues'] = issues
                    logger.warning(f"⚠ {file_path} 发现 {len(issues)} 个代码风格问题")
                except json.JSONDecodeError:
                    result['error'] = process.stdout
                    logger.error(f"✗ {file_path} 解析检查结果失败")
        
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"✗ {file_path} 代码风格检查异常: {e}")
        
        return result
    
    def find_python_files(self, path: str, recursive: bool = False) -> List[str]:
        """
        查找Python文件
        
        Args:
            path: 路径
            recursive: 是否递归搜索
            
        Returns:
            Python文件列表
        """
        python_files = []
        path_obj = Path(path)
        
        if path_obj.is_file():
            if path_obj.suffix == '.py':
                python_files.append(str(path_obj))
        elif path_obj.is_dir():
            if recursive:
                pattern = '**/*.py'
            else:
                pattern = '*.py'
            
            python_files = [str(f) for f in path_obj.glob(pattern) if f.is_file()]
        
        return python_files
    
    def format_directory(self, directory: str, recursive: bool = False, 
                        check_only: bool = False, run_flake8: bool = False) -> Dict[str, Any]:
        """
        格式化目录中的Python文件
        
        Args:
            directory: 目录路径
            recursive: 是否递归处理
            check_only: 是否只检查不修改
            run_flake8: 是否运行Flake8检查
            
        Returns:
            处理结果
        """
        python_files = self.find_python_files(directory, recursive)
        
        if not python_files:
            logger.warning(f"在 {directory} 中没有找到Python文件")
            return self.results
        
        logger.info(f"找到 {len(python_files)} 个Python文件")
        
        for file_path in python_files:
            # 使用Black格式化
            black_result = self.format_with_black(file_path, check_only)
            if black_result['formatted']:
                self.results['formatted_files'].append(file_path)
            elif black_result['error']:
                self.results['errors'].append({
                    'file': file_path,
                    'type': 'black',
                    'error': black_result['error']
                })
            
            # 使用Flake8检查
            if run_flake8:
                flake8_result = self.check_with_flake8(file_path)
                self.results['checked_files'].append(file_path)
                if flake8_result['issues']:
                    self.results['warnings'].append({
                        'file': file_path,
                        'type': 'flake8',
                        'issues': flake8_result['issues']
                    })
                elif flake8_result['error']:
                    self.results['errors'].append({
                        'file': file_path,
                        'type': 'flake8',
                        'error': flake8_result['error']
                    })
        
        return self.results
    
    def print_summary(self) -> None:
        """打印处理摘要"""
        print("\n" + "="*60)
        print("代码格式化摘要")
        print("="*60)
        
        print(f"格式化文件数: {len(self.results['formatted_files'])}")
        print(f"检查文件数: {len(self.results['checked_files'])}")
        print(f"错误数: {len(self.results['errors'])}")
        print(f"警告数: {len(self.results['warnings'])}")
        
        if self.results['formatted_files']:
            print(f"\n已格式化的文件:")
            for file_path in self.results['formatted_files']:
                print(f"  ✓ {file_path}")
        
        if self.results['errors']:
            print(f"\n错误:")
            for error in self.results['errors']:
                print(f"  ✗ {error['file']} ({error['type']}): {error['error']}")
        
        if self.results['warnings']:
            print(f"\n警告:")
            for warning in self.results['warnings']:
                print(f"  ⚠ {warning['file']} ({warning['type']}): {len(warning['issues'])} 个问题")
        
        print("="*60)
    
    def save_report(self, output_file: str) -> None:
        """保存处理报告"""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'formatted_files_count': len(self.results['formatted_files']),
                    'checked_files_count': len(self.results['checked_files']),
                    'errors_count': len(self.results['errors']),
                    'warnings_count': len(self.results['warnings'])
                },
                'results': self.results
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            logger.info(f"处理报告已保存到: {output_file}")
        except Exception as e:
            logger.error(f"保存报告失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Python代码格式化工具')
    parser.add_argument('path', help='要处理的文件或目录路径')
    parser.add_argument('-r', '--recursive', action='store_true', help='递归处理子目录')
    parser.add_argument('--check', action='store_true', help='只检查不修改（Black）')
    parser.add_argument('--flake8', action='store_true', help='运行Flake8代码风格检查')
    parser.add_argument('-o', '--output', help='输出报告文件路径')
    parser.add_argument('--black-only', action='store_true', help='只运行Black格式化')
    parser.add_argument('--flake8-only', action='store_true', help='只运行Flake8检查')
    
    args = parser.parse_args()
    
    try:
        # 创建格式化器
        formatter = CodeFormatter()
        
        # 检查工具是否安装
        if not args.flake8_only:
            if not formatter.check_black_installed():
                logger.error("Black未安装，请运行: pip install black")
                sys.exit(1)
        
        if not args.black_only and (args.flake8 or args.flake8_only):
            if not formatter.check_flake8_installed():
                logger.error("Flake8未安装，请运行: pip install flake8")
                sys.exit(1)
        
        # 确定要运行的工具
        run_black = not args.flake8_only
        run_flake8 = args.flake8 or args.flake8_only
        
        # 处理文件或目录
        if os.path.isfile(args.path):
            # 处理单个文件
            if run_black:
                black_result = formatter.format_with_black(args.path, args.check)
                if black_result['formatted']:
                    formatter.results['formatted_files'].append(args.path)
            
            if run_flake8:
                flake8_result = formatter.check_with_flake8(args.path)
                formatter.results['checked_files'].append(args.path)
                if flake8_result['issues']:
                    formatter.results['warnings'].append({
                        'file': args.path,
                        'type': 'flake8',
                        'issues': flake8_result['issues']
                    })
        else:
            # 处理目录
            formatter.format_directory(
                args.path, 
                recursive=args.recursive,
                check_only=args.check,
                run_flake8=run_flake8
            )
        
        # 打印摘要
        formatter.print_summary()
        
        # 保存报告
        if args.output:
            formatter.save_report(args.output)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"code_format_report_{timestamp}.json"
            formatter.save_report(report_file)
        
    except Exception as e:
        logger.error(f"处理失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 