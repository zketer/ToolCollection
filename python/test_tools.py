#!/usr/bin/env python3
"""
工具测试脚本 - 验证所有工具是否正常工作

作者: ToolCollection
版本: 1.0.0
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path


def test_imports():
    """测试依赖导入"""
    print("🔍 测试依赖导入...")
    
    required_modules = [
        'pandas',
        'requests', 
        'psutil',
        'matplotlib',
        'seaborn',
        'scipy',
        'sklearn',
        'yaml',
        'openpyxl'
    ]
    
    optional_modules = [
        'mysql.connector',
        'psycopg2',
        'schedule'
    ]
    
    failed_imports = []
    
    # 测试必需模块
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    # 测试可选模块
    print("\n📦 可选模块:")
    for module in optional_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ⚠️  {module}: 未安装 (可选)")
    
    if failed_imports:
        print(f"\n❌ 缺少必需模块: {', '.join(failed_imports)}")
        print("💡 请运行: pip install -r requirements.txt")
        return False
    
    print("\n✅ 所有必需模块导入成功!")
    return True


def test_data_processing_tools():
    """测试数据处理工具"""
    print("\n📊 测试数据处理工具...")
    
    tools = [
        ('csv_processor.py', ['--help']),
        ('json_processor.py', ['--help']),
        ('excel_processor.py', ['--help']),
        ('data_analyzer.py', ['--help']),
        ('data_transformer.py', ['--help']),
        ('database_manager.py', ['--help']),
        ('data_validator.py', ['--help']),
        ('data_sampler.py', ['--help']),
        ('data_merger.py', ['--help']),
        ('data_exporter.py', ['--help'])
    ]
    
    for tool, args in tools:
        tool_path = f"data_processing/{tool}"
        if os.path.exists(tool_path):
            try:
                result = subprocess.run(
                    [sys.executable, tool_path] + args,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    print(f"  ✅ {tool}")
                else:
                    print(f"  ❌ {tool}: {result.stderr.strip()}")
            except Exception as e:
                print(f"  ❌ {tool}: {e}")
        else:
            print(f"  ⚠️  {tool}: 文件不存在")


def test_file_operations_tools():
    """测试文件操作工具"""
    print("\n📁 测试文件操作工具...")
    
    tools = [
        ('batch_renamer.py', ['--help']),
        ('file_monitor.py', ['--help']),
        ('file_sync.py', ['--help']),
        ('file_deduplicator.py', ['--help']),
        ('file_compressor.py', ['--help']),
        ('file_encryptor.py', ['--help']),
        ('file_searcher.py', ['--help']),
        ('file_backup.py', ['--help']),
        ('file_classifier.py', ['--help']),
        ('file_validator.py', ['--help'])
    ]
    
    for tool, args in tools:
        tool_path = f"file_operations/{tool}"
        if os.path.exists(tool_path):
            try:
                result = subprocess.run(
                    [sys.executable, tool_path] + args,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    print(f"  ✅ {tool}")
                else:
                    print(f"  ❌ {tool}: {result.stderr.strip()}")
            except Exception as e:
                print(f"  ❌ {tool}: {e}")
        else:
            print(f"  ⚠️  {tool}: 文件不存在")


def test_web_tools():
    """测试网络工具"""
    print("\n🌐 测试网络工具...")
    
    tools = [
        ('web_crawler.py', ['--help']),
        ('api_tester.py', ['--help']),
        ('network_monitor.py', ['--help']),
        ('proxy_checker.py', ['--help']),
        ('dns_lookup.py', ['--help']),
        ('port_scanner.py', ['--help'])
    ]
    
    for tool, args in tools:
        tool_path = f"web_tools/{tool}"
        if os.path.exists(tool_path):
            try:
                result = subprocess.run(
                    [sys.executable, tool_path] + args,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    print(f"  ✅ {tool}")
                else:
                    print(f"  ❌ {tool}: {result.stderr.strip()}")
            except Exception as e:
                print(f"  ❌ {tool}: {e}")
        else:
            print(f"  ⚠️  {tool}: 文件不存在")


def test_automation_tools():
    """测试自动化工具"""
    print("\n🤖 测试自动化工具...")
    
    tools = [
        ('system_monitor.py', ['--help']),
        ('task_scheduler.py', ['--help'])
    ]
    
    for tool, args in tools:
        tool_path = f"automation/{tool}"
        if os.path.exists(tool_path):
            try:
                result = subprocess.run(
                    [sys.executable, tool_path] + args,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    print(f"  ✅ {tool}")
                else:
                    print(f"  ❌ {tool}: {result.stderr.strip()}")
            except Exception as e:
                print(f"  ❌ {tool}: {e}")
        else:
            print(f"  ⚠️  {tool}: 文件不存在")


def test_dev_tools():
    """测试开发工具"""
    print("\n🛠️ 测试开发工具...")
    
    tools = [
        ('code_formatter.py', ['--help']),
        ('code_generator.py', ['--help'])
    ]
    
    for tool, args in tools:
        tool_path = f"dev_tools/{tool}"
        if os.path.exists(tool_path):
            try:
                result = subprocess.run(
                    [sys.executable, tool_path] + args,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    print(f"  ✅ {tool}")
                else:
                    print(f"  ❌ {tool}: {result.stderr.strip()}")
            except Exception as e:
                print(f"  ❌ {tool}: {e}")
        else:
            print(f"  ⚠️  {tool}: 文件不存在")


def test_sample_data():
    """测试示例数据"""
    print("\n📋 测试示例数据...")
    
    test_files = [
        'data_processing/tests/test_data.csv',
        'data_processing/tests/test_data.json'
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"  ✅ {file_path} ({file_size} bytes)")
        else:
            print(f"  ❌ {file_path}: 文件不存在")


def run_quick_tests():
    """运行快速功能测试"""
    print("\n🚀 运行快速功能测试...")
    
    # 测试CSV处理器
    print("\n📊 测试CSV处理器:")
    csv_file = 'data_processing/tests/test_data.csv'
    if os.path.exists(csv_file):
        try:
            result = subprocess.run(
                [sys.executable, 'data_processing/csv_processor.py', csv_file, '--summary'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print("  ✅ CSV处理器测试通过")
            else:
                print(f"  ❌ CSV处理器测试失败: {result.stderr.strip()}")
        except Exception as e:
            print(f"  ❌ CSV处理器测试异常: {e}")
    else:
        print("  ⚠️  跳过CSV测试 (测试文件不存在)")
    
    # 测试JSON处理器
    print("\n📄 测试JSON处理器:")
    json_file = 'data_processing/tests/test_data.json'
    if os.path.exists(json_file):
        try:
            result = subprocess.run(
                [sys.executable, 'data_processing/json_processor.py', json_file, '--summary'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print("  ✅ JSON处理器测试通过")
            else:
                print(f"  ❌ JSON处理器测试失败: {result.stderr.strip()}")
        except Exception as e:
            print(f"  ❌ JSON处理器测试异常: {e}")
    else:
        print("  ⚠️  跳过JSON测试 (测试文件不存在)")
    
    # 测试系统监控器
    print("\n💻 测试系统监控器:")
    try:
        result = subprocess.run(
            [sys.executable, 'automation/system_monitor.py', '--once'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("  ✅ 系统监控器测试通过")
        else:
            print(f"  ❌ 系统监控器测试失败: {result.stderr.strip()}")
    except Exception as e:
        print(f"  ❌ 系统监控器测试异常: {e}")


def main():
    """主函数"""
    print("🧪 ToolCollection 工具测试")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists('requirements.txt'):
        print("❌ 请在python目录下运行此脚本")
        sys.exit(1)
    
    # 运行测试
    success = True
    
    # 测试依赖导入
    if not test_imports():
        success = False
    
    # 测试工具文件
    test_data_processing_tools()
    test_file_operations_tools()
    test_web_tools()
    test_automation_tools()
    test_dev_tools()
    
    # 测试示例数据
    test_sample_data()
    
    # 运行快速功能测试
    run_quick_tests()
    
    # 总结
    print("\n" + "=" * 50)
    if success:
        print("🎉 测试完成! 所有必需依赖已正确安装。")
        print("\n💡 下一步:")
        print("  1. 查看 README.md 了解工具使用方法")
        print("  2. 运行 python docs/QUICKSTART.md 快速开始")
        print("  3. 尝试运行各个工具")
    else:
        print("⚠️  测试完成，但发现一些问题。")
        print("💡 请检查错误信息并安装缺失的依赖。")
    
    print("\n📚 更多信息:")
    print("  - 详细文档: README.md")
    print("  - 快速开始: docs/QUICKSTART.md")
    print("  - 使用示例: docs/examples.md")


if __name__ == "__main__":
    main() 