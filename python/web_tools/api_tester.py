#!/usr/bin/env python3
"""
API测试器 - RESTful API测试和调试工具

功能:
- 发送HTTP请求 (GET, POST, PUT, DELETE)
- 请求头自定义
- 请求体支持 (JSON, Form, XML)
- 响应验证
- 批量测试
- 性能测试

作者: ToolCollection Team
版本: 1.0.0
"""

import requests
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import time
import yaml
from urllib.parse import urlparse

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class APITester:
    """API测试器类"""
    
    def __init__(self, base_url: str = ""):
        """
        初始化API测试器
        
        Args:
            base_url: 基础URL
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.test_results = []
    
    def send_request(self, method: str, endpoint: str, 
                    headers: Optional[Dict] = None,
                    data: Optional[Dict] = None,
                    json_data: Optional[Dict] = None,
                    params: Optional[Dict] = None,
                    timeout: int = 30) -> Dict[str, Any]:
        """
        发送HTTP请求
        
        Args:
            method: HTTP方法
            endpoint: API端点
            headers: 请求头
            data: 表单数据
            json_data: JSON数据
            params: URL参数
            timeout: 超时时间
            
        Returns:
            响应结果
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}" if self.base_url else endpoint
        
        start_time = time.time()
        
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                headers=headers,
                data=data,
                json=json_data,
                params=params,
                timeout=timeout
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            result = {
                'method': method.upper(),
                'url': url,
                'status_code': response.status_code,
                'response_time': response_time,
                'headers': dict(response.headers),
                'content': response.text,
                'success': response.status_code < 400
            }
            
            # 尝试解析JSON响应
            try:
                result['json'] = response.json()
            except:
                result['json'] = None
            
            logger.info(f"请求完成: {method.upper()} {url} - {response.status_code} ({response_time:.2f}s)")
            
            return result
            
        except Exception as e:
            end_time = time.time()
            result = {
                'method': method.upper(),
                'url': url,
                'error': str(e),
                'response_time': end_time - start_time,
                'success': False
            }
            
            logger.error(f"请求失败: {method.upper()} {url} - {e}")
            return result
    
    def load_test_config(self, config_file: str) -> List[Dict[str, Any]]:
        """
        加载测试配置
        
        Args:
            config_file: 配置文件路径
            
        Returns:
            测试配置列表
        """
        config_path = Path(config_file)
        
        if config_path.suffix.lower() == '.json':
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif config_path.suffix.lower() in ['.yaml', '.yml']:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            raise ValueError(f"不支持的配置文件格式: {config_path.suffix}")
    
    def run_tests(self, tests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        运行测试
        
        Args:
            tests: 测试配置列表
            
        Returns:
            测试结果列表
        """
        results = []
        
        for i, test in enumerate(tests, 1):
            logger.info(f"运行测试 {i}/{len(tests)}: {test.get('name', f'Test {i}')}")
            
            result = self.send_request(
                method=test.get('method', 'GET'),
                endpoint=test.get('endpoint', ''),
                headers=test.get('headers'),
                data=test.get('data'),
                json_data=test.get('json'),
                params=test.get('params'),
                timeout=test.get('timeout', 30)
            )
            
            # 添加测试信息
            result['test_name'] = test.get('name', f'Test {i}')
            result['test_config'] = test
            
            # 验证响应
            if 'validation' in test:
                result['validation'] = self.validate_response(result, test['validation'])
            
            results.append(result)
        
        self.test_results.extend(results)
        return results
    
    def validate_response(self, response: Dict[str, Any], validation: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证响应
        
        Args:
            response: 响应结果
            validation: 验证规则
            
        Returns:
            验证结果
        """
        validation_result = {
            'passed': True,
            'errors': []
        }
        
        # 状态码验证
        if 'status_code' in validation:
            expected_status = validation['status_code']
            if isinstance(expected_status, list):
                if response['status_code'] not in expected_status:
                    validation_result['passed'] = False
                    validation_result['errors'].append(
                        f"状态码验证失败: 期望 {expected_status}, 实际 {response['status_code']}"
                    )
            else:
                if response['status_code'] != expected_status:
                    validation_result['passed'] = False
                    validation_result['errors'].append(
                        f"状态码验证失败: 期望 {expected_status}, 实际 {response['status_code']}"
                    )
        
        # 响应时间验证
        if 'max_response_time' in validation:
            if response['response_time'] > validation['max_response_time']:
                validation_result['passed'] = False
                validation_result['errors'].append(
                    f"响应时间验证失败: 期望 < {validation['max_response_time']}s, "
                    f"实际 {response['response_time']:.2f}s"
                )
        
        # JSON响应验证
        if 'json' in validation and response['json']:
            json_validation = validation['json']
            for key, expected_value in json_validation.items():
                if key not in response['json']:
                    validation_result['passed'] = False
                    validation_result['errors'].append(f"JSON字段缺失: {key}")
                elif response['json'][key] != expected_value:
                    validation_result['passed'] = False
                    validation_result['errors'].append(
                        f"JSON字段验证失败: {key} 期望 {expected_value}, "
                        f"实际 {response['json'][key]}"
                    )
        
        # 响应内容验证
        if 'contains' in validation:
            if validation['contains'] not in response['content']:
                validation_result['passed'] = False
                validation_result['errors'].append(
                    f"响应内容验证失败: 期望包含 '{validation['contains']}'"
                )
        
        return validation_result
    
    def performance_test(self, method: str, endpoint: str, 
                        num_requests: int = 100,
                        concurrent: bool = False,
                        **kwargs) -> Dict[str, Any]:
        """
        性能测试
        
        Args:
            method: HTTP方法
            endpoint: API端点
            num_requests: 请求数量
            concurrent: 是否并发
            **kwargs: 其他请求参数
            
        Returns:
            性能测试结果
        """
        logger.info(f"开始性能测试: {method} {endpoint} ({num_requests} 请求)")
        
        start_time = time.time()
        response_times = []
        success_count = 0
        error_count = 0
        
        for i in range(num_requests):
            result = self.send_request(method, endpoint, **kwargs)
            response_times.append(result['response_time'])
            
            if result['success']:
                success_count += 1
            else:
                error_count += 1
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 计算统计信息
        response_times.sort()
        avg_time = sum(response_times) / len(response_times)
        min_time = response_times[0]
        max_time = response_times[-1]
        median_time = response_times[len(response_times) // 2]
        
        # 计算百分位数
        p95 = response_times[int(len(response_times) * 0.95)]
        p99 = response_times[int(len(response_times) * 0.99)]
        
        performance_result = {
            'total_requests': num_requests,
            'success_count': success_count,
            'error_count': error_count,
            'success_rate': success_count / num_requests * 100,
            'total_time': total_time,
            'requests_per_second': num_requests / total_time,
            'response_times': {
                'average': avg_time,
                'minimum': min_time,
                'maximum': max_time,
                'median': median_time,
                'p95': p95,
                'p99': p99
            }
        }
        
        logger.info(f"性能测试完成: 成功率 {performance_result['success_rate']:.1f}%, "
                   f"平均响应时间 {avg_time:.2f}s, "
                   f"QPS {performance_result['requests_per_second']:.1f}")
        
        return performance_result
    
    def generate_report(self, output_file: str = None) -> str:
        """
        生成测试报告
        
        Args:
            output_file: 输出文件路径
            
        Returns:
            报告内容
        """
        if not self.test_results:
            return "没有测试结果可生成报告"
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['success'])
        failed_tests = total_tests - passed_tests
        
        # 计算平均响应时间
        response_times = [r['response_time'] for r in self.test_results if 'response_time' in r]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        report = f"""
API测试报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

测试统计:
  总测试数: {total_tests}
  通过测试: {passed_tests}
  失败测试: {failed_tests}
  成功率: {passed_tests/total_tests*100:.1f}%
  平均响应时间: {avg_response_time:.2f}s

详细结果:
"""
        
        for i, result in enumerate(self.test_results, 1):
            status = "✓" if result['success'] else "✗"
            report += f"\n{i}. {status} {result.get('test_name', f'Test {i}')}\n"
            report += f"   方法: {result['method']}\n"
            report += f"   URL: {result['url']}\n"
            report += f"   状态码: {result.get('status_code', 'N/A')}\n"
            report += f"   响应时间: {result.get('response_time', 0):.2f}s\n"
            
            if 'validation' in result:
                validation = result['validation']
                if validation['passed']:
                    report += "   验证: ✓ 通过\n"
                else:
                    report += "   验证: ✗ 失败\n"
                    for error in validation['errors']:
                        report += f"     - {error}\n"
            
            if not result['success'] and 'error' in result:
                report += f"   错误: {result['error']}\n"
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            logger.info(f"测试报告已保存到: {output_file}")
        
        return report


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='RESTful API测试和调试工具')
    parser.add_argument('url', help='API URL')
    parser.add_argument('--method', default='GET', choices=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
                       help='HTTP方法')
    parser.add_argument('--headers', help='请求头JSON文件路径')
    parser.add_argument('--data', help='请求数据JSON文件路径')
    parser.add_argument('--params', help='URL参数JSON文件路径')
    parser.add_argument('--config', help='测试配置文件路径')
    parser.add_argument('--performance', type=int, help='性能测试请求数量')
    parser.add_argument('--timeout', type=int, default=30, help='请求超时时间')
    parser.add_argument('--report', help='测试报告输出文件路径')
    
    args = parser.parse_args()
    
    try:
        # 创建API测试器
        tester = APITester()
        
        if args.config:
            # 从配置文件运行测试
            tests = tester.load_test_config(args.config)
            results = tester.run_tests(tests)
        elif args.performance:
            # 性能测试
            headers = None
            data = None
            params = None
            
            if args.headers:
                with open(args.headers, 'r', encoding='utf-8') as f:
                    headers = json.load(f)
            
            if args.data:
                with open(args.data, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            if args.params:
                with open(args.params, 'r', encoding='utf-8') as f:
                    params = json.load(f)
            
            result = tester.performance_test(
                args.method, args.url, args.performance,
                headers=headers, data=data, params=params, timeout=args.timeout
            )
            
            print("性能测试结果:")
            print(f"  总请求数: {result['total_requests']}")
            print(f"  成功率: {result['success_rate']:.1f}%")
            print(f"  平均响应时间: {result['response_times']['average']:.2f}s")
            print(f"  QPS: {result['requests_per_second']:.1f}")
        else:
            # 单次请求测试
            headers = None
            data = None
            params = None
            
            if args.headers:
                with open(args.headers, 'r', encoding='utf-8') as f:
                    headers = json.load(f)
            
            if args.data:
                with open(args.data, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            if args.params:
                with open(args.params, 'r', encoding='utf-8') as f:
                    params = json.load(f)
            
            result = tester.send_request(
                args.method, args.url,
                headers=headers, data=data, params=params, timeout=args.timeout
            )
            
            print(f"请求结果:")
            print(f"  状态码: {result.get('status_code', 'N/A')}")
            print(f"  响应时间: {result.get('response_time', 0):.2f}s")
            print(f"  成功: {result['success']}")
            
            if result.get('json'):
                print(f"  响应JSON: {json.dumps(result['json'], indent=2, ensure_ascii=False)}")
            else:
                print(f"  响应内容: {result.get('content', '')[:500]}...")
        
        # 生成报告
        if args.report:
            report = tester.generate_report(args.report)
            print(report)
        
    except Exception as e:
        logger.error(f"API测试失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 