#!/usr/bin/env python3
"""
网络监控器 - 网络连接监控、性能分析工具

功能:
- 监控网络连接状态和延迟
- 检测网络丢包率
- 监控带宽使用情况
- 网络性能统计和报告
- 支持多种网络协议

作者: ToolCollection
版本: 1.0.0
"""

import argparse
import json
import socket
import sys
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import statistics

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


class NetworkMonitor:
    """网络监控器类"""
    
    def __init__(self):
        """初始化网络监控器"""
        self.stats = {
            'ping_results': [],
            'connection_tests': [],
            'bandwidth_stats': [],
            'start_time': datetime.now()
        }
        
    def ping_host(self, host: str, port: int = 80, timeout: float = 5.0) -> Dict:
        """
        测试主机连通性
        
        Args:
            host: 目标主机
            port: 端口号
            timeout: 超时时间
            
        Returns:
            测试结果字典
        """
        start_time = time.time()
        result = {
            'host': host,
            'port': port,
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'latency': None,
            'error': None
        }
        
        try:
            # 创建socket连接
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            # 尝试连接
            sock.connect((host, port))
            end_time = time.time()
            
            result['success'] = True
            result['latency'] = (end_time - start_time) * 1000  # 转换为毫秒
            sock.close()
            
        except socket.timeout:
            result['error'] = '连接超时'
        except socket.gaierror:
            result['error'] = '无法解析主机名'
        except ConnectionRefusedError:
            result['error'] = '连接被拒绝'
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def test_connection(self, host: str, port: int = 80, count: int = 5) -> Dict:
        """
        执行多次连接测试
        
        Args:
            host: 目标主机
            port: 端口号
            count: 测试次数
            
        Returns:
            测试统计结果
        """
        results = []
        successful_pings = []
        
        print(f"🔍 测试连接到 {host}:{port}")
        
        for i in range(count):
            result = self.ping_host(host, port)
            results.append(result)
            
            if result['success']:
                successful_pings.append(result['latency'])
                print(f"  {i+1}/{count}: ✅ {result['latency']:.2f}ms")
            else:
                print(f"  {i+1}/{count}: ❌ {result['error']}")
            
            if i < count - 1:  # 不是最后一次
                time.sleep(1)
        
        # 计算统计信息
        stats = {
            'host': host,
            'port': port,
            'total_tests': count,
            'successful_tests': len(successful_pings),
            'failed_tests': count - len(successful_pings),
            'success_rate': len(successful_pings) / count * 100,
            'min_latency': min(successful_pings) if successful_pings else None,
            'max_latency': max(successful_pings) if successful_pings else None,
            'avg_latency': statistics.mean(successful_pings) if successful_pings else None,
            'std_latency': statistics.stdev(successful_pings) if len(successful_pings) > 1 else None,
            'results': results
        }
        
        return stats
    
    def get_network_interfaces(self) -> List[Dict]:
        """获取网络接口信息"""
        if not HAS_PSUTIL:
            print("⚠️  psutil未安装，无法获取网络接口信息")
            return []
        
        interfaces = []
        net_io = psutil.net_io_counters(pernic=True)
        net_addrs = psutil.net_if_addrs()
        
        for interface_name, addrs in net_addrs.items():
            interface_info = {
                'name': interface_name,
                'addresses': [],
                'io_stats': net_io.get(interface_name, {})
            }
            
            for addr in addrs:
                interface_info['addresses'].append({
                    'family': str(addr.family),
                    'address': addr.address,
                    'netmask': addr.netmask,
                    'broadcast': getattr(addr, 'broadcast', None)
                })
            
            interfaces.append(interface_info)
        
        return interfaces
    
    def monitor_bandwidth(self, duration: int = 60, interval: float = 1.0) -> List[Dict]:
        """
        监控带宽使用情况
        
        Args:
            duration: 监控时长 (秒)
            interval: 采样间隔 (秒)
            
        Returns:
            带宽使用记录列表
        """
        if not HAS_PSUTIL:
            print("⚠️  psutil未安装，无法监控带宽")
            return []
        
        print(f"📊 开始监控带宽使用 ({duration}秒, 间隔{interval}秒)")
        
        bandwidth_stats = []
        start_time = time.time()
        last_io = psutil.net_io_counters()
        
        while time.time() - start_time < duration:
            time.sleep(interval)
            
            current_io = psutil.net_io_counters()
            elapsed = interval
            
            # 计算速率
            bytes_sent = current_io.bytes_sent - last_io.bytes_sent
            bytes_recv = current_io.bytes_recv - last_io.bytes_recv
            
            sent_rate = bytes_sent / elapsed
            recv_rate = bytes_recv / elapsed
            
            stat = {
                'timestamp': datetime.now().isoformat(),
                'bytes_sent': bytes_sent,
                'bytes_recv': bytes_recv,
                'sent_rate_bps': sent_rate,
                'recv_rate_bps': recv_rate,
                'sent_rate_mbps': sent_rate * 8 / 1_000_000,  # 转换为Mbps
                'recv_rate_mbps': recv_rate * 8 / 1_000_000
            }
            
            bandwidth_stats.append(stat)
            last_io = current_io
            
            # 显示实时信息
            print(f"  📤 发送: {stat['sent_rate_mbps']:.2f} Mbps, "
                  f"📥 接收: {stat['recv_rate_mbps']:.2f} Mbps")
        
        return bandwidth_stats
    
    def continuous_monitoring(self, target: str, port: int = 80, 
                            interval: float = 30.0, duration: int = None) -> None:
        """
        持续监控网络连接
        
        Args:
            target: 目标主机
            port: 端口号
            interval: 监控间隔 (秒)
            duration: 监控时长 (秒)，None表示无限监控
        """
        print(f"🔄 开始持续监控 {target}:{port} (间隔: {interval}秒)")
        if duration:
            print(f"⏱️  监控时长: {duration}秒")
        else:
            print("⏱️  无限监控 (按Ctrl+C停止)")
        
        start_time = time.time()
        test_count = 0
        
        try:
            while True:
                test_count += 1
                current_time = datetime.now().strftime('%H:%M:%S')
                
                result = self.ping_host(target, port)
                self.stats['ping_results'].append(result)
                
                if result['success']:
                    print(f"[{current_time}] #{test_count}: ✅ {result['latency']:.2f}ms")
                else:
                    print(f"[{current_time}] #{test_count}: ❌ {result['error']}")
                
                # 检查是否达到监控时长
                if duration and (time.time() - start_time) >= duration:
                    break
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n⚠️  监控被用户中断")
        
        # 生成统计报告
        self.print_monitoring_summary()
    
    def print_monitoring_summary(self):
        """打印监控摘要"""
        if not self.stats['ping_results']:
            print("❌ 没有监控数据")
            return
        
        successful_pings = [r for r in self.stats['ping_results'] if r['success']]
        failed_pings = [r for r in self.stats['ping_results'] if not r['success']]
        
        if successful_pings:
            latencies = [r['latency'] for r in successful_pings]
            print(f"\n📊 监控摘要:")
            print(f"  总测试次数: {len(self.stats['ping_results'])}")
            print(f"  成功次数: {len(successful_pings)}")
            print(f"  失败次数: {len(failed_pings)}")
            print(f"  成功率: {len(successful_pings) / len(self.stats['ping_results']) * 100:.1f}%")
            print(f"  平均延迟: {statistics.mean(latencies):.2f}ms")
            print(f"  最小延迟: {min(latencies):.2f}ms")
            print(f"  最大延迟: {max(latencies):.2f}ms")
            if len(latencies) > 1:
                print(f"  延迟标准差: {statistics.stdev(latencies):.2f}ms")
        
        if failed_pings:
            error_counts = {}
            for ping in failed_pings:
                error = ping['error']
                error_counts[error] = error_counts.get(error, 0) + 1
            
            print(f"\n❌ 失败原因统计:")
            for error, count in error_counts.items():
                print(f"  {error}: {count}次")
    
    def generate_report(self, output_file: str = None) -> Dict:
        """生成监控报告"""
        report = {
            'monitor_info': {
                'start_time': self.stats['start_time'].isoformat(),
                'end_time': datetime.now().isoformat(),
                'total_duration': (datetime.now() - self.stats['start_time']).total_seconds()
            },
            'ping_results': self.stats['ping_results'],
            'connection_tests': self.stats['connection_tests'],
            'bandwidth_stats': self.stats['bandwidth_stats'],
            'summary': {}
        }
        
        # 计算摘要统计
        if self.stats['ping_results']:
            successful_pings = [r for r in self.stats['ping_results'] if r['success']]
            if successful_pings:
                latencies = [r['latency'] for r in successful_pings]
                report['summary'] = {
                    'total_pings': len(self.stats['ping_results']),
                    'successful_pings': len(successful_pings),
                    'failed_pings': len(self.stats['ping_results']) - len(successful_pings),
                    'success_rate': len(successful_pings) / len(self.stats['ping_results']) * 100,
                    'avg_latency': statistics.mean(latencies),
                    'min_latency': min(latencies),
                    'max_latency': max(latencies),
                    'std_latency': statistics.stdev(latencies) if len(latencies) > 1 else 0
                }
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                print(f"📄 报告已保存到: {output_file}")
            except Exception as e:
                print(f"❌ 保存报告失败: {e}")
        
        return report
    
    @staticmethod
    def format_bandwidth(bytes_per_sec: float) -> str:
        """格式化带宽显示"""
        if bytes_per_sec < 1024:
            return f"{bytes_per_sec:.1f} B/s"
        elif bytes_per_sec < 1024 * 1024:
            return f"{bytes_per_sec / 1024:.1f} KB/s"
        elif bytes_per_sec < 1024 * 1024 * 1024:
            return f"{bytes_per_sec / (1024 * 1024):.1f} MB/s"
        else:
            return f"{bytes_per_sec / (1024 * 1024 * 1024):.1f} GB/s"


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="网络监控器 - 网络连接监控、性能分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 测试单个连接
  python network_monitor.py google.com --test
  
  # 持续监控连接
  python network_monitor.py google.com --monitor --interval 30
  
  # 监控带宽使用
  python network_monitor.py --bandwidth --duration 60
  
  # 显示网络接口信息
  python network_monitor.py --interfaces
  
  # 生成详细报告
  python network_monitor.py google.com --test --report report.json
        """
    )
    
    parser.add_argument('target', nargs='?', help='目标主机')
    parser.add_argument('--port', type=int, default=80, help='端口号 (默认: 80)')
    
    # 测试选项
    parser.add_argument('--test', action='store_true', help='执行连接测试')
    parser.add_argument('--count', type=int, default=5, help='测试次数 (默认: 5)')
    parser.add_argument('--timeout', type=float, default=5.0, help='超时时间 (默认: 5秒)')
    
    # 监控选项
    parser.add_argument('--monitor', action='store_true', help='持续监控连接')
    parser.add_argument('--interval', type=float, default=30.0, help='监控间隔 (默认: 30秒)')
    parser.add_argument('--duration', type=int, help='监控时长 (秒)')
    
    # 带宽监控
    parser.add_argument('--bandwidth', action='store_true', help='监控带宽使用')
    parser.add_argument('--bandwidth-interval', type=float, default=1.0, help='带宽采样间隔 (默认: 1秒)')
    
    # 其他选项
    parser.add_argument('--interfaces', action='store_true', help='显示网络接口信息')
    parser.add_argument('--report', help='生成报告文件路径')
    
    args = parser.parse_args()
    
    # 创建网络监控器
    monitor = NetworkMonitor()
    
    try:
        if args.interfaces:
            # 显示网络接口信息
            print("🌐 网络接口信息:")
            interfaces = monitor.get_network_interfaces()
            for interface in interfaces:
                print(f"\n📡 接口: {interface['name']}")
                for addr in interface['addresses']:
                    print(f"  {addr['family']}: {addr['address']}")
                    if addr['netmask']:
                        print(f"    子网掩码: {addr['netmask']}")
                    if addr['broadcast']:
                        print(f"    广播地址: {addr['broadcast']}")
                
                if interface['io_stats']:
                    stats = interface['io_stats']
                    print(f"  📊 统计信息:")
                    print(f"    发送字节: {stats.bytes_sent:,}")
                    print(f"    接收字节: {stats.bytes_recv:,}")
                    print(f"    发送包数: {stats.packets_sent:,}")
                    print(f"    接收包数: {stats.packets_recv:,}")
        
        elif args.bandwidth:
            # 监控带宽使用
            duration = args.duration or 60
            bandwidth_stats = monitor.monitor_bandwidth(duration, args.bandwidth_interval)
            monitor.stats['bandwidth_stats'] = bandwidth_stats
            
            if bandwidth_stats:
                # 计算带宽统计
                sent_rates = [s['sent_rate_mbps'] for s in bandwidth_stats]
                recv_rates = [s['recv_rate_mbps'] for s in bandwidth_stats]
                
                print(f"\n📊 带宽使用统计:")
                print(f"  平均发送速率: {statistics.mean(sent_rates):.2f} Mbps")
                print(f"  平均接收速率: {statistics.mean(recv_rates):.2f} Mbps")
                print(f"  最大发送速率: {max(sent_rates):.2f} Mbps")
                print(f"  最大接收速率: {max(recv_rates):.2f} Mbps")
        
        elif args.target:
            if args.test:
                # 执行连接测试
                test_stats = monitor.test_connection(args.target, args.port, args.count)
                monitor.stats['connection_tests'].append(test_stats)
                
                print(f"\n📊 测试结果摘要:")
                print(f"  目标: {args.target}:{args.port}")
                print(f"  成功率: {test_stats['success_rate']:.1f}%")
                if test_stats['avg_latency']:
                    print(f"  平均延迟: {test_stats['avg_latency']:.2f}ms")
                    print(f"  最小延迟: {test_stats['min_latency']:.2f}ms")
                    print(f"  最大延迟: {test_stats['max_latency']:.2f}ms")
                    if test_stats['std_latency']:
                        print(f"  延迟标准差: {test_stats['std_latency']:.2f}ms")
            
            elif args.monitor:
                # 持续监控
                monitor.continuous_monitoring(args.target, args.port, args.interval, args.duration)
            
            else:
                # 默认执行单次测试
                result = monitor.ping_host(args.target, args.port, args.timeout)
                if result['success']:
                    print(f"✅ 连接成功: {result['latency']:.2f}ms")
                else:
                    print(f"❌ 连接失败: {result['error']}")
        
        else:
            print("💡 使用 --help 查看使用说明")
        
        # 生成报告
        if args.report:
            monitor.generate_report(args.report)
    
    except KeyboardInterrupt:
        print("\n⚠️  操作被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 