# ToolCollection 🛠️

[目录导航](#目录导航) | [工具概览](#工具概览) | [使用场景](#使用场景) | [快速体验](#快速体验) | [文档导航](#文档导航) | [环境要求](#环境要求) | [安装指南](#安装指南) | [快速工作流](#快速工作流) | [贡献指南](#贡献指南)

一个开源的跨语言工具集合，专为开发者日常需求设计。每个工具都经过精心设计，开箱即用，支持多种使用场景。

## 📋 目录导航

### 🐍 [Python 工具集合](./python/)
**功能丰富的Python工具集合，涵盖数据处理、文件操作、网络工具、自动化和开发工具**

- 📊 **数据处理**: CSV处理器、JSON处理器、Excel处理器、数据分析器、数据转换器
- 📁 **文件操作**: 批量重命名器、文件监控器、文件同步器、文件去重器、文件压缩器
- 🌐 **网络工具**: 网页爬虫、API测试器、网络监控器、代理检测器、DNS查询器
- 🤖 **自动化**: 系统监控器、任务调度器、日志分析器、进程管理器、服务管理器
- 🛠️ **开发工具**: 代码格式化器、代码生成器、依赖检查器、测试运行器、文档生成器

**[🚀 快速开始](./python/docs/QUICKSTART.md)** | **[📖 详细文档](./python/README.md)** | **[💡 使用示例](./python/docs/examples.md)**

### ☕ [Java 工具集合](./java/)
> **开发中，敬请期待！**

- 计划支持：常用开发工具、构建工具、自动化脚本、数据处理、文件操作等
- 结构将与 Python 工具集保持一致

### [🐚 Shell 工具集合](./shell/)

**功能丰富的 Bash/Shell 脚本集合，涵盖数据处理、文件操作、Web 工具、自动化和开发工具**

- 📊 **数据处理**：CSV快速查看、JSON格式化、文本统计、批量去重、内容筛选、批量转换等
- 📁 **文件操作**：批量重命名、文件查找、压缩解压、目录同步、哈希校验、空间统计、空文件查找等
- 🌐 **Web 工具**：URL可用性检测、DNS查询、HTTP请求、IP归属地、端口扫描、代理检测等
- 🤖 **自动化**：日志清理、目录备份、批量下载、目录监控、定时任务、自动备份、自动清理、自动报告、消息通知等
- 🛠️ **开发工具**：系统信息、端口查杀、网络测速、环境变量对比、进程监控、Docker清理、Git助手、端口占用、环境导出等

> 所有脚本均可直接运行，支持 --help 查看详细用法。

**典型用法示例：**
```bash
# 查看系统信息
./shell/dev_tools/sys_info.sh

# 批量重命名文件
./shell/file_operations/batch_rename.sh ./photos --prefix img_ --number

# 日志清理并归档
./shell/automation/log_cleaner.sh ./logs --days 7 --archive

# 端口扫描
./shell/web_tools/port_scanner.sh 127.0.0.1 --ports 1-1000

# 目录同步
./shell/file_operations/dir_sync.sh ./src ./dst --delete
```

### 🔧 其他语言工具 (规划中)
- **JavaScript/Node.js** - 前端和后端开发工具
- **Go** - 高性能系统工具
- **Rust** - 内存安全的系统工具

## 🎯 项目特色

### ✨ 开箱即用
- 每个工具都经过精心设计，无需复杂配置
- 提供详细的命令行参数和示例
- 支持多种输入输出格式

### 🔧 通用性强
- 工具设计考虑多种使用场景
- 支持自定义参数和配置
- 可与其他工具组合使用

### 📚 文档完善
- 详细的README和快速开始指南
- 丰富的使用示例和最佳实践
- 清晰的代码注释和类型提示

### 🧪 测试完备
- 每个工具都有对应的测试数据
- 提供完整的测试用例
- 支持自动化测试

## 📊 工具概览

| 类别 | 工具数量 | 主要功能 | 状态 |
|------|----------|----------|------|
| 🐍 Python | 50+ | 数据处理、文件操作、网络、自动化、开发 | ✅ 完成 |
| 🐚 Shell  | 40+ | 批量处理、文件管理、网络工具、自动化 | ✅ 完成 |

## 🎯 使用场景

### 📊 数据处理场景
- **批量处理CSV数据文件**
  - Python: `python data_processing/csv_processor.py data.csv --summary`
  - Shell: `./shell/data_processing/csv_parser.sh data.csv --head 10`
- **分析和清理JSON数据**
  - Python: `python data_processing/json_processor.py data.json --format`
  - Shell: `./shell/data_processing/json_prettify.sh data.json --check`

### 📁 文件管理场景
- **批量重命名照片和文档**
  - Python: `python file_operations/batch_renamer.py ./photos --name-pattern "photo_{n:03d}{ext}" --execute`
  - Shell: `./shell/file_operations/batch_rename.sh ./photos --prefix img_ --number`
- **目录同步与备份**
  - Python: `python file_operations/file_sync.py ./source ./backup --mode one_way`
  - Shell: `./shell/file_operations/dir_sync.sh ./src ./dst --delete`

### 🌐 网络开发场景
- **API接口测试和调试**
  - Python: `python web_tools/api_tester.py https://api.example.com/data --method GET`
  - Shell: `./shell/web_tools/http_request.sh https://api.example.com/data --method GET`
- **端口扫描与代理检测**
  - Python: `python web_tools/port_scanner.py 127.0.0.1 --ports 1-1000`
  - Shell: `./shell/web_tools/port_scanner.sh 127.0.0.1 --ports 1-1000`

### 🤖 系统管理场景
- **定时备份与自动清理**
  - Python: `python automation/backup_scheduler.py --schedule daily --source ./data --target ./backup`
  - Shell: `./shell/automation/auto_backup.sh ./data ./backup --interval 60`
- **日志分析和报告**
  - Python: `python automation/log_analyzer.py ./logs --pattern "ERROR" --report`
  - Shell: `./shell/automation/log_cleaner.sh ./logs --days 7 --archive`

### 🛠️ 开发辅助场景
- **环境变量导出与对比**
  - Python: `python dev_tools/env_exporter.py .env`
  - Shell: `./shell/dev_tools/env_exporter.sh .env`
- **进程和端口管理**
  - Python: `python automation/process_manager.py --list --kill zombie`
  - Shell: `./shell/dev_tools/port_killer.sh 8080`

## 🚀 快速体验

### Python工具快速体验
```bash
# 克隆项目
git clone https://github.com/yourusername/ToolCollection.git
cd ToolCollection

# 进入Python工具目录
cd python

# 设置环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt

# 快速体验
python data_processing/csv_processor.py tests/data_processing/test_data.csv --summary
python data_processing/json_processor.py tests/data_processing/test_data.json --format
python file_operations/batch_renamer.py tests/file_operations/ --name-pattern "new_{n}{ext}" --preview
python automation/system_monitor.py --once
python web_tools/api_tester.py https://api.github.com/users/octocat --method GET
```

### Shell工具快速体验
```bash
# 进入Shell工具目录
cd shell

# 查看系统信息
./dev_tools/sys_info.sh

# 批量重命名文件
./file_operations/batch_rename.sh ./photos --prefix img_ --number

# 端口扫描
./web_tools/port_scanner.sh 127.0.0.1 --ports 1-1000

# 目录同步
./file_operations/dir_sync.sh ./src ./dst --delete
```

## 📚 文档导航

### 🐍 Python工具文档
- **[📖 主文档](./python/README.md)** - 完整的工具介绍和使用指南
- **[🚀 快速开始](./python/docs/QUICKSTART.md)** - 5分钟快速上手指南
- **[💡 使用示例](./python/docs/examples.md)** - 详细的使用示例和最佳实践
- **[🧪 测试数据](./python/tests/)** - 各工具的测试文件和示例数据

#### 🧪 测试数据目录规范
- 每种工具类型目录下有 `tests/` 子目录，包含该类型所有工具的测试数据和测试脚本。
- 例如：
  - `python/data_processing/tests/test_data.csv`
  - `python/data_processing/tests/test_data.json`
  - `python/file_operations/tests/photo1.jpg`
  - `python/web_tools/tests/test_crawl.json`
- 新增工具时，请将相关测试数据和测试脚本放入对应类型的 `tests/` 子目录。

### 🐚 Shell工具文档
- **[📖 主文档](./shell/README.md)** - 完整的脚本分类、功能和用法说明

## 🔧 环境要求

### Python工具要求
- **Python**: 3.7+
- **操作系统**: Windows, macOS, Linux
- **依赖管理**: pip + 虚拟环境

### 推荐环境
- **Python**: 3.8+
- **操作系统**: Linux/macOS (更好的命令行体验)
- **编辑器**: VS Code, PyCharm (支持Python开发)

## 📦 安装指南

### Python工具安装
```bash
# 1. 克隆项目
git clone https://github.com/yourusername/ToolCollection.git
cd ToolCollection

# 2. 进入Python工具目录
cd python

# 3. 创建虚拟环境
python3 -m venv venv

# 4. 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 5. 安装依赖
pip install -r requirements.txt

# 6. 验证安装
python -c "import pandas, requests, psutil, matplotlib; print('✅ 安装成功！')"
```

## 🎯 快速工作流

### 数据处理工作流
```bash
# 1. 处理CSV数据
python data_processing/csv_processor.py data.csv --clean --summary

# 2. 转换为JSON格式
python data_processing/csv_processor.py data.csv --output data.json --format json

# 3. 处理JSON数据
python data_processing/json_processor.py data.json --format --summary

# 4. 高级数据分析
python data_processing/data_analyzer.py data.csv --descriptive --correlation

# 5. 数据转换和预处理
python data_processing/data_transformer.py data.csv --normalize standard --encode label
```

### 文件管理工作流
```bash
# 1. 批量重命名文件
python file_operations/batch_renamer.py ./photos --name-pattern "photo_{n:03d}{ext}" --execute

# 2. 监控文件变化
python file_operations/file_monitor.py ./project --patterns "*.py" --command "echo {file} changed"

# 3. 同步文件到备份
python file_operations/file_sync.py ./source ./backup --mode one_way

# 4. 压缩文件
python file_operations/file_compressor.py ./files --compress --output archive.zip
```

### 网络开发工作流
```bash
# 1. 抓取网页数据
python web_tools/web_crawler.py https://example.com -s title "h1" -s content "p" -o data.json

# 2. 测试API接口
python web_tools/api_tester.py https://api.example.com/data --method GET --performance 100

# 3. 监控网络连接
python web_tools/network_monitor.py --target google.com --interval 30

# 4. 检查DNS记录
python web_tools/dns_lookup.py example.com --record-type A
```

### 开发辅助工作流
```bash
# 1. 格式化代码
python dev_tools/code_formatter.py . --recursive

# 2. 检查代码风格
python dev_tools/code_formatter.py . --flake8

# 3. 运行测试
python dev_tools/test_runner.py --coverage --report

# 4. 生成文档
python dev_tools/doc_generator.py --output docs/

# 5. 检查依赖
python dev_tools/dependency_checker.py --update --security
```

### 系统管理工作流
```bash
# 1. 监控系统资源
python automation/system_monitor.py --once

# 2. 分析日志文件
python automation/log_analyzer.py ./logs --pattern "ERROR" --report

# 3. 管理进程
python automation/process_manager.py --list --kill zombie

# 4. 定时备份
python automation/backup_scheduler.py --schedule daily --source ./data --target ./backup
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！无论是报告bug、提出新功能建议，还是提交代码改进，我们都非常欢迎。

### 🐛 报告问题
1. 使用 [GitHub Issues](https://github.com/yourusername/ToolCollection/issues) 报告bug
2. 提供详细的错误信息和复现步骤
3. 包含操作系统和Python版本信息

### 💡 提出建议
1. 使用 [GitHub Discussions](https://github.com/yourusername/ToolCollection/discussions) 提出新功能建议
2. 描述使用场景和预期效果
3. 讨论实现方案和优先级

### 🔧 提交代码
1. **Fork** 本项目
2. **创建** 功能分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 更改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送** 到分支 (`git push origin feature/AmazingFeature`)
5. **打开** Pull Request

### 📝 开发规范
- **代码风格**: 遵循各语言的编码规范
- **文档**: 每个工具都要有清晰的文档说明
- **测试**: 提供测试数据和示例
- **错误处理**: 添加适当的错误处理和日志记录
- **类型提示**: 使用类型提示提高代码可读性

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](./LICENSE) 文件了解详情。

## ⭐ 支持我们

如果这个项目对你有帮助，请给我们一个 ⭐ Star！

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

**💡 提示**: 
- 查看各语言目录下的README获取详细使用指南
- 所有工具都支持 `--help` 参数查看详细用法
- 遇到问题？查看文档或提交Issue
- 有好的想法？欢迎参与讨论和贡献代码 
