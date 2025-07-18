#!/usr/bin/env python3
"""
文件监控器 - 监控文件变化并执行相应操作

功能:
- 监控文件和目录变化
- 支持多种事件类型（创建、修改、删除、移动）
- 自定义过滤规则
- 执行自定义命令
- 生成变化报告
- 支持递归监控

作者: ToolCollection Team
版本: 1.0.0
"""

import time
import os
import subprocess
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent, FileDeletedEvent, FileMovedEvent

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FileChangeHandler(FileSystemEventHandler):
    """文件变化处理器"""
    
    def __init__(self, patterns: Optional[List[str]] = None, 
                 ignore_patterns: Optional[List[str]] = None,
                 command: Optional[str] = None,
                 callback: Optional[Callable] = None):
        """
        初始化处理器
        
        Args:
            patterns: 匹配的文件模式
            ignore_patterns: 忽略的文件模式
            command: 执行的自定义命令
            callback: 自定义回调函数
        """
        self.patterns = patterns or ["*"]
        self.ignore_patterns = ignore_patterns or []
        self.command = command
        self.callback = callback
        self.events = []
    
    def should_process(self, file_path: str) -> bool:
        """
        判断是否应该处理该文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否处理
        """
        path = Path(file_path)
        
        # 检查忽略模式
        for pattern in self.ignore_patterns:
            if path.match(pattern):
                return False
        
        # 检查匹配模式
        for pattern in self.patterns:
            if path.match(pattern):
                return True
        
        return False
    
    def on_created(self, event):
        """文件创建事件"""
        if not event.is_directory and self.should_process(event.src_path):
            self._handle_event("created", event.src_path)
    
    def on_modified(self, event):
        """文件修改事件"""
        if not event.is_directory and self.should_process(event.src_path):
            self._handle_event("modified", event.src_path)
    
    def on_deleted(self, event):
        """文件删除事件"""
        if not event.is_directory and self.should_process(event.src_path):
            self._handle_event("deleted", event.src_path)
    
    def on_moved(self, event):
        """文件移动事件"""
        if not event.is_directory:
            if self.should_process(event.src_path):
                self._handle_event("moved_from", event.src_path)
            if self.should_process(event.dest_path):
                self._handle_event("moved_to", event.dest_path)
    
    def _handle_event(self, event_type: str, file_path: str):
        """
        处理文件事件
        
        Args:
            event_type: 事件类型
            file_path: 文件路径
        """
        timestamp = datetime.now()
        event_info = {
            'type': event_type,
            'file': file_path,
            'timestamp': timestamp,
            'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
        }
        
        self.events.append(event_info)
        
        # 记录事件
        logger.info(f"文件{event_type}: {file_path}")
        
        # 执行自定义命令
        if self.command:
            self._execute_command(event_info)
        
        # 执行自定义回调
        if self.callback:
            self.callback(event_info)
    
    def _execute_command(self, event_info: Dict[str, Any]):
        """
        执行自定义命令
        
        Args:
            event_info: 事件信息
        """
        try:
            # 替换命令中的占位符
            command = self.command.replace('{file}', event_info['file'])
            command = command.replace('{type}', event_info['type'])
            command = command.replace('{timestamp}', event_info['timestamp'].isoformat())
            
            # 执行命令
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"命令执行成功: {command}")
                if result.stdout:
                    logger.info(f"输出: {result.stdout}")
            else:
                logger.error(f"命令执行失败: {command}")
                if result.stderr:
                    logger.error(f"错误: {result.stderr}")
        
        except Exception as e:
            logger.error(f"执行命令异常: {e}")


