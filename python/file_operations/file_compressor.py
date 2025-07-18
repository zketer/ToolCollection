#!/usr/bin/env python3
"""
文件压缩器

功能：
- 批量压缩文件/目录为zip或tar.gz
- 支持递归压缩、批量压缩
- 支持解压zip/tar.gz到指定目录
- 自动识别压缩/解压模式

作者: ToolCollection
"""
import argparse
import os
import sys
import zipfile
import tarfile
from pathlib import Path


def compress_zip(inputs, output):
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
        for path in inputs:
            path = Path(path)
            if path.is_dir():
                for file in path.rglob('*'):
                    if file.is_file():
                        zf.write(file, file.relative_to(path.parent))
            else:
                zf.write(path, path.name)
    print(f"✅ 已压缩为: {output}")

def compress_tar(inputs, output):
    with tarfile.open(output, 'w:gz') as tf:
        for path in inputs:
            path = Path(path)
            if path.is_dir():
                for file in path.rglob('*'):
                    tf.add(file, arcname=file.relative_to(path.parent))
            else:
                tf.add(path, arcname=path.name)
    print(f"✅ 已压缩为: {output}")

def extract_zip(input_file, output_dir):
    with zipfile.ZipFile(input_file, 'r') as zf:
        zf.extractall(output_dir)
    print(f"✅ 已解压到: {output_dir}")

def extract_tar(input_file, output_dir):
    with tarfile.open(input_file, 'r:gz') as tf:
        tf.extractall(output_dir)
    print(f"✅ 已解压到: {output_dir}")

def main():
    parser = argparse.ArgumentParser(
        description="文件压缩器 - 支持zip/tar.gz压缩与解压，递归、批量、解压到指定目录",
        epilog="""
示例：
  # 压缩文件和目录为zip
  python file_compressor.py compress file1.txt dir1 --output archive.zip
  # 压缩为tar.gz
  python file_compressor.py compress file1.txt dir1 --output archive.tar.gz
  # 解压zip
  python file_compressor.py extract archive.zip --output outdir
  # 解压tar.gz
  python file_compressor.py extract archive.tar.gz --output outdir
        """
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # 压缩
    p_compress = subparsers.add_parser('compress', help='压缩文件/目录')
    p_compress.add_argument('inputs', nargs='+', help='待压缩的文件或目录')
    p_compress.add_argument('--output', required=True, help='输出文件名（.zip或.tar.gz）')

    # 解压
    p_extract = subparsers.add_parser('extract', help='解压文件')
    p_extract.add_argument('input', help='待解压的zip或tar.gz文件')
    p_extract.add_argument('--output', default='.', help='解压到的目录')

    args = parser.parse_args()

    if args.command == 'compress':
        if args.output.endswith('.zip'):
            compress_zip(args.inputs, args.output)
        elif args.output.endswith('.tar.gz'):
            compress_tar(args.inputs, args.output)
        else:
            print('❌ 仅支持输出为 .zip 或 .tar.gz')
            sys.exit(1)
    elif args.command == 'extract':
        if args.input.endswith('.zip'):
            extract_zip(args.input, args.output)
        elif args.input.endswith('.tar.gz'):
            extract_tar(args.input, args.output)
        else:
            print('❌ 仅支持解压 .zip 或 .tar.gz 文件')
            sys.exit(1)

if __name__ == "__main__":
    main() 