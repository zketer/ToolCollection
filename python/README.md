# Python 工具集合 🐍

一个功能丰富的Python工具集合，专为开发者日常需求设计。每个工具都经过精心设计，开箱即用，支持多种使用场景。

## 📋 目录导航

- [🐍 Python 工具集](../python/)
- [☕ Java 工具集](../java/)  （开发中，结构与Python一致）

### 🔧 [数据处理工具](./data_processing/)
- **[CSV处理器](./data_processing/csv_processor.py)** - 批量处理CSV文件，支持数据清洗、转换和合并
- **[JSON处理器](./data_processing/json_processor.py)** - JSON数据验证、格式化、路径查询和合并
- **[Excel处理器](./data_processing/excel_processor.py)** - Excel文件处理、图表生成、数据透视表
- **[数据分析器](./data_processing/data_analyzer.py)** - 高级数据分析、统计、可视化
- **[数据转换器](./data_processing/data_transformer.py)** - 多格式转换、特征工程、数据预处理
- **[数据库管理器](./data_processing/database_manager.py)** - 数据库连接、查询、备份
- **[数据验证器](./data_processing/data_validator.py)** - 数据质量检查、规则验证
- **[数据采样器](./data_processing/data_sampler.py)** - 智能数据采样、平衡处理
- **[数据合并器](./data_processing/data_merger.py)** - 多源数据合并、关联分析
- **[数据导出器](./data_processing/data_exporter.py)** - 多格式数据导出、报表生成

### 📁 [文件操作工具](./file_operations/)
- **[批量重命名器](./file_operations/batch_renamer.py)** - 根据规则批量重命名文件和文件夹
- **[文件监控器](./file_operations/file_monitor.py)** - 监控文件变化并执行相应操作
- **[文件同步器](./file_operations/file_sync.py)** - 双向文件同步、增量同步
- **[文件去重器](./file_operations/file_deduplicator.py)** - 检测和删除重复文件
- **[文件压缩器](./file_operations/file_compressor.py)** - 批量压缩、解压缩文件
- **[文件加密器](./file_operations/file_encryptor.py)** - 文件加密、解密工具
- **[文件搜索器](./file_operations/file_searcher.py)** - 高级文件搜索、内容匹配
- **[文件备份器](./file_operations/file_backup.py)** - 自动备份、版本管理
- **[文件分类器](./file_operations/file_classifier.py)** - 智能文件分类、整理
- **[文件校验器](./file_operations/file_validator.py)** - 文件完整性校验、修复

### 🌐 [网络工具](./web_tools/)
- **[网页爬虫](./web_tools/web_crawler.py)** - 简单的网页数据抓取工具
- **[API测试器](./web_tools/api_tester.py)** - RESTful API测试和调试工具
- **[网络监控器](./web_tools/network_monitor.py)** - 网络连接监控、性能分析
- **[代理检测器](./web_tools/proxy_checker.py)** - 代理服务器检测、验证
- **[DNS查询器](./web_tools/dns_lookup.py)** - DNS记录查询、解析
- **[端口扫描器](./web_tools/port_scanner.py)** - 端口扫描、服务检测
- **[网络诊断器](./web_tools/network_diagnostic.py)** - 网络故障诊断、分析
- **[WebSocket客户端](./web_tools/websocket_client.py)** - WebSocket连接、测试
- **[邮件发送器](./web_tools/email_sender.py)** - 批量邮件发送、模板支持
- **[FTP客户端](./web_tools/ftp_client.py)** - FTP文件传输、管理

### 🤖 [自动化工具](./automation/)
- **[系统监控器](./automation/system_monitor.py)** - 监控系统资源使用情况（CPU、内存、磁盘、网络）
- **[任务调度器](./automation/task_scheduler.py)** - 定时任务调度、管理
- **[日志分析器](./automation/log_analyzer.py)** - 日志文件分析、统计
- **[进程管理器](./automation/process_manager.py)** - 进程监控、管理
- **[服务管理器](./automation/service_manager.py)** - 系统服务管理、控制
- **[定时备份器](./automation/backup_scheduler.py)** - 自动备份调度、执行
- **[性能分析器](./automation/performance_analyzer.py)** - 系统性能分析、优化
- **[资源清理器](./automation/resource_cleaner.py)** - 系统资源清理、优化
- **[自动化测试器](./automation/auto_tester.py)** - 自动化测试执行、报告
- **[工作流引擎](./automation/workflow_engine.py)** - 工作流定义、执行

### 🛠️ [开发工具](./dev_tools/)
- **[代码格式化器](./dev_tools/code_formatter.py)** - 自动格式化Python代码（Black + Flake8）
- **[代码生成器](./dev_tools/code_generator.py)** - 代码模板生成、脚手架
- **[依赖检查器](./dev_tools/dependency_checker.py)** - 依赖版本检查、更新
- **[测试运行器](./dev_tools/test_runner.py)** - 自动化测试执行、覆盖率
- **[文档生成器](./dev_tools/doc_generator.py)** - 代码文档生成、更新
- **[代码审查器](./dev_tools/code_reviewer.py)** - 代码质量检查、建议
- **[性能分析器](./dev_tools/performance_profiler.py)** - 代码性能分析、优化
- **[调试助手](./dev_tools/debug_helper.py)** - 调试工具、日志分析
- **[版本管理器](./dev_tools/version_manager.py)** - 版本控制、标签管理
- **[部署助手](./dev_tools/deployment_helper.py)** - 自动化部署、配置管理