class FileMonitor:
    """文件监控器类"""
    
    def __init__(self):
        """初始化文件监控器"""
        self.observer = Observer()
        self.handlers = []
        self.monitoring = False
    
    def add_watch(self, path: str, patterns: Optional[List[str]] = None,
                  ignore_patterns: Optional[List[str]] = None,
                  command: Optional[str] = None,
                  callback: Optional[Callable] = None,
                  recursive: bool = True) -> None:
        """
        添加监控路径
        
        Args:
            path: 监控路径
            patterns: 匹配的文件模式
            ignore_patterns: 忽略的文件模式
            command: 执行的自定义命令
            callback: 自定义回调函数
            recursive: 是否递归监控
        """
        if not os.path.exists(path):
            logger.error(f"路径不存在: {path}")
            return
        
        handler = FileChangeHandler(patterns, ignore_patterns, command, callback)
        self.handlers.append(handler)
        
        self.observer.schedule(handler, path, recursive=recursive)
        logger.info(f"添加监控路径: {path} (递归: {recursive})")
    
    def start_monitoring(self) -> None:
        """开始监控"""
        if not self.observer.schedules:
            logger.error("没有监控路径")
            return
        
        self.observer.start()
        self.monitoring = True
        logger.info("开始文件监控...")
    
    def stop_monitoring(self) -> None:
        """停止监控"""
        if self.monitoring:
            self.observer.stop()
            self.observer.join()
            self.monitoring = False
            logger.info("停止文件监控")
    
    def get_events_summary(self) -> Dict[str, Any]:
        """
        获取事件摘要
        
        Returns:
            事件摘要
        """
        all_events = []
        for handler in self.handlers:
            all_events.extend(handler.events)
        
        if not all_events:
            return {'total': 0, 'by_type': {}}
        
        # 按类型统计
        by_type = {}
        for event in all_events:
            event_type = event['type']
            by_type[event_type] = by_type.get(event_type, 0) + 1
        
        return {
            'total': len(all_events),
            'by_type': by_type,
            'events': all_events
        }
    
    def print_events_summary(self) -> None:
        """打印事件摘要"""
        summary = self.get_events_summary()
        
        print("\n" + "="*50)
        print("文件监控事件摘要")
        print("="*50)
        print(f"总事件数: {summary['total']}")
        
        if summary['by_type']:
            print("\n按类型统计:")
            for event_type, count in summary['by_type'].items():
                print(f"  {event_type}: {count}")
        
        if summary['events']:
            print("\n最近事件:")
            for event in summary['events'][-10:]:  # 显示最近10个事件
                print(f"  [{event['timestamp'].strftime('%H:%M:%S')}] "
                      f"{event['type']}: {event['file']}")
        
        print("="*50)
    
    def save_events_report(self, output_file: str) -> None:
        """
        保存事件报告
        
        Args:
            output_file: 输出文件路径
        """
        summary = self.get_events_summary()
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("文件监控事件报告\n")
                f.write("="*50 + "\n")
                f.write(f"生成时间: {datetime.now().isoformat()}\n")
                f.write(f"总事件数: {summary['total']}\n\n")
                
                if summary['by_type']:
                    f.write("按类型统计:\n")
                    for event_type, count in summary['by_type'].items():
                        f.write(f"  {event_type}: {count}\n")
                    f.write("\n")
                
                if summary['events']:
                    f.write("详细事件列表:\n")
                    for event in summary['events']:
                        f.write(f"[{event['timestamp'].isoformat()}] "
                               f"{event['type']}: {event['file']}\n")
            
            logger.info(f"事件报告已保存到: {output_file}")
        except Exception as e:
            logger.error(f"保存事件报告失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='文件变化监控工具')
    parser.add_argument('path', help='要监控的路径')
    parser.add_argument('-p', '--patterns', nargs='+', help='匹配的文件模式')
    parser.add_argument('-i', '--ignore', nargs='+', help='忽略的文件模式')
    parser.add_argument('-c', '--command', help='文件变化时执行的命令')
    parser.add_argument('-r', '--recursive', action='store_true', default=True, 
                       help='递归监控子目录')
    parser.add_argument('-d', '--duration', type=int, help='监控持续时间（秒）')
    parser.add_argument('-o', '--output', help='事件报告输出文件')
    parser.add_argument('--summary', action='store_true', help='显示事件摘要')
    
    args = parser.parse_args()
    
    try:
        # 创建监控器
        monitor = FileMonitor()
        
        # 添加监控路径
        monitor.add_watch(
            args.path,
            patterns=args.patterns,
            ignore_patterns=args.ignore,
            command=args.command,
            recursive=args.recursive
        )
        
        # 开始监控
        monitor.start_monitoring()
        
        try:
            if args.duration:
                # 定时监控
                time.sleep(args.duration)
            else:
                # 持续监控
                while True:
                    time.sleep(1)
        
        except KeyboardInterrupt:
            logger.info("用户中断监控")
        
        finally:
            # 停止监控
            monitor.stop_monitoring()
            
            # 显示摘要
            if args.summary:
                monitor.print_events_summary()
            
            # 保存报告
            if args.output:
                monitor.save_events_report(args.output)
        
    except Exception as e:
        logger.error(f"监控失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 