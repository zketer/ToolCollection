#!/usr/bin/env python3
"""
文件同步器 - 文件和目录同步工具

功能:
- 双向文件同步
- 增量同步
- 冲突检测和解决
- 同步日志记录
- 多种同步策略

作者: ToolCollection Team
版本: 1.0.0
"""

import os
import shutil
import hashlib
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
import logging
from datetime import datetime
import json
import time

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FileSync:
    """文件同步器类"""
    
    def __init__(self, source: str, target: str, mode: str = "one_way"):
        """
        初始化文件同步器
        
        Args:
            source: 源目录路径
            target: 目标目录路径
            mode: 同步模式 (one_way, two_way, mirror)
        """
        self.source = Path(source)
        self.target = Path(target)
        self.mode = mode
        self.sync_log = []
        self.conflicts = []
        
        # 确保目录存在
        self.source.mkdir(parents=True, exist_ok=True)
        self.target.mkdir(parents=True, exist_ok=True)
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """计算文件哈希值"""
        if not file_path.exists():
            return ""
        
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"计算文件哈希失败 {file_path}: {e}")
            return ""
    
    def get_file_info(self, file_path: Path) -> Optional[Dict]:
        """获取文件信息"""
        if not file_path.exists():
            return None
        
        try:
            stat = file_path.stat()
            return {
                'path': file_path,
                'size': stat.st_size,
                'mtime': stat.st_mtime,
                'hash': self.calculate_file_hash(file_path)
            }
        except Exception as e:
            logger.error(f"获取文件信息失败 {file_path}: {e}")
            return None
    
    def scan_directory(self, directory: Path) -> Dict[str, Dict]:
        """扫描目录"""
        files = {}
        
        try:
            for item in directory.rglob("*"):
                if item.is_file():
                    relative_path = item.relative_to(directory)
                    file_info = self.get_file_info(item)
                    if file_info:
                        files[str(relative_path)] = file_info
        except Exception as e:
            logger.error(f"扫描目录失败 {directory}: {e}")
        
        return files
    
    def detect_changes(self) -> Tuple[Dict, Dict, Set]:
        """检测变化"""
        source_files = self.scan_directory(self.source)
        target_files = self.scan_directory(self.target)
        
        all_files = set(source_files.keys()) | set(target_files.keys())
        
        new_files = {}
        modified_files = {}
        deleted_files = set()
        
        for file_path in all_files:
            source_info = source_files.get(file_path)
            target_info = target_files.get(file_path)
            
            if source_info and not target_info:
                new_files[file_path] = source_info
            elif not source_info and target_info:
                if self.mode == "one_way":
                    deleted_files.add(file_path)
                else:
                    new_files[file_path] = target_info
            elif source_info and target_info:
                if (source_info['size'] != target_info['size'] or 
                    abs(source_info['mtime'] - target_info['mtime']) > 1 or
                    source_info['hash'] != target_info['hash']):
                    modified_files[file_path] = (source_info, target_info)
        
        return new_files, modified_files, deleted_files
    
    def sync_files(self, dry_run: bool = False) -> Dict[str, Any]:
        """同步文件"""
        logger.info(f"开始文件同步: {self.source} -> {self.target} (模式: {self.mode})")
        
        new_files, modified_files, deleted_files = self.detect_changes()
        
        stats = {
            'new_files': len(new_files),
            'modified_files': len(modified_files),
            'deleted_files': len(deleted_files),
            'conflicts': len(self.conflicts)
        }
        
        if dry_run:
            logger.info("预览模式 - 不会实际执行同步操作")
            self._print_sync_preview(new_files, modified_files, deleted_files)
            return stats
        
        start_time = time.time()
        
        # 复制新文件
        for file_path, file_info in new_files.items():
            source_path = self.source / file_path
            target_path = self.target / file_path
            
            if file_info['path'] == source_path:
                success = self._copy_file(source_path, target_path)
            else:
                success = self._copy_file(target_path, source_path)
            
            if success:
                self.sync_log.append({
                    'action': 'copy',
                    'file': file_path,
                    'timestamp': datetime.now().isoformat()
                })
        
        # 处理修改的文件
        for file_path, (source_info, target_info) in modified_files.items():
            source_path = self.source / file_path
            target_path = self.target / file_path
            
            if source_info['mtime'] > target_info['mtime']:
                success = self._copy_file(source_path, target_path)
            else:
                success = self._copy_file(target_path, source_path)
            
            if success:
                self.sync_log.append({
                    'action': 'update',
                    'file': file_path,
                    'timestamp': datetime.now().isoformat()
                })
        
        # 删除文件
        for file_path in deleted_files:
            target_path = self.target / file_path
            success = self._delete_file(target_path)
            
            if success:
                self.sync_log.append({
                    'action': 'delete',
                    'file': file_path,
                    'timestamp': datetime.now().isoformat()
                })
        
        end_time = time.time()
        stats['sync_time'] = end_time - start_time
        
        logger.info(f"同步完成: 新增 {stats['new_files']} 个文件, "
                   f"修改 {stats['modified_files']} 个文件, "
                   f"删除 {stats['deleted_files']} 个文件")
        
        return stats
    
    def _copy_file(self, source_path: Path, target_path: Path) -> bool:
        """复制文件"""
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)
            logger.info(f"文件复制成功: {source_path} -> {target_path}")
            return True
        except Exception as e:
            logger.error(f"文件复制失败: {source_path} -> {target_path}: {e}")
            return False
    
    def _delete_file(self, file_path: Path) -> bool:
        """删除文件"""
        try:
            file_path.unlink()
            logger.info(f"文件删除成功: {file_path}")
            return True
        except Exception as e:
            logger.error(f"文件删除失败: {file_path}: {e}")
            return False
    
    def _print_sync_preview(self, new_files: Dict, modified_files: Dict, deleted_files: Set) -> None:
        """打印同步预览"""
        print("\n=== 同步预览 ===")
        
        if new_files:
            print(f"\n新增文件 ({len(new_files)}):")
            for file_path in new_files.keys():
                print(f"  + {file_path}")
        
        if modified_files:
            print(f"\n修改文件 ({len(modified_files)}):")
            for file_path in modified_files.keys():
                print(f"  ~ {file_path}")
        
        if deleted_files:
            print(f"\n删除文件 ({len(deleted_files)}):")
            for file_path in deleted_files:
                print(f"  - {file_path}")
    
    def save_sync_log(self, log_file: str) -> None:
        """保存同步日志"""
        log_data = {
            'sync_info': {
                'source': str(self.source),
                'target': str(self.target),
                'mode': self.mode,
                'timestamp': datetime.now().isoformat()
            },
            'sync_log': self.sync_log,
            'conflicts': self.conflicts
        }
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)
            logger.info(f"同步日志已保存到: {log_file}")
        except Exception as e:
            logger.error(f"保存同步日志失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='文件和目录同步工具')
    parser.add_argument('source', help='源目录路径')
    parser.add_argument('target', help='目标目录路径')
    parser.add_argument('--mode', choices=['one_way', 'two_way', 'mirror'], 
                       default='one_way', help='同步模式')
    parser.add_argument('--dry-run', action='store_true', help='预览模式')
    parser.add_argument('--log', help='同步日志文件路径')
    
    args = parser.parse_args()
    
    try:
        syncer = FileSync(args.source, args.target, args.mode)
        stats = syncer.sync_files(args.dry_run)
        
        if args.log:
            syncer.save_sync_log(args.log)
        
        print(f"\n同步统计:")
        print(f"  新增文件: {stats['new_files']}")
        print(f"  修改文件: {stats['modified_files']}")
        print(f"  删除文件: {stats['deleted_files']}")
        if 'sync_time' in stats:
            print(f"  同步耗时: {stats['sync_time']:.2f} 秒")
        
    except Exception as e:
        logger.error(f"同步失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 