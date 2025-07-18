#!/usr/bin/env python3
"""
批量重命名器 - 批量重命名文件和文件夹工具

功能:
- 根据模式批量重命名文件
- 支持正则表达式匹配
- 支持序号重命名
- 支持大小写转换
- 支持添加前缀/后缀
- 预览重命名结果

作者: ToolCollection Team
版本: 1.0.0
"""

import os
import re
import argparse
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BatchRenamer:
    """批量重命名器类"""
    
    def __init__(self, directory: str):
        """
        初始化批量重命名器
        
        Args:
            directory: 要处理的目录路径
        """
        self.directory = Path(directory)
        if not self.directory.exists():
            raise ValueError(f"目录不存在: {directory}")
        if not self.directory.is_dir():
            raise ValueError(f"路径不是目录: {directory}")
    
    def get_files(self, pattern: str = "*", recursive: bool = False) -> List[Path]:
        """
        获取匹配模式的文件列表
        
        Args:
            pattern: 文件匹配模式，支持通配符
            recursive: 是否递归搜索子目录
            
        Returns:
            匹配的文件路径列表
        """
        files = []
        if recursive:
            search_pattern = f"**/{pattern}"
            files = list(self.directory.glob(search_pattern))
        else:
            files = list(self.directory.glob(pattern))
        
        # 过滤掉目录，只保留文件
        files = [f for f in files if f.is_file()]
        logger.info(f"找到 {len(files)} 个匹配的文件")
        return files
    
    def preview_rename(self, files: List[Path], new_name_pattern: str, 
                      start_number: int = 1, case: str = "lower") -> List[Tuple[Path, Path]]:
        """
        预览重命名结果
        
        Args:
            files: 文件列表
            new_name_pattern: 新文件名模式，支持 {n} 表示序号，{name} 表示原文件名
            start_number: 起始序号
            case: 大小写转换 ("lower", "upper", "title", "none")
            
        Returns:
            原路径和新路径的元组列表
        """
        rename_plans = []
        
        for i, file_path in enumerate(files):
            # 生成新文件名
            new_name = new_name_pattern.format(
                n=start_number + i,
                name=file_path.stem,
                ext=file_path.suffix
            )
            
            # 应用大小写转换
            if case == "lower":
                new_name = new_name.lower()
            elif case == "upper":
                new_name = new_name.upper()
            elif case == "title":
                new_name = new_name.title()
            
            new_path = file_path.parent / new_name
            rename_plans.append((file_path, new_path))
        
        return rename_plans
    
    def rename_with_regex(self, files: List[Path], pattern: str, replacement: str) -> List[Tuple[Path, Path]]:
        """
        使用正则表达式重命名
        
        Args:
            files: 文件列表
            pattern: 正则表达式模式
            replacement: 替换字符串
            
        Returns:
            原路径和新路径的元组列表
        """
        rename_plans = []
        regex = re.compile(pattern)
        
        for file_path in files:
            new_name = regex.sub(replacement, file_path.name)
            new_path = file_path.parent / new_name
            rename_plans.append((file_path, new_path))
        
        return rename_plans
    
    def add_prefix_suffix(self, files: List[Path], prefix: str = "", suffix: str = "") -> List[Tuple[Path, Path]]:
        """
        添加前缀和后缀
        
        Args:
            files: 文件列表
            prefix: 前缀
            suffix: 后缀（不包含扩展名）
            
        Returns:
            原路径和新路径的元组列表
        """
        rename_plans = []
        
        for file_path in files:
            new_name = f"{prefix}{file_path.stem}{suffix}{file_path.suffix}"
            new_path = file_path.parent / new_name
            rename_plans.append((file_path, new_path))
        
        return rename_plans
    
    def execute_rename(self, rename_plans: List[Tuple[Path, Path]], dry_run: bool = True) -> None:
        """
        执行重命名操作
        
        Args:
            rename_plans: 重命名计划列表
            dry_run: 是否为预览模式（不实际重命名）
        """
        if dry_run:
            logger.info("=== 预览重命名结果 ===")
            for old_path, new_path in rename_plans:
                print(f"  {old_path.name} -> {new_path.name}")
            return
        
        logger.info("开始执行重命名...")
        success_count = 0
        
        for old_path, new_path in rename_plans:
            try:
                # 检查新文件名是否已存在
                if new_path.exists():
                    logger.warning(f"目标文件已存在，跳过: {new_path}")
                    continue
                
                old_path.rename(new_path)
                logger.info(f"重命名成功: {old_path.name} -> {new_path.name}")
                success_count += 1
                
            except Exception as e:
                logger.error(f"重命名失败 {old_path}: {e}")
        
        logger.info(f"重命名完成，成功 {success_count}/{len(rename_plans)} 个文件")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='批量重命名文件和文件夹')
    parser.add_argument('directory', help='要处理的目录路径')
    parser.add_argument('-p', '--pattern', default='*', help='文件匹配模式（默认: *）')
    parser.add_argument('-r', '--recursive', action='store_true', help='递归搜索子目录')
    parser.add_argument('--preview', action='store_true', help='预览重命名结果')
    
    # 重命名模式选择
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--pattern-rename', metavar=('PATTERN', 'REPLACEMENT'), 
                           nargs=2, help='使用正则表达式重命名')
    mode_group.add_argument('--name-pattern', metavar='PATTERN', 
                           help='使用模式重命名，支持 {n}（序号）、{name}（原文件名）、{ext}（扩展名）')
    mode_group.add_argument('--prefix', help='添加前缀')
    mode_group.add_argument('--suffix', help='添加后缀（不包含扩展名）')
    
    # 其他选项
    parser.add_argument('--start-number', type=int, default=1, help='起始序号（默认: 1）')
    parser.add_argument('--case', choices=['lower', 'upper', 'title', 'none'], 
                       default='none', help='大小写转换（默认: none）')
    parser.add_argument('--execute', action='store_true', help='执行重命名（默认只预览）')
    
    args = parser.parse_args()
    
    try:
        # 创建重命名器
        renamer = BatchRenamer(args.directory)
        
        # 获取文件列表
        files = renamer.get_files(args.pattern, args.recursive)
        if not files:
            logger.warning("没有找到匹配的文件")
            return
        
        # 生成重命名计划
        rename_plans = []
        
        if args.pattern_rename:
            pattern, replacement = args.pattern_rename
            rename_plans = renamer.rename_with_regex(files, pattern, replacement)
        elif args.name_pattern:
            rename_plans = renamer.preview_rename(files, args.name_pattern, 
                                                args.start_number, args.case)
        elif args.prefix or args.suffix:
            rename_plans = renamer.add_prefix_suffix(files, args.prefix or "", args.suffix or "")
        else:
            logger.error("请指定重命名模式")
            sys.exit(1)
        
        # 执行或预览重命名
        dry_run = not args.execute
        renamer.execute_rename(rename_plans, dry_run)
        
        if dry_run and not args.preview:
            print("\n使用 --execute 参数执行实际重命名操作")
        
    except Exception as e:
        logger.error(f"操作失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 