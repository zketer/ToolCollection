#!/usr/bin/env python3
"""
数据库管理器 - 数据库连接、查询、备份工具

功能:
- 支持多种数据库类型 (SQLite, MySQL, PostgreSQL)
- 执行SQL查询和批量操作
- 数据库备份和恢复
- 表结构分析和优化
- 数据导入导出

作者: ToolCollection
版本: 1.0.0
"""

import argparse
import json
import sqlite3
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd

try:
    import mysql.connector
    import psycopg2
    HAS_ADVANCED_DB = True
except ImportError:
    HAS_ADVANCED_DB = False


class DatabaseManager:
    """数据库管理器类"""
    
    def __init__(self, db_type: str = 'sqlite', **kwargs):
        """
        初始化数据库管理器
        
        Args:
            db_type: 数据库类型 ('sqlite', 'mysql', 'postgresql')
            **kwargs: 数据库连接参数
        """
        self.db_type = db_type.lower()
        self.connection = None
        self.connection_params = kwargs
        
    def connect(self) -> bool:
        """连接到数据库"""
        try:
            if self.db_type == 'sqlite':
                db_path = self.connection_params.get('database', ':memory:')
                self.connection = sqlite3.connect(db_path)
                self.connection.row_factory = sqlite3.Row
                
            elif self.db_type == 'mysql' and HAS_ADVANCED_DB:
                self.connection = mysql.connector.connect(**self.connection_params)
                
            elif self.db_type == 'postgresql' and HAS_ADVANCED_DB:
                self.connection = psycopg2.connect(**self.connection_params)
                
            else:
                print(f"❌ 不支持的数据库类型: {self.db_type}")
                if not HAS_ADVANCED_DB:
                    print("💡 安装额外依赖: pip install mysql-connector-python psycopg2-binary")
                return False
                
            print(f"✅ 成功连接到 {self.db_type} 数据库")
            return True
            
        except Exception as e:
            print(f"❌ 连接数据库失败: {e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            print("✅ 数据库连接已关闭")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """执行查询并返回结果"""
        if not self.connection:
            print("❌ 未连接到数据库")
            return []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                columns = [desc[0] for desc in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
            else:
                self.connection.commit()
                return [{"affected_rows": cursor.rowcount}]
                
        except Exception as e:
            print(f"❌ 执行查询失败: {e}")
            return []
    
    def get_tables(self) -> List[str]:
        """获取所有表名"""
        if self.db_type == 'sqlite':
            query = "SELECT name FROM sqlite_master WHERE type='table'"
        elif self.db_type == 'mysql':
            query = "SHOW TABLES"
        elif self.db_type == 'postgresql':
            query = "SELECT tablename FROM pg_tables WHERE schemaname='public'"
        else:
            return []
        
        results = self.execute_query(query)
        if self.db_type == 'mysql':
            return [list(row.values())[0] for row in results]
        else:
            return [row['name'] for row in results]
    
    def get_table_info(self, table_name: str) -> List[Dict]:
        """获取表结构信息"""
        if self.db_type == 'sqlite':
            query = f"PRAGMA table_info({table_name})"
            results = self.execute_query(query)
            return [
                {
                    'column': row['name'],
                    'type': row['type'],
                    'not_null': bool(row['notnull']),
                    'primary_key': bool(row['pk']),
                    'default': row['dflt_value']
                }
                for row in results
            ]
        elif self.db_type == 'mysql':
            query = f"DESCRIBE {table_name}"
            results = self.execute_query(query)
            return [
                {
                    'column': row['Field'],
                    'type': row['Type'],
                    'null': row['Null'],
                    'key': row['Key'],
                    'default': row['Default']
                }
                for row in results
            ]
        elif self.db_type == 'postgresql':
            query = """
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = %s
                ORDER BY ordinal_position
            """
            results = self.execute_query(query, (table_name,))
            return [
                {
                    'column': row['column_name'],
                    'type': row['data_type'],
                    'nullable': row['is_nullable'],
                    'default': row['column_default']
                }
                for row in results
            ]
        return []
    
    def backup_database(self, backup_path: str) -> bool:
        """备份数据库"""
        try:
            if self.db_type == 'sqlite':
                # SQLite备份
                backup_conn = sqlite3.connect(backup_path)
                self.connection.backup(backup_conn)
                backup_conn.close()
                
            elif self.db_type == 'mysql':
                # MySQL备份 (需要mysqldump)
                import subprocess
                cmd = [
                    'mysqldump',
                    f'--host={self.connection_params.get("host", "localhost")}',
                    f'--user={self.connection_params.get("user", "root")}',
                    f'--password={self.connection_params.get("password", "")}',
                    self.connection_params.get('database', ''),
                    '>', backup_path
                ]
                subprocess.run(' '.join(cmd), shell=True)
                
            elif self.db_type == 'postgresql':
                # PostgreSQL备份 (需要pg_dump)
                import subprocess
                cmd = [
                    'pg_dump',
                    f'--host={self.connection_params.get("host", "localhost")}',
                    f'--port={self.connection_params.get("port", "5432")}',
                    f'--username={self.connection_params.get("user", "postgres")}',
                    f'--dbname={self.connection_params.get("database", "")}',
                    '>', backup_path
                ]
                subprocess.run(' '.join(cmd), shell=True)
            
            print(f"✅ 数据库已备份到: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ 备份失败: {e}")
            return False
    
    def import_data(self, table_name: str, data: List[Dict], mode: str = 'insert') -> bool:
        """导入数据到表"""
        if not data:
            print("❌ 没有数据可导入")
            return False
        
        try:
            columns = list(data[0].keys())
            placeholders = ', '.join(['?' if self.db_type == 'sqlite' else '%s'] * len(columns))
            column_names = ', '.join(columns)
            
            if mode == 'insert':
                query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
            elif mode == 'replace':
                query = f"REPLACE INTO {table_name} ({column_names}) VALUES ({placeholders})"
            else:
                print(f"❌ 不支持的导入模式: {mode}")
                return False
            
            cursor = self.connection.cursor()
            values = [tuple(row.values()) for row in data]
            cursor.executemany(query, values)
            self.connection.commit()
            
            print(f"✅ 成功导入 {len(data)} 条数据到表 {table_name}")
            return True
            
        except Exception as e:
            print(f"❌ 导入数据失败: {e}")
            return False
    
    def export_data(self, table_name: str, output_path: str, format: str = 'csv') -> bool:
        """导出表数据"""
        try:
            query = f"SELECT * FROM {table_name}"
            results = self.execute_query(query)
            
            if not results:
                print(f"❌ 表 {table_name} 没有数据")
                return False
            
            df = pd.DataFrame(results)
            
            if format.lower() == 'csv':
                df.to_csv(output_path, index=False)
            elif format.lower() == 'json':
                df.to_json(output_path, orient='records', indent=2)
            elif format.lower() == 'excel':
                df.to_excel(output_path, index=False)
            else:
                print(f"❌ 不支持的导出格式: {format}")
                return False
            
            print(f"✅ 数据已导出到: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ 导出数据失败: {e}")
            return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="数据库管理器 - 数据库连接、查询、备份工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 连接SQLite数据库
  python database_manager.py --type sqlite --database test.db --info
  
  # 执行查询
  python database_manager.py --type sqlite --database test.db --query "SELECT * FROM users"
  
  # 获取表结构
  python database_manager.py --type sqlite --database test.db --table-info users
  
  # 备份数据库
  python database_manager.py --type sqlite --database test.db --backup backup.db
  
  # 导入数据
  python database_manager.py --type sqlite --database test.db --import users data.json
  
  # 导出数据
  python database_manager.py --type sqlite --database test.db --export users --output users.csv
        """
    )
    
    # 数据库连接参数
    parser.add_argument('--type', choices=['sqlite', 'mysql', 'postgresql'], 
                       default='sqlite', help='数据库类型')
    parser.add_argument('--database', help='数据库名称或文件路径')
    parser.add_argument('--host', default='localhost', help='数据库主机')
    parser.add_argument('--port', type=int, help='数据库端口')
    parser.add_argument('--user', help='数据库用户名')
    parser.add_argument('--password', help='数据库密码')
    
    # 操作参数
    parser.add_argument('--info', action='store_true', help='显示数据库信息')
    parser.add_argument('--query', help='执行SQL查询')
    parser.add_argument('--table-info', help='获取指定表的结构信息')
    parser.add_argument('--backup', help='备份数据库到指定路径')
    parser.add_argument('--import', dest='import_table', help='导入数据到指定表')
    parser.add_argument('--import-file', help='导入数据文件路径')
    parser.add_argument('--import-mode', choices=['insert', 'replace'], 
                       default='insert', help='导入模式')
    parser.add_argument('--export', help='导出指定表的数据')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--format', choices=['csv', 'json', 'excel'], 
                       default='csv', help='导出格式')
    
    args = parser.parse_args()
    
    # 构建连接参数
    connection_params = {}
    if args.type == 'sqlite':
        connection_params['database'] = args.database or ':memory:'
    else:
        connection_params.update({
            'host': args.host,
            'port': args.port,
            'user': args.user,
            'password': args.password,
            'database': args.database
        })
    
    # 创建数据库管理器
    db_manager = DatabaseManager(args.type, **connection_params)
    
    # 连接数据库
    if not db_manager.connect():
        sys.exit(1)
    
    try:
        # 执行操作
        if args.info:
            print("\n📊 数据库信息:")
            print(f"类型: {args.type}")
            tables = db_manager.get_tables()
            print(f"表数量: {len(tables)}")
            if tables:
                print(f"表名: {', '.join(tables)}")
                
                # 显示每个表的基本信息
                for table in tables[:5]:  # 只显示前5个表
                    info = db_manager.get_table_info(table)
                    print(f"\n表 {table}:")
                    print(f"  列数: {len(info)}")
                    for col in info[:3]:  # 只显示前3列
                        print(f"  - {col['column']}: {col['type']}")
                    if len(info) > 3:
                        print(f"  ... 还有 {len(info) - 3} 列")
        
        elif args.query:
            print(f"\n🔍 执行查询: {args.query}")
            results = db_manager.execute_query(args.query)
            if results:
                print(f"✅ 查询成功，返回 {len(results)} 条记录")
                if len(results) <= 10:
                    for i, row in enumerate(results, 1):
                        print(f"  {i}. {row}")
                else:
                    print("  (显示前10条记录)")
                    for i, row in enumerate(results[:10], 1):
                        print(f"  {i}. {row}")
                    print(f"  ... 还有 {len(results) - 10} 条记录")
            else:
                print("✅ 查询执行完成，无返回数据")
        
        elif args.table_info:
            print(f"\n📋 表 {args.table_info} 结构:")
            info = db_manager.get_table_info(args.table_info)
            if info:
                for col in info:
                    print(f"  - {col['column']}: {col['type']}")
                    if 'not_null' in col and col['not_null']:
                        print("    NOT NULL")
                    if 'primary_key' in col and col['primary_key']:
                        print("    PRIMARY KEY")
            else:
                print(f"❌ 表 {args.table_info} 不存在或无法获取结构信息")
        
        elif args.backup:
            print(f"\n💾 备份数据库到: {args.backup}")
            db_manager.backup_database(args.backup)
        
        elif args.import_table:
            if not args.import_file:
                print("❌ 请指定导入文件路径 (--import-file)")
                sys.exit(1)
            
            print(f"\n📥 导入数据到表 {args.import_table}")
            
            # 读取数据文件
            if args.import_file.endswith('.json'):
                with open(args.import_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            elif args.import_file.endswith('.csv'):
                data = pd.read_csv(args.import_file).to_dict('records')
            else:
                print(f"❌ 不支持的文件格式: {args.import_file}")
                sys.exit(1)
            
            db_manager.import_data(args.import_table, data, args.import_mode)
        
        elif args.export:
            if not args.output:
                print("❌ 请指定输出文件路径 (--output)")
                sys.exit(1)
            
            print(f"\n📤 导出表 {args.export} 数据")
            db_manager.export_data(args.export, args.output, args.format)
        
        else:
            print("💡 使用 --help 查看使用说明")
    
    finally:
        db_manager.disconnect()


if __name__ == "__main__":
    main() 