### 📚 [文档和测试](./docs/)
- **[快速开始指南](./docs/QUICKSTART.md)** - 5分钟快速上手
- **[详细使用示例](./docs/examples.md)** - 完整的使用示例和最佳实践
- **[测试数据](./tests/)** - 各工具的测试文件和示例数据

#### 🧪 测试数据规范
- 每种工具类型目录下有 `tests/` 子目录，包含该类型所有工具的测试数据和测试脚本。
- 例如：
  - `data_processing/tests/test_data.csv`
  - `data_processing/tests/test_data.json`
  - `file_operations/tests/photo1.jpg`
  - `web_tools/tests/test_crawl.json`
- 新增工具时，请将相关测试数据和测试脚本放入对应类型的 `tests/` 子目录。

## 🚀 快速开始

### 环境准备
```bash
# 进入python目录
cd python

# 激活虚拟环境
source venv/bin/activate

# 验证安装
python -c "import pandas, requests, psutil, matplotlib; print('✅ 依赖安装成功！')"
```

### 快速体验
```bash
# 处理CSV数据
python data_processing/csv_processor.py data_processing/tests/test_data.csv --summary

# 格式化JSON
python data_processing/json_processor.py data_processing/tests/test_data.json --format

# 批量重命名文件
python file_operations/batch_renamer.py tests/file_operations/ --name-pattern "new_{n}{ext}" --preview

# 监控系统状态
python automation/system_monitor.py --once

# 格式化代码
python dev_tools/code_formatter.py . --check

# 测试API
python web_tools/api_tester.py https://api.github.com/users/octocat --method GET
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

#### [Excel处理器](./data_processing/excel_processor.py)
**功能**: 专业的Excel文件处理工具
- ✅ 多工作表处理
- ✅ 数据透视表生成
- ✅ 图表创建和样式设置
- ✅ 公式计算和验证
- ✅ 数据清洗和验证

**快速使用**:
```bash
# 显示工作表信息
python data_processing/excel_processor.py data.xlsx --info

# 创建数据透视表
python data_processing/excel_processor.py data.xlsx --pivot "category" "region" "sales"

# 生成图表
python data_processing/excel_processor.py data.xlsx --chart bar "month" "revenue,profit"
```

#### [数据分析器](./data_processing/data_analyzer.py)
**功能**: 高级数据分析和统计工具
- ✅ 描述性统计分析
- ✅ 相关性分析和异常值检测
- ✅ 数据分布分析
- ✅ 时间序列分析
- ✅ 机器学习预处理

**快速使用**:
```bash
# 描述性统计
python data_processing/data_analyzer.py data.csv --descriptive

# 相关性分析
python data_processing/data_analyzer.py data.csv --correlation

# 异常值检测
python data_processing/data_analyzer.py data.csv --outliers
```

#### [数据转换器](./data_processing/data_transformer.py)
**功能**: 多格式数据转换和预处理工具
- ✅ 多种格式转换 (CSV, JSON, XML, YAML, Excel)
- ✅ 数据编码转换
- ✅ 特征工程
- ✅ 数据标准化和归一化
- ✅ 数据采样和分割

**快速使用**:
```bash
# 格式转换
python data_processing/data_transformer.py data.csv -o data.json --format json

# 数据标准化
python data_processing/data_transformer.py data.csv --normalize standard

# 特征工程
python data_processing/data_transformer.py data.csv --features features_config.json
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

#### [文件同步器](./file_operations/file_sync.py)
**功能**: 强大的文件同步工具
- ✅ 双向文件同步
- ✅ 增量同步
- ✅ 冲突检测和解决
- ✅ 同步日志记录
- ✅ 多种同步策略

**快速使用**:
```bash
# 单向同步
python file_operations/file_sync.py ./source ./backup --mode one_way

# 双向同步
python file_operations/file_sync.py ./dir1 ./dir2 --mode two_way --dry-run
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

#### [API测试器](./web_tools/api_tester.py)
**功能**: 专业的API测试和调试工具
- ✅ 发送HTTP请求 (GET, POST, PUT, DELETE)
- ✅ 请求头自定义
- ✅ 响应验证
- ✅ 批量测试
- ✅ 性能测试

**快速使用**:
```bash
# 基本API测试
python web_tools/api_tester.py https://api.github.com/users/octocat --method GET

# 性能测试
python web_tools/api_tester.py https://api.example.com/data --performance 100

# 批量测试
python web_tools/api_tester.py https://api.example.com --config tests.json
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
- 📋 Excel文件自动化处理
- 🔬 高级数据分析和可视化

### 文件管理场景
- 📁 批量重命名照片和文档
- 👀 监控项目文件变化
- 🔄 自动化文件整理
- 🔗 多设备文件同步
- 🗂️ 智能文件分类和备份

### 开发辅助场景
- 🌐 抓取网页数据用于分析
- 🔧 API接口测试和调试
- 💻 监控系统资源使用
- 🎨 保持代码风格一致
- 📝 自动化文档生成

### 自动化场景
- 🤖 定时系统监控
- 📝 自动代码格式化
- 🔄 文件变化触发操作
- 📊 自动化数据报告
- 🚀 持续集成和部署

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