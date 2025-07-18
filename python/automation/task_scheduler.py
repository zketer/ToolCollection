#!/usr/bin/env python3
"""
任务调度器 - 定时任务调度、管理工具

功能:
- 支持多种调度策略 (定时、间隔、条件触发)
- 任务依赖关系管理
- 任务执行状态监控
- 失败重试机制
- 任务日志记录

作者: ToolCollection
版本: 1.0.0
"""

import argparse
import json
import os
import sys
import time
import threading
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
import schedule


class Task:
    """任务类"""
    
    def __init__(self, name: str, command: str, schedule_type: str = 'interval', 
                 schedule_value: Any = None, retry_count: int = 3, 
                 retry_delay: int = 60, enabled: bool = True):
        """
        初始化任务
        
        Args:
            name: 任务名称
            command: 要执行的命令
            schedule_type: 调度类型 ('interval', 'daily', 'weekly', 'cron')
            schedule_value: 调度值
            retry_count: 重试次数
            retry_delay: 重试延迟 (秒)
            enabled: 是否启用
        """
        self.name = name
        self.command = command
        self.schedule_type = schedule_type
        self.schedule_value = schedule_value
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.enabled = enabled
        
        # 执行状态
        self.last_run = None
        self.next_run = None
        self.run_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.last_status = None
        self.last_error = None
        
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'name': self.name,
            'command': self.command,
            'schedule_type': self.schedule_type,
            'schedule_value': self.schedule_value,
            'retry_count': self.retry_count,
            'retry_delay': self.retry_delay,
            'enabled': self.enabled,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None,
            'run_count': self.run_count,
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'last_status': self.last_status,
            'last_error': self.last_error
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """从字典创建任务"""
        task = cls(
            name=data['name'],
            command=data['command'],
            schedule_type=data['schedule_type'],
            schedule_value=data['schedule_value'],
            retry_count=data.get('retry_count', 3),
            retry_delay=data.get('retry_delay', 60),
            enabled=data.get('enabled', True)
        )
        
        # 恢复状态
        if data.get('last_run'):
            task.last_run = datetime.fromisoformat(data['last_run'])
        if data.get('next_run'):
            task.next_run = datetime.fromisoformat(data['next_run'])
        task.run_count = data.get('run_count', 0)
        task.success_count = data.get('success_count', 0)
        task.failure_count = data.get('failure_count', 0)
        task.last_status = data.get('last_status')
        task.last_error = data.get('last_error')
        
        return task


