#!/bin/bash
# 激活Python虚拟环境脚本

echo "正在激活Python虚拟环境..."
source venv/bin/activate
echo "虚拟环境已激活！"
echo "现在可以使用以下命令："
echo "  python data_processing/csv_processor.py --help"
echo "  python file_operations/batch_renamer.py --help"
echo "  python web_tools/web_crawler.py --help"
echo ""
echo "要退出虚拟环境，请运行: deactivate" 