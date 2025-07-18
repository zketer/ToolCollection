# Python 工具集合 🐍

一个功能丰富的Python工具集合，专为开发者日常需求设计。每个工具都经过精心设计，开箱即用，支持多种使用场景。

## 📋 目录导航

### 🔧 [数据处理工具](./data_processing/)
- **[CSV处理器](./data_processing/csv_processor.py)** - 批量处理CSV文件，支持数据清洗、转换和合并
- **[JSON处理器](./data_processing/json_processor.py)** - JSON数据验证、格式化、路径查询和合并

### 📁 [文件操作工具](./file_operations/)
- **[批量重命名器](./file_operations/batch_renamer.py)** - 根据规则批量重命名文件和文件夹
- **[文件监控器](./file_operations/file_monitor.py)** - 监控文件变化并执行相应操作

### 🌐 [网络工具](./web_tools/)
- **[网页爬虫](./web_tools/web_crawler.py)** - 简单的网页数据抓取工具

### 🤖 [自动化工具](./automation/)
- **[系统监控器](./automation/system_monitor.py)** - 监控系统资源使用情况（CPU、内存、磁盘、网络）

### 🛠️ [开发工具](./dev_tools/)
- **[代码格式化器](./dev_tools/code_formatter.py)** - 自动格式化Python代码（Black + Flake8）

### 📚 [文档和测试](./docs/)
- **[快速开始指南](./docs/QUICKSTART.md)** - 5分钟快速上手
- **[详细使用示例](./docs/examples.md)** - 完整的使用示例和最佳实践
- **[测试数据](./tests/)** - 各工具的测试文件和示例数据

## 🚀 快速开始

### 环境准备
```bash
# 进入python目录
cd python

# 激活虚拟环境
source venv/bin/activate

# 验证安装
python -c "import pandas, requests, psutil; print('✅ 依赖安装成功！')"
```

### 快速体验
```bash
# 处理CSV数据
python data_processing/csv_processor.py tests/data_processing/test_data.csv --summary

# 格式化JSON
python data_processing/json_processor.py tests/data_processing/test_data.json --format

# 批量重命名文件
python file_operations/batch_renamer.py tests/file_operations/ --name-pattern "new_{n}{ext}" --preview

# 监控系统状态
python automation/system_monitor.py --once

# 格式化代码
python dev_tools/code_formatter.py . --check
```

## 🛠️ 工具详情

### 📊 数据处理工具

#### [CSV处理器](./data_processing/csv_processor.py)
**功能**: 强大的CSV文件处理工具
- ✅ 数据清洗（删除重复行，填充空值）
- ✅ 列重命名和删除
- ✅ 数据过滤和排序
- ✅ 数据摘要统计
- ✅ 支持多种输出格式

**快速使用**:
```bash
# 基本处理
python data_processing/csv_processor.py data.csv --summary

# 数据清洗和过滤
python data_processing/csv_processor.py data.csv --clean --filter status active --sort age
```

#### [JSON处理器](./data_processing/json_processor.py)
**功能**: 完整的JSON数据处理工具
- ✅ JSON验证和格式化
- ✅ 路径查询和提取
- ✅ 数据合并和比较
- ✅ 压缩和美化
- ✅ 结构分析

**快速使用**:
```bash
# 格式化JSON
python data_processing/json_processor.py data.json --format

# 路径查询
python data_processing/json_processor.py data.json --path "users[0].name"

# 数据摘要
python data_processing/json_processor.py data.json --summary
```

### 📁 文件操作工具

#### [批量重命名器](./file_operations/batch_renamer.py)
**功能**: 灵活的文件批量重命名工具
- ✅ 模式重命名（支持序号、原文件名、扩展名）
- ✅ 正则表达式重命名
- ✅ 前缀/后缀添加
- ✅ 大小写转换
- ✅ 预览模式

**快速使用**:
```bash
# 序号重命名
python file_operations/batch_renamer.py ./photos --name-pattern "photo_{n:03d}{ext}" --execute

# 添加前缀
python file_operations/batch_renamer.py ./files --prefix "backup_" --execute
```

#### [文件监控器](./file_operations/file_monitor.py)
**功能**: 实时文件变化监控工具
- ✅ 监控文件创建、修改、删除、移动
- ✅ 自定义过滤规则
- ✅ 执行自定义命令
- ✅ 生成变化报告
- ✅ 递归监控

