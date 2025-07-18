#!/usr/bin/env python3
"""
文件加密器

功能：
- 文件加密、解密（对称加密，AES）
- 支持密码
- 支持加密/解密单文件

作者: ToolCollection
"""
import argparse
import sys
import os
from pathlib import Path
from getpass import getpass
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

BLOCK_SIZE = 16
SALT_SIZE = 16
KEY_SIZE = 32


def pad(data):
    pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError('解密失败，填充无效')
    return data[:-pad_len]

def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=KEY_SIZE, count=100_000)

def encrypt_file(input_file, output_file, password):
    salt = get_random_bytes(SALT_SIZE)
    key = derive_key(password.encode(), salt)
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    ciphertext = cipher.encrypt(pad(plaintext))
    with open(output_file, 'wb') as f:
        f.write(salt + iv + ciphertext)
    print(f"✅ 已加密: {input_file} -> {output_file}")

def decrypt_file(input_file, output_file, password):
    with open(input_file, 'rb') as f:
        salt = f.read(SALT_SIZE)
        iv = f.read(BLOCK_SIZE)
        ciphertext = f.read()
    key = derive_key(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        plaintext = unpad(cipher.decrypt(ciphertext))
    except Exception as e:
        print(f"❌ 解密失败: {e}")
        sys.exit(1)
    with open(output_file, 'wb') as f:
        f.write(plaintext)
    print(f"✅ 已解密: {input_file} -> {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="文件加密器 - 文件加密/解密（AES对称加密，支持密码）",
        epilog="""
示例：
  # 加密
  python file_encryptor.py encrypt file.txt --output file.enc
  # 解密
  python file_encryptor.py decrypt file.enc --output file.txt
        """
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # 加密
    p_encrypt = subparsers.add_parser('encrypt', help='加密文件')
    p_encrypt.add_argument('input', help='待加密的文件')
    p_encrypt.add_argument('--output', required=True, help='输出加密文件')
    p_encrypt.add_argument('--password', help='加密密码（不建议明文，建议留空交互输入）')

    # 解密
    p_decrypt = subparsers.add_parser('decrypt', help='解密文件')
    p_decrypt.add_argument('input', help='待解密的文件')
    p_decrypt.add_argument('--output', required=True, help='输出解密文件')
    p_decrypt.add_argument('--password', help='解密密码（不建议明文，建议留空交互输入）')

    args = parser.parse_args()

    if args.command == 'encrypt':
        password = args.password or getpass('请输入加密密码: ')
        encrypt_file(args.input, args.output, password)
    elif args.command == 'decrypt':
        password = args.password or getpass('请输入解密密码: ')
        decrypt_file(args.input, args.output, password)

if __name__ == "__main__":
    main() 