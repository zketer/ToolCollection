# 快速开始指南 🚀

本指南将帮助你在5分钟内开始使用 ToolCollection 的 Shell 工具。

## 1. 环境准备

### 赋予脚本可执行权限
```bash
# 进入 shell 目录
cd shell

# 赋予所有脚本可执行权限
find . -type f -name "*.sh" -exec chmod +x {} \;
```

### 检查依赖
部分脚本依赖常用命令行工具（如 jq、curl、rsync、inotifywait、fswatch、md5sum、sha1sum、zip、unzip 等），如未安装请先通过包管理器安装。

## 2. 目录结构说明
- 每种工具类型有独立子目录（data_processing、file_operations、web_tools、automation、dev_tools）
- 每个脚本自带 --help 参数，查看详细用法

## 3. 快速体验示例

### 数据处理 - CSV 快速查看
```bash
# 查看 CSV 文件前10行
./data_processing/csv_parser.sh data.csv --head 10
```

### 文件操作 - 批量重命名
```bash
# 批量重命名文件
./file_operations/batch_rename.sh ./photos --prefix img_ --number
```

### Web 工具 - 端口扫描
```bash
# 扫描本机 1-1000 端口
./web_tools/port_scanner.sh 127.0.0.1 --ports 1-1000
```

### 自动化 - 日志清理
```bash
# 清理7天前日志并归档
./automation/log_cleaner.sh ./logs --days 7 --archive
```

### 开发工具 - 系统信息
```bash
# 查看系统信息
./dev_tools/sys_info.sh
```

## 4. 常用工作流

### 目录同步
```bash
./file_operations/dir_sync.sh ./src ./dst --delete
```

### 定时自动备份
```bash
./automation/auto_backup.sh ./data ./backup --interval 60
```

## 5. 故障排查

- **权限不足**：请确保脚本有执行权限 `chmod +x script.sh`
- **命令未找到**：请安装缺失的依赖工具
- **参数错误**：使用 `--help` 查看脚本用法

---

**提示**: 所有脚本均支持 `--help` 参数查看详细用法！ 