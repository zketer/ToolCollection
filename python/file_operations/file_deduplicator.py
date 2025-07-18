#!/usr/bin/env python3
"""
文件去重器 - 检测和删除重复文件工具

功能:
- 基于文件内容检测重复文件
- 支持多种哈希算法 (MD5, SHA1, SHA256)
- 智能文件大小预过滤
- 批量删除重复文件
- 生成重复文件报告

作者: ToolCollection
版本: 1.0.0
"""

import argparse
import hashlib
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple
import time


class FileDeduplicator:
    """文件去重器类"""
    
    def __init__(self, hash_algorithm: str = 'md5', chunk_size: int = 8192):
        """
        初始化文件去重器
        
        Args:
            hash_algorithm: 哈希算法 ('md5', 'sha1', 'sha256')
            chunk_size: 读取文件块大小
        """
        self.hash_algorithm = hash_algorithm.lower()
        self.chunk_size = chunk_size
        self.hash_func = getattr(hashlib, self.hash_algorithm)
        
    def calculate_file_hash(self, file_path: str) -> str:
        """计算文件哈希值"""
        try:
            hash_obj = self.hash_func()
            with open(file_path, 'rb') as f:
                while chunk := f.read(self.chunk_size):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except Exception as e:
            print(f"❌ 计算文件哈希失败 {file_path}: {e}")
            return None
    
    def scan_directory(self, directory: str, extensions: List[str] = None, 
                      min_size: int = 0, max_size: int = None) -> Dict[str, List[str]]:
        """
        扫描目录，按文件大小分组
        
        Args:
            directory: 扫描目录
            extensions: 文件扩展名过滤
            min_size: 最小文件大小 (字节)
            max_size: 最大文件大小 (字节)
            
        Returns:
            按文件大小分组的文件路径字典
        """
        size_groups = defaultdict(list)
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # 检查文件扩展名
                    if extensions:
                        file_ext = os.path.splitext(file)[1].lower()
                        if file_ext not in extensions:
                            continue
                    
                    # 获取文件大小
                    try:
                        file_size = os.path.getsize(file_path)
                    except OSError:
                        continue
                    
                    # 检查文件大小范围
                    if file_size < min_size:
                        continue
                    if max_size and file_size > max_size:
                        continue
                    
                    size_groups[file_size].append(file_path)
            
            return size_groups
            
        except Exception as e:
            print(f"❌ 扫描目录失败: {e}")
            return {}
    
    def find_duplicates(self, directory: str, extensions: List[str] = None,
                       min_size: int = 0, max_size: int = None) -> Dict[str, List[str]]:
        """
        查找重复文件
        
        Args:
            directory: 扫描目录
            extensions: 文件扩展名过滤
            min_size: 最小文件大小 (字节)
            max_size: 最大文件大小 (字节)
            
        Returns:
            按哈希值分组的重复文件字典
        """
        print(f"🔍 扫描目录: {directory}")
        size_groups = self.scan_directory(directory, extensions, min_size, max_size)
        
        if not size_groups:
            print("❌ 未找到符合条件的文件")
            return {}
        
        print(f"📊 找到 {sum(len(files) for files in size_groups.values())} 个文件")
        
        # 按大小分组，只处理有多个文件的组
        duplicate_candidates = {size: files for size, files in size_groups.items() 
                              if len(files) > 1}
        
        if not duplicate_candidates:
            print("✅ 未发现重复文件")
            return {}
        
        print(f"🔍 检查 {len(duplicate_candidates)} 个大小组中的重复文件...")
        
        # 计算哈希值并分组
        hash_groups = defaultdict(list)
        total_files = sum(len(files) for files in duplicate_candidates.values())
        processed = 0
        
        for size, files in duplicate_candidates.items():
            for file_path in files:
                processed += 1
                if processed % 100 == 0:
                    print(f"  进度: {processed}/{total_files}")
                
                file_hash = self.calculate_file_hash(file_path)
                if file_hash:
                    hash_groups[file_hash].append(file_path)
        
        # 只返回有重复的组
        duplicates = {hash_val: files for hash_val, files in hash_groups.items() 
                     if len(files) > 1}
        
        return duplicates
    
    def delete_duplicates(self, duplicates: Dict[str, List[str]], 
                         keep_strategy: str = 'oldest', dry_run: bool = True) -> Dict[str, List[str]]:
        """
        删除重复文件
        
        Args:
            duplicates: 重复文件字典
            keep_strategy: 保留策略 ('oldest', 'newest', 'smallest_path')
            dry_run: 是否只预览，不实际删除
            
        Returns:
            已删除的文件列表
        """
        deleted_files = []
        
        for hash_val, files in duplicates.items():
            if len(files) <= 1:
                continue
            
            # 根据策略选择要保留的文件
            if keep_strategy == 'oldest':
                files.sort(key=lambda x: os.path.getctime(x))
                keep_file = files[0]
            elif keep_strategy == 'newest':
                files.sort(key=lambda x: os.path.getctime(x))
                keep_file = files[-1]
            elif keep_strategy == 'smallest_path':
                keep_file = min(files, key=lambda x: len(x))
            else:
                keep_file = files[0]
            
            # 删除其他文件
            for file_path in files:
                if file_path != keep_file:
                    if not dry_run:
                        try:
                            os.remove(file_path)
                            deleted_files.append(file_path)
                            print(f"🗑️  已删除: {file_path}")
                        except Exception as e:
                            print(f"❌ 删除失败 {file_path}: {e}")
                    else:
                        deleted_files.append(file_path)
                        print(f"🗑️  将删除: {file_path}")
            
            if not dry_run:
                print(f"✅ 保留: {keep_file}")
        
        return deleted_files
    
    def generate_report(self, duplicates: Dict[str, List[str]], 
                       output_file: str = None) -> Dict:
        """生成重复文件报告"""
        report = {
            'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'hash_algorithm': self.hash_algorithm,
            'total_duplicate_groups': len(duplicates),
            'total_duplicate_files': sum(len(files) for files in duplicates.values()),
            'potential_space_saved': 0,
            'duplicate_groups': []
        }
        
        for hash_val, files in duplicates.items():
            file_size = os.path.getsize(files[0])
            space_saved = file_size * (len(files) - 1)
            report['potential_space_saved'] += space_saved
            
            group_info = {
                'hash': hash_val,
                'file_count': len(files),
                'file_size': file_size,
                'space_saved': space_saved,
                'files': files
            }
            report['duplicate_groups'].append(group_info)
        
        # 按节省空间排序
        report['duplicate_groups'].sort(key=lambda x: x['space_saved'], reverse=True)
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                print(f"📄 报告已保存到: {output_file}")
            except Exception as e:
                print(f"❌ 保存报告失败: {e}")
        
        return report
    
    def print_summary(self, duplicates: Dict[str, List[str]]):
        """打印重复文件摘要"""
        if not duplicates:
            print("✅ 未发现重复文件")
            return
        
        total_groups = len(duplicates)
        total_files = sum(len(files) for files in duplicates.values())
        total_size = sum(os.path.getsize(files[0]) * (len(files) - 1) 
                        for files in duplicates.values())
        
        print(f"\n📊 重复文件摘要:")
        print(f"  重复组数: {total_groups}")
        print(f"  重复文件数: {total_files}")
        print(f"  可节省空间: {self.format_size(total_size)}")
        
        # 显示前5个最大的重复组
        sorted_groups = sorted(duplicates.items(), 
                             key=lambda x: os.path.getsize(x[1][0]) * (len(x[1]) - 1),
                             reverse=True)
        
        print(f"\n🔝 前5个最大的重复组:")
        for i, (hash_val, files) in enumerate(sorted_groups[:5], 1):
            file_size = os.path.getsize(files[0])
            space_saved = file_size * (len(files) - 1)
            print(f"  {i}. {len(files)} 个文件, 每组 {self.format_size(file_size)}, "
                  f"可节省 {self.format_size(space_saved)}")
            for file_path in files[:3]:
                print(f"     - {file_path}")
            if len(files) > 3:
                print(f"     ... 还有 {len(files) - 3} 个文件")
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="文件去重器 - 检测和删除重复文件工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 扫描目录，查找重复文件
  python file_deduplicator.py /path/to/directory --scan
  
  # 查找特定类型的重复文件
  python file_deduplicator.py /path/to/directory --scan --extensions .jpg .png .mp4
  
  # 删除重复文件 (保留最旧的)
  python file_deduplicator.py /path/to/directory --delete --keep oldest
  
  # 预览删除操作
  python file_deduplicator.py /path/to/directory --delete --dry-run
  
  # 生成详细报告
  python file_deduplicator.py /path/to/directory --scan --report report.json
        """
    )
    
    parser.add_argument('directory', help='要扫描的目录路径')
    parser.add_argument('--scan', action='store_true', help='扫描重复文件')
    parser.add_argument('--delete', action='store_true', help='删除重复文件')
    parser.add_argument('--dry-run', action='store_true', help='预览模式，不实际删除')
    parser.add_argument('--report', help='生成报告文件路径')
    
    # 扫描选项
    parser.add_argument('--extensions', nargs='+', help='文件扩展名过滤 (如 .jpg .png)')
    parser.add_argument('--min-size', type=int, default=0, help='最小文件大小 (字节)')
    parser.add_argument('--max-size', type=int, help='最大文件大小 (字节)')
    parser.add_argument('--hash', choices=['md5', 'sha1', 'sha256'], 
                       default='md5', help='哈希算法')
    
    # 删除选项
    parser.add_argument('--keep', choices=['oldest', 'newest', 'smallest_path'], 
                       default='oldest', help='保留策略')
    parser.add_argument('--chunk-size', type=int, default=8192, help='读取文件块大小')
    
    args = parser.parse_args()
    
    # 检查目录是否存在
    if not os.path.exists(args.directory):
        print(f"❌ 目录不存在: {args.directory}")
        sys.exit(1)
    
    # 创建去重器
    deduplicator = FileDeduplicator(args.hash, args.chunk_size)
    
    # 处理文件扩展名
    extensions = None
    if args.extensions:
        extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' 
                     for ext in args.extensions]
    
    try:
        if args.scan or args.delete:
            # 查找重复文件
            duplicates = deduplicator.find_duplicates(
                args.directory, extensions, args.min_size, args.max_size
            )
            
            if duplicates:
                # 打印摘要
                deduplicator.print_summary(duplicates)
                
                # 生成报告
                if args.report:
                    deduplicator.generate_report(duplicates, args.report)
                
                # 删除重复文件
                if args.delete:
                    print(f"\n🗑️  开始删除重复文件 (保留策略: {args.keep})")
                    if args.dry_run:
                        print("🔍 预览模式 - 不会实际删除文件")
                    
                    deleted_files = deduplicator.delete_duplicates(
                        duplicates, args.keep, args.dry_run
                    )
                    
                    if args.dry_run:
                        print(f"\n📊 预览结果: 将删除 {len(deleted_files)} 个重复文件")
                    else:
                        print(f"\n✅ 删除完成: 已删除 {len(deleted_files)} 个重复文件")
            else:
                print("✅ 未发现重复文件")
        
        else:
            print("💡 使用 --help 查看使用说明")
    
    except KeyboardInterrupt:
        print("\n⚠️  操作被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 