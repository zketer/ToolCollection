# 快速开始指南 🚀

这个指南将帮助你在5分钟内开始使用ToolCollection的Python工具。

## 1. 环境准备

### 激活虚拟环境
```bash
# 进入python目录
cd python

# 激活虚拟环境
source venv/bin/activate

# 或者使用提供的脚本
./activate_env.sh
```

### 验证安装
```bash
# 检查Python版本
python --version

# 检查关键依赖
python -c "import pandas, requests, psutil; print('依赖安装成功！')"
```

## 2. 快速体验

### 数据处理 - CSV处理器
```bash
# 创建测试数据
echo "name,age,city
张三,25,北京
李四,30,上海
王五,28,广州" > test.csv

# 处理数据
python data_processing/csv_processor.py test.csv --summary
```

### 文件操作 - 批量重命名器
```bash
# 创建测试文件
mkdir test_files
touch test_files/file1.txt test_files/file2.txt

# 预览重命名
python file_operations/batch_renamer.py test_files --name-pattern "new_{n}{ext}" --preview
```

### 网络工具 - 网页爬虫
```bash
# 抓取网页基本信息
python web_tools/web_crawler.py https://httpbin.org/html --extract-links
```

### 系统监控
```bash
# 查看系统状态
python automation/system_monitor.py --once
```

### 代码格式化
```bash
# 检查代码格式
python dev_tools/code_formatter.py data_processing/csv_processor.py --check
```

## 3. 常用工作流

### 数据处理工作流
```bash
# 1. 抓取数据
python web_tools/web_crawler.py https://example.com \
    -s title "h1" \
    -s content "p" \
    -o raw_data.json

# 2. 转换为CSV（手动或使用其他工具）

# 3. 处理数据
python data_processing/csv_processor.py data.csv \
    --clean \
    --sort name \
    --filter status active \
    -o processed_data.csv
```

### 文件整理工作流
```bash
# 1. 批量重命名照片
python file_operations/batch_renamer.py ./photos \
    --name-pattern "vacation_{n:03d}{ext}" \
    --execute

# 2. 添加日期前缀
python file_operations/batch_renamer.py ./photos \
    --prefix "2024_01_15_" \
    --execute
```

### 开发工作流
```bash
# 1. 格式化代码
python dev_tools/code_formatter.py . --recursive

# 2. 检查代码风格
python dev_tools/code_formatter.py . --flake8

# 3. 监控系统资源
python automation/system_monitor.py -i 30 -d 300
```

## 4. 实用技巧

### 组合使用工具
```bash
# 监控系统 + 保存报告
python automation/system_monitor.py --once -o system_report.json

# 格式化代码 + 生成报告
python dev_tools/code_formatter.py . --recursive --flake8 -o format_report.json
```

### 批量处理
```bash
# 处理多个CSV文件
for file in *.csv; do
    python data_processing/csv_processor.py "$file" --clean -o "cleaned_$file"
done

# 格式化多个目录
for dir in project1 project2 project3; do
    python dev_tools/code_formatter.py "$dir" --recursive
done
```

### 自动化脚本
```bash
#!/bin/bash
# daily_maintenance.sh

echo "开始日常维护..."

# 系统监控
python automation/system_monitor.py --once -o daily_monitor.json

# 代码格式化
python dev_tools/code_formatter.py . --recursive --flake8 -o daily_format.json

echo "维护完成！"
```

## 5. 故障排除

### 常见问题

**问题**: `ModuleNotFoundError: No module named 'pandas'`
**解决**: 确保已激活虚拟环境 `source venv/bin/activate`

**问题**: `Permission denied`
**解决**: 检查文件权限 `chmod +x script.py`

**问题**: 网络请求失败
**解决**: 检查网络连接，或增加延迟时间 `--delay 2.0`

### 获取帮助
```bash
# 查看工具帮助
python data_processing/csv_processor.py --help
python file_operations/batch_renamer.py --help
python web_tools/web_crawler.py --help
python automation/system_monitor.py --help
python dev_tools/code_formatter.py --help
```

## 6. 下一步

- 查看 [examples.md](examples.md) 获取详细使用示例
- 阅读 [README.md](README.md) 了解完整功能
- 探索各个工具的源代码学习实现
- 贡献新的工具或改进现有工具

---

**提示**: 所有工具都支持 `--help` 参数查看详细用法！ 