**快速使用**:
```bash
# 监控目录变化
python file_operations/file_monitor.py ./project --patterns "*.py" --command "echo {file} changed"

# 监控并生成报告
python file_operations/file_monitor.py ./logs -d 60 --summary -o report.txt
```

### 🌐 网络工具

#### [网页爬虫](./web_tools/web_crawler.py)
**功能**: 简单易用的网页数据抓取工具
- ✅ 抓取网页内容
- ✅ CSS选择器提取
- ✅ 自定义请求头
- ✅ 多种输出格式
- ✅ 请求延迟控制

**快速使用**:
```bash
# 基本抓取
python web_tools/web_crawler.py https://example.com --extract-links

# 自定义提取
python web_tools/web_crawler.py https://example.com -s title "h1" -s content "p" -o data.json
```

### 🤖 自动化工具

#### [系统监控器](./automation/system_monitor.py)
**功能**: 全面的系统资源监控工具
- ✅ CPU使用率和频率监控
- ✅ 内存使用情况
- ✅ 磁盘空间监控
- ✅ 网络流量统计
- ✅ 进程信息分析

**快速使用**:
```bash
# 单次监控
python automation/system_monitor.py --once

# 持续监控
python automation/system_monitor.py -i 10 -d 300 -o monitor.json
```

### 🛠️ 开发工具

#### [代码格式化器](./dev_tools/code_formatter.py)
**功能**: 专业的代码格式化和检查工具
- ✅ Black代码格式化
- ✅ Flake8代码风格检查
- ✅ 批量处理
- ✅ 生成格式化报告
- ✅ 递归处理

**快速使用**:
```bash
# 格式化代码
python dev_tools/code_formatter.py . --recursive

# 代码风格检查
python dev_tools/code_formatter.py . --flake8

# 生成报告
python dev_tools/code_formatter.py . --recursive --flake8 -o format_report.json
```

## 📚 文档导航

### 📖 [快速开始指南](./docs/QUICKSTART.md)
- 🚀 5分钟快速上手
- 🔧 环境准备和验证
- 💡 常用工作流示例
- ⚠️ 故障排除指南

### 📝 [详细使用示例](./docs/examples.md)
- 📊 数据处理工作流
- 📁 文件整理工作流
- 🌐 网络数据抓取
- 🤖 系统监控和自动化
- 🛠️ 开发工具使用

### 🧪 [测试数据](./tests/)
- `tests/data_processing/` - CSV和JSON测试数据
- `tests/file_operations/` - 文件操作测试文件
- `tests/web_tools/` - 网络工具测试数据
- `tests/automation/` - 自动化工具测试数据

## 🔧 环境要求

- **Python**: 3.7+
- **操作系统**: Windows, macOS, Linux
- **依赖管理**: pip + 虚拟环境

## 📦 安装依赖

```bash
# 进入python目录
cd python

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

## 🎯 使用场景

### 数据处理场景
- 📊 批量处理CSV数据文件
- 🔍 分析和清理JSON数据
- 📈 生成数据报告和统计

### 文件管理场景
- 📁 批量重命名照片和文档
- 👀 监控项目文件变化
- 🔄 自动化文件整理

### 开发辅助场景
- 🌐 抓取网页数据用于分析
- 💻 监控系统资源使用
- 🎨 保持代码风格一致

### 自动化场景
- 🤖 定时系统监控
- 📝 自动代码格式化
- 🔄 文件变化触发操作

## 🤝 贡献指南

我们欢迎所有形式的贡献！

1. **Fork** 本项目
2. **创建** 功能分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 更改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送** 到分支 (`git push origin feature/AmazingFeature`)
5. **打开** Pull Request

### 开发规范
- 每个工具都应该有清晰的文档说明
- 包含使用示例和参数说明
- 遵循PEP 8编码规范
- 添加适当的错误处理和日志记录
- 提供测试数据和示例

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](../LICENSE) 文件了解详情。

## ⭐ 支持我们

如果这个项目对你有帮助，请给我们一个 ⭐ Star！

---

**💡 提示**: 
- 所有工具都支持 `--help` 参数查看详细用法
- 查看 [快速开始指南](./docs/QUICKSTART.md) 获取更多使用技巧
- 遇到问题？查看 [使用示例](./docs/examples.md) 或提交 Issue 