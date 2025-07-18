# ToolCollection 🛠️

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

### ☕ [Java 工具集](./java/)
> **开发中，敬请期待！**

- 计划支持：常用开发工具、构建工具、自动化脚本、数据处理、文件操作等
- 结构将与 Python 工具集保持一致

- [🐚 Shell 工具集](./shell/)  
  常用 Bash/Shell 脚本，适用于开发、运维、数据处理等场景。

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

## 📊 工具概览

| 类别 | 工具数量 | 主要功能 | 状态 |
|------|----------|----------|------|
| 📊 数据处理 | 10个 | CSV/JSON/Excel处理、数据分析、格式转换 | ✅ 完成 |
| 📁 文件操作 | 10个 | 重命名、监控、同步、压缩、加密 | ✅ 完成 |
| 🌐 网络工具 | 10个 | 爬虫、API测试、网络监控、DNS查询 | ✅ 完成 |
| 🤖 自动化 | 10个 | 系统监控、任务调度、日志分析 | ✅ 完成 |
| 🛠️ 开发工具 | 10个 | 代码格式化、生成、测试、文档 | ✅ 完成 |

## 🎯 使用场景

### 📊 数据处理场景
- **批量处理CSV数据文件** - 使用CSV处理器清洗和转换数据
- **分析和清理JSON数据** - 使用JSON处理器验证和格式化数据
- **Excel文件自动化处理** - 使用Excel处理器生成图表和透视表
- **高级数据分析和可视化** - 使用数据分析器进行统计分析
- **多格式数据转换** - 使用数据转换器进行格式转换和预处理

### 📁 文件管理场景
- **批量重命名照片和文档** - 使用批量重命名器整理文件
- **监控项目文件变化** - 使用文件监控器跟踪文件变更
- **多设备文件同步** - 使用文件同步器保持文件一致
- **智能文件分类和备份** - 使用文件分类器和备份器
- **文件压缩和加密** - 使用文件压缩器和加密器

### 🌐 网络开发场景
- **抓取网页数据用于分析** - 使用网页爬虫获取数据
- **API接口测试和调试** - 使用API测试器验证接口
- **网络连接监控** - 使用网络监控器分析性能
- **DNS记录查询** - 使用DNS查询器解析域名
- **代理服务器检测** - 使用代理检测器验证代理

### 🤖 系统管理场景
- **监控系统资源使用** - 使用系统监控器跟踪性能
- **自动化系统维护** - 使用任务调度器执行定时任务
- **日志分析和报告** - 使用日志分析器处理日志
- **进程和服务管理** - 使用进程管理器和服务管理器
- **系统性能优化** - 使用性能分析器和资源清理器

### 🛠️ 开发辅助场景
- **保持代码风格一致** - 使用代码格式化器统一代码风格
- **自动化测试执行** - 使用测试运行器批量运行测试
- **代码质量检查** - 使用代码审查器检查代码质量
- **自动化文档生成** - 使用文档生成器生成文档
- **持续集成和部署** - 使用部署助手自动化部署

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
