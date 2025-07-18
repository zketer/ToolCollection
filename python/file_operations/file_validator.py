#!/usr/bin/env python3
"""
文件校验器

功能：
- 文件完整性校验（MD5/SHA1/SHA256）
- 支持校验和生成与校验
- 支持批量校验

作者: ToolCollection
"""
import argparse
import sys
import hashlib
from pathlib import Path


def calc_hash(file_path, algorithm):
    h = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def generate_checksums(files, algorithm, output):
    with open(output, 'w', encoding='utf-8') as out:
        for file in files:
            hashval = calc_hash(file, algorithm)
            out.write(f"{hashval}  {file}\n")
            print(f"{file}: {hashval}")
    print(f"✅ 校验和已保存到: {output}")

def verify_checksums(checksum_file, algorithm):
    ok, fail = 0, 0
    with open(checksum_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            hashval, file = line.strip().split(None, 1)
            file = file.strip()
            if not Path(file).exists():
                print(f"❌ 文件不存在: {file}")
                fail += 1
                continue
            actual = calc_hash(file, algorithm)
            if actual == hashval:
                print(f"✅ {file} 校验通过")
                ok += 1
            else:
                print(f"❌ {file} 校验失败 (期望: {hashval}, 实际: {actual})")
                fail += 1
    print(f"共校验 {ok+fail} 个文件，成功 {ok}，失败 {fail}")

def main():
    parser = argparse.ArgumentParser(
        description="文件校验器 - 支持MD5/SHA1/SHA256校验，批量校验和生成",
        epilog="""
示例：
  # 生成校验和
  python file_validator.py generate file1.txt file2.txt --algorithm md5 --output files.md5
  # 校验
  python file_validator.py verify files.md5 --algorithm md5
        """
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # 生成校验和
    p_gen = subparsers.add_parser('generate', help='生成校验和')
    p_gen.add_argument('files', nargs='+', help='待校验的文件')
    p_gen.add_argument('--algorithm', choices=['md5', 'sha1', 'sha256'], default='md5', help='校验算法')
    p_gen.add_argument('--output', required=True, help='输出校验和文件')

    # 校验
    p_ver = subparsers.add_parser('verify', help='校验文件')
    p_ver.add_argument('checksum_file', help='校验和文件')
    p_ver.add_argument('--algorithm', choices=['md5', 'sha1', 'sha256'], default='md5', help='校验算法')

    args = parser.parse_args()

    if args.command == 'generate':
        generate_checksums(args.files, args.algorithm, args.output)
    elif args.command == 'verify':
        verify_checksums(args.checksum_file, args.algorithm)

if __name__ == "__main__":
    main() 