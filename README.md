# ToolCollection 🛠️

一个开源的跨语言工具集合，专为开发者日常需求设计。每个工具都经过精心设计，开箱即用，支持多种使用场景。

## 📋 目录导航

### 🐍 [Python 工具集合](./python/)
**功能丰富的Python工具集合，涵盖数据处理、文件操作、网络工具、自动化和开发工具**

- 📊 **数据处理**: CSV处理器、JSON处理器
- 📁 **文件操作**: 批量重命名器、文件监控器  
- 🌐 **网络工具**: 网页爬虫
- 🤖 **自动化**: 系统监控器
- 🛠️ **开发工具**: 代码格式化器

**[🚀 快速开始](./python/docs/QUICKSTART.md)** | **[📖 详细文档](./python/README.md)** | **[💡 使用示例](./python/docs/examples.md)**

### 🔧 其他语言工具 (计划中)
- **JavaScript/Node.js** - 前端和后端开发工具
- **Go** - 高性能系统工具
- **Rust** - 内存安全的系统工具
- **Java** - 企业级开发工具

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
```

## 📊 工具概览

| 类别 | 工具名称 | 功能描述 | 状态 |
|------|----------|----------|------|
| 📊 数据处理 | CSV处理器 | 批量处理CSV文件，支持数据清洗、转换和合并 | ✅ 完成 |
| 📊 数据处理 | JSON处理器 | JSON数据验证、格式化、路径查询和合并 | ✅ 完成 |
| 📁 文件操作 | 批量重命名器 | 根据规则批量重命名文件和文件夹 | ✅ 完成 |
| 📁 文件操作 | 文件监控器 | 监控文件变化并执行相应操作 | ✅ 完成 |
| 🌐 网络工具 | 网页爬虫 | 简单的网页数据抓取工具 | ✅ 完成 |
| 🤖 自动化 | 系统监控器 | 监控系统资源使用情况 | ✅ 完成 |
| 🛠️ 开发工具 | 代码格式化器 | 自动格式化Python代码 | ✅ 完成 |

## 🎯 使用场景

### 📊 数据处理场景
- **批量处理CSV数据文件** - 使用CSV处理器清洗和转换数据
- **分析和清理JSON数据** - 使用JSON处理器验证和格式化数据
- **生成数据报告和统计** - 自动化数据分析和报告生成

### 📁 文件管理场景
- **批量重命名照片和文档** - 使用批量重命名器整理文件
- **监控项目文件变化** - 使用文件监控器跟踪文件变更
- **自动化文件整理** - 根据规则自动组织文件结构

### 🌐 网络开发场景
- **抓取网页数据用于分析** - 使用网页爬虫获取数据
- **API数据收集和处理** - 自动化数据收集流程
- **网站内容监控** - 定期检查网站内容变化

### 🤖 系统管理场景
- **监控系统资源使用** - 使用系统监控器跟踪性能
- **自动化系统维护** - 定时执行系统维护任务
- **日志分析和报告** - 自动化日志处理和分析

### 🛠️ 开发辅助场景
- **保持代码风格一致** - 使用代码格式化器统一代码风格
- **自动化测试执行** - 批量运行测试和生成报告
- **项目依赖管理** - 检查和更新项目依赖

## 📚 文档导航

### 🐍 Python工具文档
- **[📖 主文档](./python/README.md)** - 完整的工具介绍和使用指南
- **[🚀 快速开始](./python/docs/QUICKSTART.md)** - 5分钟快速上手指南
- **[💡 使用示例](./python/docs/examples.md)** - 详细的使用示例和最佳实践
- **[🧪 测试数据](./python/tests/)** - 各工具的测试文件和示例数据

### 📋 项目文档
- **[📄 许可证](./LICENSE)** - 项目许可证信息
- **[🤝 贡献指南](#贡献指南)** - 如何参与项目开发
- **[📝 更新日志](./CHANGELOG.md)** - 版本更新记录

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
python -c "import pandas, requests, psutil; print('✅ 安装成功！')"
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
```

### 文件管理工作流
```bash
# 1. 批量重命名文件
python file_operations/batch_renamer.py ./photos --name-pattern "photo_{n:03d}{ext}" --execute

# 2. 监控文件变化
python file_operations/file_monitor.py ./project --patterns "*.py" --command "echo {file} changed"
```

### 开发辅助工作流
```bash
# 1. 格式化代码
python dev_tools/code_formatter.py . --recursive

# 2. 检查代码风格
python dev_tools/code_formatter.py . --flake8

# 3. 监控系统资源
python automation/system_monitor.py --once
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