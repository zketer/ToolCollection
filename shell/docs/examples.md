# 使用示例 📚

这里提供了一些常用 Shell 工具的使用示例，帮助你快速上手。

## CSV 快速查看
```bash
# 显示前10行
./data_processing/csv_parser.sh data.csv --head 10

# 只显示第2列
./data_processing/csv_parser.sh data.csv --col 2
```

## 批量重命名文件
```bash
# 批量重命名并加前缀
./file_operations/batch_rename.sh ./photos --prefix img_ --number
```

## 端口扫描
```bash
# 扫描本机常用端口
./web_tools/port_scanner.sh 127.0.0.1 --ports 1-1000
```

## 日志清理
```bash
# 清理7天前日志
./automation/log_cleaner.sh ./logs --days 7
```

## 目录同步
```bash
# 同步 src 到 dst，目标多余文件会被删除
./file_operations/dir_sync.sh ./src ./dst --delete
```

## 批量下载
```bash
# 从 url_list.txt 批量下载到 downloads 目录
./automation/batch_downloader.sh url_list.txt --dir downloads
```

## 组合用法
```bash
# 先批量重命名，再同步到备份目录
./file_operations/batch_rename.sh ./photos --prefix img_ --number
./file_operations/dir_sync.sh ./photos ./backup_photos

# 端口扫描+进程查杀
./web_tools/port_scanner.sh 127.0.0.1 --ports 8000-9000
./dev_tools/port_killer.sh 8080
```

## 常见问题排查
```bash
# 查看帮助
./data_processing/csv_parser.sh --help
./file_operations/batch_rename.sh --help
./web_tools/port_scanner.sh --help
```

---

**提示**: 所有脚本均支持 `--help` 参数查看详细用法！ 