class TaskScheduler:
    """任务调度器类"""
    
    def __init__(self, config_file: str = 'tasks.json'):
        """
        初始化任务调度器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.tasks: Dict[str, Task] = {}
        self.running = False
        self.scheduler_thread = None
        
        # 加载现有任务
        self.load_tasks()
    
    def add_task(self, task: Task) -> bool:
        """添加任务"""
        if task.name in self.tasks:
            print(f"⚠️  任务 '{task.name}' 已存在，将被覆盖")
        
        self.tasks[task.name] = task
        self.schedule_task(task)
        print(f"✅ 任务 '{task.name}' 已添加")
        return True
    
    def remove_task(self, task_name: str) -> bool:
        """删除任务"""
        if task_name not in self.tasks:
            print(f"❌ 任务 '{task_name}' 不存在")
            return False
        
        # 取消调度
        schedule.clear(task_name)
        del self.tasks[task_name]
        print(f"✅ 任务 '{task_name}' 已删除")
        return True
    
    def enable_task(self, task_name: str) -> bool:
        """启用任务"""
        if task_name not in self.tasks:
            print(f"❌ 任务 '{task_name}' 不存在")
            return False
        
        task = self.tasks[task_name]
        task.enabled = True
        self.schedule_task(task)
        print(f"✅ 任务 '{task_name}' 已启用")
        return True
    
    def disable_task(self, task_name: str) -> bool:
        """禁用任务"""
        if task_name not in self.tasks:
            print(f"❌ 任务 '{task_name}' 不存在")
            return False
        
        task = self.tasks[task_name]
        task.enabled = False
        schedule.clear(task_name)
        print(f"✅ 任务 '{task_name}' 已禁用")
        return True
    
    def schedule_task(self, task: Task):
        """调度任务"""
        if not task.enabled:
            return
        
        # 清除现有调度
        schedule.clear(task.name)
        
        # 根据调度类型设置调度
        if task.schedule_type == 'interval':
            # 间隔执行
            schedule.every(task.schedule_value).seconds.do(
                self.execute_task, task.name
            ).tag(task.name)
            
        elif task.schedule_type == 'daily':
            # 每日执行
            schedule.every().day.at(task.schedule_value).do(
                self.execute_task, task.name
            ).tag(task.name)
            
        elif task.schedule_type == 'weekly':
            # 每周执行
            day, time_str = task.schedule_value.split(' ')
            getattr(schedule.every(), day).at(time_str).do(
                self.execute_task, task.name
            ).tag(task.name)
            
        elif task.schedule_type == 'cron':
            # Cron表达式 (简化版)
            minute, hour, day, month, weekday = task.schedule_value.split()
            schedule.every().day.at(f"{hour}:{minute}").do(
                self.execute_task, task.name
            ).tag(task.name)
        
        # 更新下次运行时间
        task.next_run = self.get_next_run_time(task)
    
    def get_next_run_time(self, task: Task) -> Optional[datetime]:
        """获取下次运行时间"""
        try:
            if task.schedule_type == 'interval':
                return datetime.now() + timedelta(seconds=task.schedule_value)
            elif task.schedule_type == 'daily':
                # 简化的下次运行时间计算
                return datetime.now().replace(
                    hour=int(task.schedule_value.split(':')[0]),
                    minute=int(task.schedule_value.split(':')[1]),
                    second=0, microsecond=0
                )
            else:
                return None
        except:
            return None
    
    def execute_task(self, task_name: str):
        """执行任务"""
        if task_name not in self.tasks:
            print(f"❌ 任务 '{task_name}' 不存在")
            return
        
        task = self.tasks[task_name]
        if not task.enabled:
            return
        
        print(f"🚀 执行任务: {task_name}")
        print(f"   命令: {task.command}")
        
        task.last_run = datetime.now()
        task.run_count += 1
        
        # 执行命令
        success = False
        error_msg = None
        
        for attempt in range(task.retry_count + 1):
            try:
                if attempt > 0:
                    print(f"   重试 {attempt}/{task.retry_count}...")
                    time.sleep(task.retry_delay)
                
                # 执行命令
                result = subprocess.run(
                    task.command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5分钟超时
                )
                
                if result.returncode == 0:
                    success = True
                    task.last_status = 'success'
                    task.success_count += 1
                    print(f"✅ 任务 '{task_name}' 执行成功")
                    if result.stdout.strip():
                        print(f"   输出: {result.stdout.strip()}")
                    break
                else:
                    error_msg = f"命令返回非零退出码: {result.returncode}"
                    if result.stderr.strip():
                        error_msg += f"\n错误: {result.stderr.strip()}"
                    
            except subprocess.TimeoutExpired:
                error_msg = "命令执行超时"
            except Exception as e:
                error_msg = f"执行失败: {str(e)}"
        
        if not success:
            task.last_status = 'failed'
            task.failure_count += 1
            task.last_error = error_msg
            print(f"❌ 任务 '{task_name}' 执行失败: {error_msg}")
        
        # 更新下次运行时间
        task.next_run = self.get_next_run_time(task)
    
    def run_task_now(self, task_name: str) -> bool:
        """立即运行任务"""
        if task_name not in self.tasks:
            print(f"❌ 任务 '{task_name}' 不存在")
            return False
        
        print(f"⚡ 立即执行任务: {task_name}")
        self.execute_task(task_name)
        return True
    
    def list_tasks(self, show_details: bool = False):
        """列出所有任务"""
        if not self.tasks:
            print("📋 没有配置的任务")
            return
        
        print(f"📋 任务列表 ({len(self.tasks)} 个):")
        for task in self.tasks.values():
            status = "✅ 启用" if task.enabled else "❌ 禁用"
            print(f"\n🔹 {task.name} ({status})")
            print(f"   命令: {task.command}")
            print(f"   调度: {task.schedule_type} - {task.schedule_value}")
            print(f"   运行次数: {task.run_count} (成功: {task.success_count}, 失败: {task.failure_count})")
            
            if task.last_run:
                print(f"   上次运行: {task.last_run.strftime('%Y-%m-%d %H:%M:%S')}")
            if task.next_run:
                print(f"   下次运行: {task.next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if show_details and task.last_error:
                print(f"   最后错误: {task.last_error}")
    
    def start_scheduler(self):
        """启动调度器"""
        if self.running:
            print("⚠️  调度器已在运行")
            return
        
        print("🚀 启动任务调度器...")
        self.running = True
        
        # 启动调度器线程
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        
        print("✅ 调度器已启动")
        print("💡 按 Ctrl+C 停止调度器")
    
    def stop_scheduler(self):
        """停止调度器"""
        if not self.running:
            print("⚠️  调度器未运行")
            return
        
        print("🛑 停止任务调度器...")
        self.running = False
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        print("✅ 调度器已停止")
    
    def _scheduler_loop(self):
        """调度器主循环"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                print(f"❌ 调度器错误: {e}")
                time.sleep(5)
    
    def load_tasks(self):
        """从文件加载任务"""
        if not os.path.exists(self.config_file):
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for task_data in data.get('tasks', []):
                task = Task.from_dict(task_data)
                self.tasks[task.name] = task
                self.schedule_task(task)
            
            print(f"📥 从 {self.config_file} 加载了 {len(self.tasks)} 个任务")
            
        except Exception as e:
            print(f"❌ 加载任务失败: {e}")
    
    def save_tasks(self):
        """保存任务到文件"""
        try:
            data = {
                'tasks': [task.to_dict() for task in self.tasks.values()],
                'last_saved': datetime.now().isoformat()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 任务已保存到 {self.config_file}")
            
        except Exception as e:
            print(f"❌ 保存任务失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="任务调度器 - 定时任务调度、管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 添加间隔任务
  python task_scheduler.py --add "backup" "python backup.py" --interval 3600
  
  # 添加每日任务
  python task_scheduler.py --add "daily_report" "python report.py" --daily "09:00"
  
  # 添加每周任务
  python task_scheduler.py --add "weekly_cleanup" "python cleanup.py" --weekly "monday 02:00"
  
  # 列出任务
  python task_scheduler.py --list
  
  # 立即执行任务
  python task_scheduler.py --run "backup"
  
  # 启动调度器
  python task_scheduler.py --start
  
  # 从配置文件加载
  python task_scheduler.py --config tasks.json --start
        """
    )
    
    parser.add_argument('--config', default='tasks.json', help='配置文件路径')
    
    # 任务管理
    parser.add_argument('--add', nargs=2, metavar=('NAME', 'COMMAND'), help='添加任务')
    parser.add_argument('--remove', help='删除任务')
    parser.add_argument('--enable', help='启用任务')
    parser.add_argument('--disable', help='禁用任务')
    parser.add_argument('--run', help='立即运行任务')
    parser.add_argument('--list', action='store_true', help='列出所有任务')
    parser.add_argument('--details', action='store_true', help='显示详细信息')
    
    # 调度选项
    parser.add_argument('--interval', type=int, help='间隔执行 (秒)')
    parser.add_argument('--daily', help='每日执行 (HH:MM)')
    parser.add_argument('--weekly', help='每周执行 (day HH:MM)')
    parser.add_argument('--cron', help='Cron表达式 (minute hour day month weekday)')
    
    # 重试选项
    parser.add_argument('--retry', type=int, default=3, help='重试次数 (默认: 3)')
    parser.add_argument('--retry-delay', type=int, default=60, help='重试延迟 (默认: 60秒)')
    
    # 调度器控制
    parser.add_argument('--start', action='store_true', help='启动调度器')
    parser.add_argument('--stop', action='store_true', help='停止调度器')
    parser.add_argument('--save', action='store_true', help='保存任务配置')
    
    args = parser.parse_args()
    
    # 创建调度器
    scheduler = TaskScheduler(args.config)
    
    try:
        if args.add:
            # 添加任务
            name, command = args.add
            
            # 确定调度类型
            schedule_type = 'interval'
            schedule_value = 3600  # 默认1小时
            
            if args.interval:
                schedule_type = 'interval'
                schedule_value = args.interval
            elif args.daily:
                schedule_type = 'daily'
                schedule_value = args.daily
            elif args.weekly:
                schedule_type = 'weekly'
                schedule_value = args.weekly
            elif args.cron:
                schedule_type = 'cron'
                schedule_value = args.cron
            
            task = Task(
                name=name,
                command=command,
                schedule_type=schedule_type,
                schedule_value=schedule_value,
                retry_count=args.retry,
                retry_delay=args.retry_delay
            )
            
            scheduler.add_task(task)
            scheduler.save_tasks()
        
        elif args.remove:
            # 删除任务
            scheduler.remove_task(args.remove)
            scheduler.save_tasks()
        
        elif args.enable:
            # 启用任务
            scheduler.enable_task(args.enable)
            scheduler.save_tasks()
        
        elif args.disable:
            # 禁用任务
            scheduler.disable_task(args.disable)
            scheduler.save_tasks()
        
        elif args.run:
            # 立即运行任务
            scheduler.run_task_now(args.run)
        
        elif args.list:
            # 列出任务
            scheduler.list_tasks(args.details)
        
        elif args.start:
            # 启动调度器
            scheduler.start_scheduler()
            
            try:
                # 保持运行
                while scheduler.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                scheduler.stop_scheduler()
        
        elif args.stop:
            # 停止调度器
            scheduler.stop_scheduler()
        
        elif args.save:
            # 保存配置
            scheduler.save_tasks()
        
        else:
            print("💡 使用 --help 查看使用说明")
    
    except KeyboardInterrupt:
        print("\n⚠️  操作被用户中断")
        scheduler.stop_scheduler()
        sys.exit(1)
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 