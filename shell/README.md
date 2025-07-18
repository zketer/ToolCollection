# Shell 工具集

本目录收录常用 Bash/Shell 脚本工具，适用于日常开发、运维、数据处理等场景。

## 工具类型导航

- [数据处理（data_processing）](./data_processing/)
- [文件操作（file_operations）](./file_operations/)
- [Web 工具（web_tools）](./web_tools/)
- [自动化脚本（automation）](./automation/)
- [开发者工具（dev_tools）](./dev_tools/)

---

## 工具列表

### 数据处理（data_processing）
- **csv_parser.sh**       - CSV 文件快速查看/筛选，支持按行/列输出
- **json_prettify.sh**    - JSON 格式化与校验，依赖 jq
- **text_stats.sh**       - 文本统计（行、词、字符）
- **column_extractor.sh** - 提取文本/CSV 指定列，支持自定义分隔符
- **data_cleaner.sh**     - 批量去重/去空/标准化，支持多种处理选项
- **data_merger.sh**      - 多文件合并去重，支持合并后去重
- **text_filter.sh**      - 文本内容筛选，支持关键字/正则/包含排除
- **text_transform.sh**   - 文本批量大小写/替换/去重等转换

### 文件操作（file_operations）
- **batch_rename.sh**     - 批量文件重命名，支持前缀/后缀/正则/序号
- **file_finder.sh**      - 多条件查找文件，支持按名/扩展名/大小筛选
- **file_compressor.sh**  - 批量压缩/解压，支持 zip/unzip
- **file_splitter.sh**    - 大文件分割，支持自定义行数和前缀
- **file_merger.sh**      - 文件合并，支持多文件顺序合并
- **dir_sync.sh**         - 目录同步，支持 rsync 和可选删除
- **file_hasher.sh**      - 文件哈希计算，支持 md5/sha1/sha256
- **dir_size.sh**         - 目录空间统计，显示各子目录占用
- **empty_finder.sh**     - 查找空文件和空目录

### Web 工具（web_tools）
- **url_checker.sh**      - 批量检测 URL 可用性，输出 HTTP 状态码
- **dns_lookup.sh**       - 批量 DNS 查询，支持 A/MX/TXT 等类型
- **http_request.sh**     - 命令行 HTTP 请求，支持多方法/自定义头/数据
- **ip_info.sh**          - IP 归属地查询，支持单个或批量
- **port_scanner.sh**     - 端口扫描，支持自定义端口范围
- **proxy_checker.sh**    - 代理可用性检测，支持自定义测试 URL

### 自动化脚本（automation）
- **log_cleaner.sh**      - 日志清理与归档，支持按天/大小清理
- **backup_dir.sh**       - 目录自动压缩备份，保留最近N份
- **batch_downloader.sh** - 批量下载工具，支持自定义目录
- **file_watcher.sh**     - 目录变动监控，支持 inotifywait/fswatch
- **cron_helper.sh**      - 定时任务生成与管理，支持增删查
- **auto_updater.sh**     - 自动拉取/更新代码，支持 git pull
- **notify.sh**           - 跨平台消息通知，支持 macOS/Linux
- **auto_backup.sh**      - 定时自动备份，支持自定义间隔
- **auto_cleaner.sh**     - 定时自动清理目录/文件，支持多条件
- **auto_report.sh**      - 定时自动生成目录/文件报告

### 开发者工具（dev_tools）
- **sys_info.sh**         - 系统信息一键查看
- **port_killer.sh**      - 一键查杀指定端口进程
- **net_speed_test.sh**   - 网络测速，curl或speedtest-cli
- **env_diff.sh**         - 环境变量对比，支持 .env 文件
- **process_monitor.sh**  - 进程监控，支持自定义间隔
- **docker_cleaner.sh**   - 一键清理 Docker 残留，支持全量/部分
- **git_helper.sh**       - 常用 Git 操作封装，支持状态/拉取/推送/日志
- **port_usage.sh**       - 端口占用查询，显示占用进程
- **env_exporter.sh**     - 环境变量导出为 .env 文件

> 所有脚本均可直接运行，支持 --help 查看用法。

---

## 示例用法

```bash
# 查看系统信息
./dev_tools/sys_info.sh

# 批量重命名
./file_operations/batch_rename.sh ./photos --prefix img_ --number

# 日志清理并归档
./automation/log_cleaner.sh ./logs --days 7 --archive

# 查杀端口
./dev_tools/port_killer.sh 8080

# 网络测速
./dev_tools/net_speed_test.sh

# 目录备份，保留最近3份
./automation/backup_dir.sh ./data --keep 3
``` 