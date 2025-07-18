# 使用示例 📚

这里提供了一些常用工具的使用示例，帮助你快速上手。

## CSV处理器使用示例

### 基本用法
```bash
# 处理CSV文件并显示摘要
python data_processing/csv_processor.py data.csv --summary

# 清洗数据（删除重复行，填充空值）
python data_processing/csv_processor.py data.csv --clean

# 按指定列排序
python data_processing/csv_processor.py data.csv --sort name age

# 过滤数据
python data_processing/csv_processor.py data.csv --filter status active --filter age 25

# 重命名列
python data_processing/csv_processor.py data.csv --rename old_name new_name --rename old_age new_age

# 指定输出文件
python data_processing/csv_processor.py data.csv -o processed_data.csv
```

### 组合使用
```bash
# 清洗数据 + 排序 + 过滤 + 重命名
python data_processing/csv_processor.py data.csv \
    --clean \
    --sort name \
    --filter status active \
    --rename old_name new_name \
    -o final_data.csv \
    --summary
```

## 批量重命名器使用示例

### 基本用法
```bash
# 预览重命名结果（不实际执行）
python file_operations/batch_renamer.py ./photos

# 使用序号重命名
python file_operations/batch_renamer.py ./photos --name-pattern "photo_{n:03d}{ext}" --execute

# 添加前缀
python file_operations/batch_renamer.py ./photos --prefix "vacation_" --execute

# 添加后缀
python file_operations/batch_renamer.py ./photos --suffix "_2024" --execute

# 转换为小写
python file_operations/batch_renamer.py ./photos --case lower --execute
```

### 高级用法
```bash
# 使用正则表达式重命名
python file_operations/batch_renamer.py ./files --pattern-rename "IMG_(\d+)" "photo_$1" --execute

# 递归处理子目录
python file_operations/batch_renamer.py ./photos -r --name-pattern "photo_{n}{ext}" --execute

# 只处理特定文件类型
python file_operations/batch_renamer.py ./photos -p "*.jpg" --name-pattern "image_{n}{ext}" --execute
```

## 网页爬虫使用示例

### 基本用法
```bash
# 抓取网页基本信息
python web_tools/web_crawler.py https://example.com

# 提取所有链接
python web_tools/web_crawler.py https://example.com --extract-links

# 提取所有图片
python web_tools/web_crawler.py https://example.com --extract-images

# 保存为CSV格式
python web_tools/web_crawler.py https://example.com -f csv -o data.csv
```

### 自定义选择器
```bash
# 提取特定元素
python web_tools/web_crawler.py https://example.com \
    -s title "h1" \
    -s price ".price" \
    -s description ".description" \
    -o products.json

# 提取属性
python web_tools/web_crawler.py https://example.com \
    -s image_url "attr:img[src]" \
    -s link_url "attr:a[href]" \
    -o links.json
```

### 高级配置
```bash
# 自定义User-Agent和延迟
python web_tools/web_crawler.py https://example.com \
    --user-agent "MyBot/1.0" \
    --delay 2.0 \
    --extract-links \
    -o links.json
```

## 系统监控器使用示例

### 基本用法
```bash
# 监控一次系统状态
python automation/system_monitor.py --once

# 持续监控，每10秒一次
python automation/system_monitor.py -i 10

# 监控30秒后停止
python automation/system_monitor.py -d 30

# 保存为CSV格式
python automation/system_monitor.py --once -f csv -o system_status.csv
```

## 代码格式化器使用示例

### 基本用法
```bash
# 检查单个文件格式
python dev_tools/code_formatter.py myfile.py --check

# 格式化单个文件
python dev_tools/code_formatter.py myfile.py

# 递归格式化整个目录
python dev_tools/code_formatter.py . --recursive

# 运行Flake8代码风格检查
python dev_tools/code_formatter.py . --flake8

# 同时格式化和检查
python dev_tools/code_formatter.py . --recursive --flake8
```

## 实际应用场景

### 数据处理工作流
```bash
# 1. 抓取网页数据
python web_tools/web_crawler.py https://example.com/products \
    -s title "h2.product-title" \
    -s price ".product-price" \
    -s url "attr:a[href]" \
    -o products_raw.json

# 2. 转换为CSV格式（手动或使用其他工具）

# 3. 处理CSV数据
python data_processing/csv_processor.py products.csv \
    --clean \
    --sort price \
    --filter status available \
    -o products_processed.csv \
    --summary
```

### 文件整理工作流
```bash
# 1. 批量重命名照片
python file_operations/batch_renamer.py ./vacation_photos \
    --name-pattern "vacation_{n:03d}{ext}" \
    --execute

# 2. 添加日期前缀
python file_operations/batch_renamer.py ./vacation_photos \
    --prefix "2024_01_15_" \
    --execute
```

## 注意事项

1. **备份重要文件**: 在执行重命名操作前，建议备份重要文件
2. **测试小数据集**: 先用小数据集测试工具功能
3. **检查输出**: 使用 `--preview` 或 `--summary` 参数检查结果
4. **网络爬虫礼仪**: 设置适当的延迟时间，避免对服务器造成压力
5. **数据验证**: 处理后的数据要验证其正确性

## 故障排除

### 常见问题

1. **权限错误**: 确保对目标目录有读写权限
2. **编码问题**: 处理中文文件时注意编码设置
3. **网络超时**: 增加超时时间或检查网络连接
4. **内存不足**: 处理大文件时考虑分批处理

### 获取帮助
```bash
# 查看工具帮助
python data_processing/csv_processor.py --help
python file_operations/batch_renamer.py --help
python web_tools/web_crawler.py --help
```

## 🧪 测试数据目录规范
- 每种工具类型目录下有 `tests/` 子目录，包含该类型所有工具的测试数据和测试脚本。
- 例如：
  - `data_processing/tests/test_data.csv`
  - `data_processing/tests/test_data.json`
  - `file_operations/tests/photo1.jpg`
  - `web_tools/tests/test_crawl.json`
- 新增工具时，请将相关测试数据和测试脚本放入对应类型的 `tests/` 子目录。

## 示例命令
```bash
python data_processing/csv_processor.py data_processing/tests/test_data.csv --summary
python data_processing/json_processor.py data_processing/tests/test_data.json --format
``` 