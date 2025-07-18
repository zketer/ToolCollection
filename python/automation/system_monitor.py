#!/usr/bin/env python3
"""
系统监控器 - 监控系统资源使用情况

功能:
- 监控CPU使用率
- 监控内存使用情况
- 监控磁盘使用情况
- 监控网络连接
- 生成监控报告
- 支持实时监控和定时监控

作者: ToolCollection Team
版本: 1.0.0
"""

import psutil
import time
import json
import csv
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SystemMonitor:
    """系统监控器类"""
    
    def __init__(self):
        """初始化系统监控器"""
        self.monitoring = False
        self.data_points = []
    
    def get_cpu_info(self) -> Dict[str, Any]:
        """获取CPU信息"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            return {
                'usage_percent': cpu_percent,
                'count': cpu_count,
                'frequency_mhz': cpu_freq.current if cpu_freq else None,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"获取CPU信息失败: {e}")
            return {}
    
    def get_memory_info(self) -> Dict[str, Any]:
        """获取内存信息"""
        try:
            memory = psutil.virtual_memory()
            
            return {
                'total_gb': round(memory.total / (1024**3), 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'used_gb': round(memory.used / (1024**3), 2),
                'usage_percent': memory.percent,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"获取内存信息失败: {e}")
            return {}
    
    def get_disk_info(self) -> Dict[str, Any]:
        """获取磁盘信息"""
        try:
            disk = psutil.disk_usage('/')
            
            return {
                'total_gb': round(disk.total / (1024**3), 2),
                'used_gb': round(disk.used / (1024**3), 2),
                'free_gb': round(disk.free / (1024**3), 2),
                'usage_percent': round((disk.used / disk.total) * 100, 2),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"获取磁盘信息失败: {e}")
            return {}
    
    def get_network_info(self) -> Dict[str, Any]:
        """获取网络信息"""
        try:
            network = psutil.net_io_counters()
            
            return {
                'bytes_sent_mb': round(network.bytes_sent / (1024**2), 2),
                'bytes_recv_mb': round(network.bytes_recv / (1024**2), 2),
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"获取网络信息失败: {e}")
            return {}
    
    def get_process_info(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """获取进程信息"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu_percent': proc.info['cpu_percent'],
                        'memory_percent': proc.info['memory_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # 按CPU使用率排序
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            return processes[:top_n]
        except Exception as e:
            logger.error(f"获取进程信息失败: {e}")
            return []
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统基本信息"""
        try:
            return {
                'platform': psutil.sys.platform,
                'python_version': psutil.sys.version,
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"获取系统信息失败: {e}")
            return {}
    
    def collect_data(self) -> Dict[str, Any]:
        """收集所有系统数据"""
        data = {
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'disk': self.get_disk_info(),
            'network': self.get_network_info(),
            'processes': self.get_process_info(),
            'system': self.get_system_info()
        }
        
        self.data_points.append(data)
        return data
    
    def print_summary(self, data: Dict[str, Any]) -> None:
        """打印系统摘要"""
        print("\n" + "="*50)
        print("系统监控摘要")
        print("="*50)
        
        # CPU信息
        if data.get('cpu'):
            cpu = data['cpu']
            print(f"CPU使用率: {cpu.get('usage_percent', 0):.1f}%")
            print(f"CPU核心数: {cpu.get('count', 0)}")
            if cpu.get('frequency_mhz'):
                print(f"CPU频率: {cpu['frequency_mhz']:.0f} MHz")
        
        # 内存信息
        if data.get('memory'):
            mem = data['memory']
            print(f"内存使用率: {mem.get('usage_percent', 0):.1f}%")
            print(f"内存总量: {mem.get('total_gb', 0):.1f} GB")
            print(f"可用内存: {mem.get('available_gb', 0):.1f} GB")
        
        # 磁盘信息
        if data.get('disk'):
            disk = data['disk']
            print(f"磁盘使用率: {disk.get('usage_percent', 0):.1f}%")
            print(f"磁盘总量: {disk.get('total_gb', 0):.1f} GB")
            print(f"可用空间: {disk.get('free_gb', 0):.1f} GB")
        
        # 网络信息
        if data.get('network'):
            net = data['network']
            print(f"发送数据: {net.get('bytes_sent_mb', 0):.1f} MB")
            print(f"接收数据: {net.get('bytes_recv_mb', 0):.1f} MB")
        
        # 进程信息
        if data.get('processes'):
            print(f"\n前5个高CPU进程:")
            for i, proc in enumerate(data['processes'][:5]):
                print(f"  {i+1}. {proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu_percent']:.1f}%")
        
        print("="*50)
    
    def save_to_json(self, output_file: str) -> None:
        """保存数据为JSON格式"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.data_points, f, ensure_ascii=False, indent=2)
            logger.info(f"监控数据已保存到: {output_file}")
        except Exception as e:
            logger.error(f"保存JSON文件失败: {e}")
    
    def save_to_csv(self, output_file: str) -> None:
        """保存数据为CSV格式"""
        if not self.data_points:
            logger.warning("没有数据可保存")
            return
        
        try:
            # 准备CSV数据
            csv_data = []
            for data_point in self.data_points:
                row = {
                    'timestamp': data_point.get('system', {}).get('timestamp', ''),
                    'cpu_usage': data_point.get('cpu', {}).get('usage_percent', 0),
                    'memory_usage': data_point.get('memory', {}).get('usage_percent', 0),
                    'disk_usage': data_point.get('disk', {}).get('usage_percent', 0),
                    'network_sent_mb': data_point.get('network', {}).get('bytes_sent_mb', 0),
                    'network_recv_mb': data_point.get('network', {}).get('bytes_recv_mb', 0)
                }
                csv_data.append(row)
            
            # 写入CSV文件
            fieldnames = ['timestamp', 'cpu_usage', 'memory_usage', 'disk_usage', 
                         'network_sent_mb', 'network_recv_mb']
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
            
            logger.info(f"监控数据已保存到: {output_file}")
        except Exception as e:
            logger.error(f"保存CSV文件失败: {e}")
    
    def start_monitoring(self, interval: int = 5, duration: Optional[int] = None, 
                        output_file: Optional[str] = None) -> None:
        """
        开始监控
        
        Args:
            interval: 监控间隔（秒）
            duration: 监控持续时间（秒），None表示无限监控
            output_file: 输出文件路径
        """
        self.monitoring = True
        start_time = time.time()
        
        logger.info(f"开始系统监控，间隔: {interval}秒")
        if duration:
            logger.info(f"监控持续时间: {duration}秒")
        
        try:
            while self.monitoring:
                # 收集数据
                data = self.collect_data()
                
                # 打印摘要
                self.print_summary(data)
                
                # 检查是否超时
                if duration and (time.time() - start_time) >= duration:
                    logger.info("监控时间已到，停止监控")
                    break
                
                # 等待下次监控
                if self.monitoring:
                    time.sleep(interval)
        
        except KeyboardInterrupt:
            logger.info("用户中断监控")
        
        finally:
            self.monitoring = False
            
            # 保存数据
            if output_file and self.data_points:
                if output_file.endswith('.csv'):
                    self.save_to_csv(output_file)
                else:
                    self.save_to_json(output_file)
            
            logger.info("监控已停止")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='系统资源监控工具')
    parser.add_argument('-i', '--interval', type=int, default=5, help='监控间隔（秒，默认: 5）')
    parser.add_argument('-d', '--duration', type=int, help='监控持续时间（秒）')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-f', '--format', choices=['json', 'csv'], default='json', 
                       help='输出格式（默认: json）')
    parser.add_argument('--once', action='store_true', help='只监控一次')
    
    args = parser.parse_args()
    
    try:
        # 创建监控器
        monitor = SystemMonitor()
        
        # 确定输出文件
        if args.output:
            output_file = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"system_monitor_{timestamp}.{args.format}"
        
        if args.once:
            # 只监控一次
            data = monitor.collect_data()
            monitor.print_summary(data)
            
            if output_file:
                if args.format == 'csv':
                    monitor.save_to_csv(output_file)
                else:
                    monitor.save_to_json(output_file)
        else:
            # 持续监控
            monitor.start_monitoring(
                interval=args.interval,
                duration=args.duration,
                output_file=output_file
            )
        
    except Exception as e:
        logger.error(f"监控失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 