#!/usr/bin/env python3
"""
代码生成器 - 代码模板生成、脚手架工具

功能:
- 多种项目模板 (Web应用、CLI工具、API服务等)
- 自定义模板支持
- 变量替换和条件生成
- 项目结构自动创建
- 依赖管理集成

作者: ToolCollection
版本: 1.0.0
"""

import argparse
import json
import os
import sys
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import re


class CodeGenerator:
    """代码生成器类"""
    
    def __init__(self, templates_dir: str = None):
        """
        初始化代码生成器
        
        Args:
            templates_dir: 模板目录路径
        """
        self.templates_dir = templates_dir or os.path.join(
            os.path.dirname(__file__), 'templates'
        )
        self.builtin_templates = {
            'web-app': {
                'name': 'Web应用',
                'description': 'Flask/Django Web应用模板',
                'files': [
                    'app.py',
                    'templates/index.html',
                    'static/css/style.css',
                    'static/js/main.js',
                    'requirements.txt',
                    'README.md'
                ]
            },
            'cli-tool': {
                'name': 'CLI工具',
                'description': '命令行工具模板',
                'files': [
                    'main.py',
                    'cli.py',
                    'utils.py',
                    'requirements.txt',
                    'README.md',
                    'setup.py'
                ]
            },
            'api-service': {
                'name': 'API服务',
                'description': 'RESTful API服务模板',
                'files': [
                    'app.py',
                    'models.py',
                    'routes.py',
                    'config.py',
                    'requirements.txt',
                    'README.md'
                ]
            },
            'data-analysis': {
                'name': '数据分析项目',
                'description': '数据分析项目模板',
                'files': [
                    'main.py',
                    'data_processor.py',
                    'visualization.py',
                    'requirements.txt',
                    'README.md',
                    'notebooks/analysis.ipynb'
                ]
            },
            'package': {
                'name': 'Python包',
                'description': 'Python包开发模板',
                'files': [
                    'src/__init__.py',
                    'src/main.py',
                    'tests/__init__.py',
                    'tests/test_main.py',
                    'requirements.txt',
                    'setup.py',
                    'README.md',
                    'pyproject.toml'
                ]
            }
        }
    
    def list_templates(self) -> None:
        """列出可用模板"""
        print("📋 可用模板:")
        print()
        
        for template_id, template_info in self.builtin_templates.items():
            print(f"🔹 {template_id}")
            print(f"   名称: {template_info['name']}")
            print(f"   描述: {template_info['description']}")
            print(f"   文件: {len(template_info['files'])} 个")
            print()
        
        # 检查自定义模板
        if os.path.exists(self.templates_dir):
            custom_templates = [d for d in os.listdir(self.templates_dir) 
                              if os.path.isdir(os.path.join(self.templates_dir, d))]
            if custom_templates:
                print("📁 自定义模板:")
                for template in custom_templates:
                    print(f"  - {template}")
    
    def get_template_info(self, template_id: str) -> Optional[Dict]:
        """获取模板信息"""
        if template_id in self.builtin_templates:
            return self.builtin_templates[template_id]
        
        # 检查自定义模板
        custom_template_path = os.path.join(self.templates_dir, template_id)
        if os.path.exists(custom_template_path):
            config_file = os.path.join(custom_template_path, 'template.json')
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except:
                    pass
        
        return None
    
    def generate_project(self, template_id: str, project_name: str, 
                        output_dir: str = None, variables: Dict = None) -> bool:
        """
        生成项目
        
        Args:
            template_id: 模板ID
            project_name: 项目名称
            output_dir: 输出目录
            variables: 变量替换字典
            
        Returns:
            是否成功
        """
        template_info = self.get_template_info(template_id)
        if not template_info:
            print(f"❌ 模板 '{template_id}' 不存在")
            return False
        
        # 设置输出目录
        if not output_dir:
            output_dir = os.path.join(os.getcwd(), project_name)
        
        # 检查输出目录
        if os.path.exists(output_dir):
            print(f"❌ 输出目录已存在: {output_dir}")
            return False
        
        # 设置默认变量
        default_vars = {
            'project_name': project_name,
            'author': os.getenv('USER', 'Unknown'),
            'email': f"{os.getenv('USER', 'user')}@example.com",
            'year': datetime.now().year,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'description': f'A {template_info["name"]} project',
            'version': '0.1.0'
        }
        
        if variables:
            default_vars.update(variables)
        
        print(f"🚀 生成项目: {project_name}")
        print(f"   模板: {template_info['name']}")
        print(f"   输出目录: {output_dir}")
        
        try:
            # 创建输出目录
            os.makedirs(output_dir, exist_ok=True)
            
            # 生成文件
            if template_id in self.builtin_templates:
                self._generate_builtin_template(template_id, output_dir, default_vars)
            else:
                self._generate_custom_template(template_id, output_dir, default_vars)
            
            print(f"✅ 项目生成完成: {output_dir}")
            return True
            
        except Exception as e:
            print(f"❌ 生成项目失败: {e}")
            # 清理已创建的目录
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            return False
    
    def _generate_builtin_template(self, template_id: str, output_dir: str, variables: Dict):
        """生成内置模板"""
        template_info = self.builtin_templates[template_id]
        
        for file_path in template_info['files']:
            # 替换变量
            file_path = self._replace_variables(file_path, variables)
            
            # 创建目录
            full_path = os.path.join(output_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # 生成文件内容
            content = self._get_template_content(template_id, file_path, variables)
            
            # 写入文件
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  📄 创建: {file_path}")
    
    def _generate_custom_template(self, template_id: str, output_dir: str, variables: Dict):
        """生成自定义模板"""
        template_path = os.path.join(self.templates_dir, template_id)
        
        for root, dirs, files in os.walk(template_path):
            # 计算相对路径
            rel_path = os.path.relpath(root, template_path)
            
            # 创建目录
            if rel_path != '.':
                target_dir = os.path.join(output_dir, rel_path)
                os.makedirs(target_dir, exist_ok=True)
            
            # 处理文件
            for file in files:
                if file == 'template.json':
                    continue
                
                src_file = os.path.join(root, file)
                rel_file = os.path.join(rel_path, file) if rel_path != '.' else file
                
                # 替换变量
                rel_file = self._replace_variables(rel_file, variables)
                target_file = os.path.join(output_dir, rel_file)
                
                # 读取并处理文件内容
                with open(src_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content = self._replace_variables(content, variables)
                
                # 写入文件
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  📄 创建: {rel_file}")
    
    def _get_template_content(self, template_id: str, file_path: str, variables: Dict) -> str:
        """获取模板文件内容"""
        if template_id == 'web-app':
            return self._get_web_app_content(file_path, variables)
        elif template_id == 'cli-tool':
            return self._get_cli_tool_content(file_path, variables)
        elif template_id == 'api-service':
            return self._get_api_service_content(file_path, variables)
        elif template_id == 'data-analysis':
            return self._get_data_analysis_content(file_path, variables)
        elif template_id == 'package':
            return self._get_package_content(file_path, variables)
        else:
            return ""
    
    def _get_web_app_content(self, file_path: str, variables: Dict) -> str:
        """获取Web应用模板内容"""
        if file_path == 'app.py':
            return f'''#!/usr/bin/env python3
"""
{variables['project_name']} - {variables['description']}

作者: {variables['author']}
版本: {variables['version']}
"""

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/hello')
def hello():
    return jsonify({{"message": "Hello, World!"}})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
        
        elif file_path == 'templates/index.html':
            return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{variables['project_name']}</title>
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/style.css') }}}}">
</head>
<body>
    <div class="container">
        <h1>欢迎使用 {variables['project_name']}</h1>
        <p>这是一个Flask Web应用模板</p>
        <button id="hello-btn">点击测试API</button>
        <div id="result"></div>
    </div>
    
    <script src="{{{{ url_for('static', filename='js/main.js') }}}}"></script>
</body>
</html>
'''
        
        elif file_path == 'static/css/style.css':
            return '''body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h1 {
    color: #333;
    text-align: center;
}

button {
    background: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    margin: 10px 0;
}

button:hover {
    background: #0056b3;
}

#result {
    margin-top: 20px;
    padding: 10px;
    border-radius: 4px;
}
'''
        
        elif file_path == 'static/js/main.js':
            return '''document.getElementById('hello-btn').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/hello');
        const data = await response.json();
        document.getElementById('result').innerHTML = 
            `<div style="background: #d4edda; color: #155724; padding: 10px; border-radius: 4px;">
                ${data.message}
            </div>`;
    } catch (error) {
        document.getElementById('result').innerHTML = 
            `<div style="background: #f8d7da; color: #721c24; padding: 10px; border-radius: 4px;">
                请求失败: ${error.message}
            </div>`;
    }
});
'''
        
        elif file_path == 'requirements.txt':
            return '''Flask==2.3.3
Werkzeug==2.3.7
'''
        
        elif file_path == 'README.md':
            return f'''# {variables['project_name']}

{variables['description']}

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
python app.py
```

然后在浏览器中访问 http://localhost:5000

## 功能

- 基本的Web页面
- RESTful API示例
- 静态文件支持

## 作者

{variables['author']} - {variables['email']}
'''
        
        return ""
    
    def _get_cli_tool_content(self, file_path: str, variables: Dict) -> str:
        """获取CLI工具模板内容"""
        if file_path == 'main.py':
            return f'''#!/usr/bin/env python3
"""
{variables['project_name']} - {variables['description']}

作者: {variables['author']}
版本: {variables['version']}
"""

from cli import main

if __name__ == '__main__':
    main()
'''
        
        elif file_path == 'cli.py':
            return f'''#!/usr/bin/env python3
"""
CLI接口模块
"""

import argparse
import sys
from utils import process_data

def main():
    parser = argparse.ArgumentParser(
        description="{variables['description']}",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('input', help='输入文件或数据')
    parser.add_argument('-o', '--output', help='输出文件')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    try:
        result = process_data(args.input, args.output, args.verbose)
        print(f"✅ 处理完成: {{result}}")
    except Exception as e:
        print(f"❌ 处理失败: {{e}}")
        sys.exit(1)

if __name__ == '__main__':
    main()
'''
        
        elif file_path == 'utils.py':
            return '''#!/usr/bin/env python3
"""
工具函数模块
"""

def process_data(input_data, output_file=None, verbose=False):
    """
    处理数据
    
    Args:
        input_data: 输入数据
        output_file: 输出文件
        verbose: 是否详细输出
        
    Returns:
        处理结果
    """
    if verbose:
        print(f"处理输入: {input_data}")
    
    # 在这里添加你的处理逻辑
    result = f"处理了: {input_data}"
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        if verbose:
            print(f"结果已保存到: {output_file}")
    
    return result
'''
        
        elif file_path == 'setup.py':
            return f'''#!/usr/bin/env python3
"""
安装脚本
"""

from setuptools import setup, find_packages

setup(
    name="{variables['project_name'].lower().replace(' ', '-')}",
    version="{variables['version']}",
    description="{variables['description']}",
    author="{variables['author']}",
    author_email="{variables['email']}",
    packages=find_packages(),
    install_requires=[
        # 在这里添加依赖
    ],
    entry_points={{
        'console_scripts': [
            '{variables["project_name"].lower().replace(" ", "-")}=main:main',
        ],
    }},
    python_requires='>=3.7',
)
'''
        
        elif file_path == 'requirements.txt':
            return '''# 在这里添加项目依赖
# 例如:
# requests==2.31.0
# pandas==2.0.3
'''
        
        elif file_path == 'README.md':
            return f'''# {variables['project_name']}

{variables['description']}

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python main.py input_data -o output.txt -v
```

或者安装后使用:

```bash
{variables['project_name'].lower().replace(' ', '-')} input_data -o output.txt -v
```

## 参数说明

- `input`: 输入文件或数据
- `-o, --output`: 输出文件 (可选)
- `-v, --verbose`: 详细输出 (可选)

## 作者

{variables['author']} - {variables['email']}
'''
        
        return ""
    
    def _get_api_service_content(self, file_path: str, variables: Dict) -> str:
        """获取API服务模板内容"""
        if file_path == 'app.py':
            return f'''#!/usr/bin/env python3
"""
{variables['project_name']} - {variables['description']}

作者: {variables['author']}
版本: {variables['version']}
"""

from flask import Flask, request, jsonify
from routes import api_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# 注册蓝图
app.register_blueprint(api_bp, url_prefix='/api/v1')

@app.route('/health')
def health_check():
    return jsonify({{"status": "healthy", "service": "{variables['project_name']}"}})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
        
        elif file_path == 'routes.py':
            return '''#!/usr/bin/env python3
"""
API路由模块
"""

from flask import Blueprint, request, jsonify
from models import db, User

api_bp = Blueprint('api', __name__)

@api_bp.route('/users', methods=['GET'])
def get_users():
    """获取用户列表"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@api_bp.route('/users', methods=['POST'])
def create_user():
    """创建用户"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "缺少必要参数"}), 400
    
    user = User(name=data['name'], email=data.get('email', ''))
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取单个用户"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())
'''
        
        elif file_path == 'models.py':
            return '''#!/usr/bin/env python3
"""
数据模型模块
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
'''
        
        elif file_path == 'config.py':
            return '''#!/usr/bin/env python3
"""
配置模块
"""

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
'''
        
        elif file_path == 'requirements.txt':
            return '''Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Werkzeug==2.3.7
'''
        
        elif file_path == 'README.md':
            return f'''# {variables['project_name']}

{variables['description']}

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
python app.py
```

## API端点

- `GET /health` - 健康检查
- `GET /api/v1/users` - 获取用户列表
- `POST /api/v1/users` - 创建用户
- `GET /api/v1/users/<id>` - 获取单个用户

## 示例请求

```bash
# 创建用户
curl -X POST http://localhost:5000/api/v1/users \\
  -H "Content-Type: application/json" \\
  -d '{{"name": "张三", "email": "zhangsan@example.com"}}'

# 获取用户列表
curl http://localhost:5000/api/v1/users
```

## 作者

{variables['author']} - {variables['email']}
'''
        
        return ""
    
    def _get_data_analysis_content(self, file_path: str, variables: Dict) -> str:
        """获取数据分析模板内容"""
        if file_path == 'main.py':
            return f'''#!/usr/bin/env python3
"""
{variables['project_name']} - {variables['description']}

作者: {variables['author']}
版本: {variables['version']}
"""

import pandas as pd
from data_processor import DataProcessor
from visualization import Visualizer

def main():
    # 加载数据
    processor = DataProcessor()
    data = processor.load_data('data.csv')
    
    # 数据预处理
    processed_data = processor.preprocess(data)
    
    # 数据分析
    analysis_results = processor.analyze(processed_data)
    
    # 可视化
    visualizer = Visualizer()
    visualizer.create_plots(processed_data, analysis_results)
    
    print("✅ 数据分析完成")

if __name__ == '__main__':
    main()
'''
        
        elif file_path == 'data_processor.py':
            return '''#!/usr/bin/env python3
"""
数据处理模块
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

class DataProcessor:
    def __init__(self):
        self.data = None
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        """加载数据"""
        try:
            self.data = pd.read_csv(file_path)
            print(f"✅ 数据加载成功: {len(self.data)} 行")
            return self.data
        except Exception as e:
            print(f"❌ 数据加载失败: {e}")
            return pd.DataFrame()
    
    def preprocess(self, data: pd.DataFrame) -> pd.DataFrame:
        """数据预处理"""
        if data.empty:
            return data
        
        # 处理缺失值
        data = data.fillna(data.mean())
        
        # 删除重复行
        data = data.drop_duplicates()
        
        # 数据类型转换
        # 在这里添加你的预处理逻辑
        
        print(f"✅ 数据预处理完成: {len(data)} 行")
        return data
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """数据分析"""
        if data.empty:
            return {}
        
        results = {
            'summary': data.describe(),
            'correlation': data.corr() if data.select_dtypes(include=[np.number]).shape[1] > 1 else None,
            'missing_values': data.isnull().sum().to_dict(),
            'data_types': data.dtypes.to_dict()
        }
        
        print("✅ 数据分析完成")
        return results
'''
        
        elif file_path == 'visualization.py':
            return '''#!/usr/bin/env python3
"""
可视化模块
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict, Any

class Visualizer:
    def __init__(self):
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
    
    def create_plots(self, data: pd.DataFrame, analysis_results: Dict[str, Any]):
        """创建图表"""
        if data.empty:
            print("❌ 没有数据可以可视化")
            return
        
        # 创建图表
        self._create_summary_plot(data)
        self._create_correlation_plot(analysis_results.get('correlation'))
        self._create_distribution_plots(data)
        
        print("✅ 可视化图表已生成")
    
    def _create_summary_plot(self, data: pd.DataFrame):
        """创建数据摘要图"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('数据摘要', fontsize=16)
        
        # 数据形状
        axes[0, 0].text(0.5, 0.5, f'数据形状: {data.shape}', 
                       ha='center', va='center', transform=axes[0, 0].transAxes)
        axes[0, 0].set_title('数据形状')
        
        # 缺失值
        missing = data.isnull().sum()
        if missing.sum() > 0:
            missing.plot(kind='bar', ax=axes[0, 1])
            axes[0, 1].set_title('缺失值统计')
        else:
            axes[0, 1].text(0.5, 0.5, '无缺失值', 
                           ha='center', va='center', transform=axes[0, 1].transAxes)
            axes[0, 1].set_title('缺失值统计')
        
        # 数据类型
        data_types = data.dtypes.value_counts()
        data_types.plot(kind='pie', ax=axes[1, 0])
        axes[1, 0].set_title('数据类型分布')
        
        # 数值列统计
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            data[numeric_cols].boxplot(ax=axes[1, 1])
            axes[1, 1].set_title('数值列分布')
            axes[1, 1].tick_params(axis='x', rotation=45)
        else:
            axes[1, 1].text(0.5, 0.5, '无数值列', 
                           ha='center', va='center', transform=axes[1, 1].transAxes)
            axes[1, 1].set_title('数值列分布')
        
        plt.tight_layout()
        plt.savefig('summary_plot.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_correlation_plot(self, correlation_matrix):
        """创建相关性图"""
        if correlation_matrix is None or correlation_matrix.empty:
            return
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('相关性矩阵')
        plt.tight_layout()
        plt.savefig('correlation_plot.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_distribution_plots(self, data: pd.DataFrame):
        """创建分布图"""
        numeric_cols = data.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) == 0:
            return
        
        # 为每个数值列创建分布图
        for col in numeric_cols[:6]:  # 限制最多6个图
            plt.figure(figsize=(10, 6))
            
            plt.subplot(1, 2, 1)
            data[col].hist(bins=30, alpha=0.7)
            plt.title(f'{col} - 直方图')
            plt.xlabel(col)
            plt.ylabel('频次')
            
            plt.subplot(1, 2, 2)
            data[col].plot(kind='box')
            plt.title(f'{col} - 箱线图')
            plt.ylabel(col)
            
            plt.tight_layout()
            plt.savefig(f'distribution_{col}.png', dpi=300, bbox_inches='tight')
            plt.close()
'''
        
        elif file_path == 'requirements.txt':
            return '''pandas==2.0.3
numpy==1.24.3
matplotlib==3.7.2
seaborn==0.12.2
scikit-learn==1.3.0
'''
        
        elif file_path == 'README.md':
            return f'''# {variables['project_name']}

{variables['description']}

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

1. 准备数据文件 `data.csv`
2. 运行分析:

```bash
python main.py
```

## 功能

- 数据加载和预处理
- 统计分析
- 数据可视化
- 图表自动生成

## 输出文件

- `summary_plot.png` - 数据摘要图
- `correlation_plot.png` - 相关性矩阵图
- `distribution_*.png` - 各列分布图

## 作者

{variables['author']} - {variables['email']}
'''
        
        elif file_path == 'notebooks/analysis.ipynb':
            return '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 数据分析笔记本\\n",
    "\\n",
    "这个笔记本用于交互式数据分析。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\\n",
    "import numpy as np\\n",
    "import matplotlib.pyplot as plt\\n",
    "import seaborn as sns\\n",
    "\\n",
    "# 设置中文字体\\n",
    "plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']\\n",
    "plt.rcParams['axes.unicode_minus'] = False"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 加载数据\\n",
    "data = pd.read_csv('../data.csv')\\n",
    "print(f\"数据形状: {data.shape}\")\\n",
    "data.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 数据预处理\\n",
    "# 在这里添加你的预处理代码"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 数据分析\\n",
    "# 在这里添加你的分析代码"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 数据可视化\\n",
    "# 在这里添加你的可视化代码"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}'''
        
        return ""
    
    def _get_package_content(self, file_path: str, variables: Dict) -> str:
        """获取Python包模板内容"""
        if file_path == 'src/__init__.py':
            return f'''"""
{variables['project_name']}

{variables['description']}

作者: {variables['author']}
版本: {variables['version']}
"""

__version__ = "{variables['version']}"
__author__ = "{variables['author']}"
__email__ = "{variables['email']}"

from .main import main

__all__ = ['main']
'''
        
        elif file_path == 'src/main.py':
            return f'''#!/usr/bin/env python3
"""
{variables['project_name']} 主模块

作者: {variables['author']}
版本: {variables['version']}
"""

def main():
    """主函数"""
    print("Hello from {variables['project_name']}!")
    return True

if __name__ == '__main__':
    main()
'''
        
        elif file_path == 'tests/__init__.py':
            return '''"""
测试包初始化
"""
'''
        
        elif file_path == 'tests/test_main.py':
            return f'''#!/usr/bin/env python3
"""
{variables['project_name']} 测试模块
"""

import unittest
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import main

class TestMain(unittest.TestCase):
    def test_main(self):
        """测试主函数"""
        result = main()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
'''
        
        elif file_path == 'setup.py':
            return f'''#!/usr/bin/env python3
"""
安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{variables['project_name'].lower().replace(' ', '-')}",
    version="{variables['version']}",
    author="{variables['author']}",
    author_email="{variables['email']}",
    description="{variables['description']}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={{"": "src"}},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        # 在这里添加依赖
    ],
    extras_require={{
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    }},
    entry_points={{
        "console_scripts": [
            "{variables['project_name'].lower().replace(' ', '-')}=main:main",
        ],
    }},
)
'''
        
        elif file_path == 'pyproject.toml':
            return f'''[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{variables['project_name'].lower().replace(' ', '-')}"
version = "{variables['version']}"
description = "{variables['description']}"
authors = [
    {{name = "{variables['author']}", email = "{variables['email']}"}}
]
readme = "README.md"
license = {{text = "MIT"}}
requires-python = ">=3.7"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
    # 在这里添加依赖
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "pytest-cov>=2.0",
    "black>=21.0",
    "flake8>=3.8",
]

[project.scripts]
{variables['project_name'].lower().replace(' ', '-')} = "main:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --cov=src --cov-report=term-missing"

[tool.black]
line-length = 88
target-version = ['py37']
include = '\\.pyi?$'

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
'''
        
        elif file_path == 'requirements.txt':
            return '''# 开发依赖
pytest>=6.0
pytest-cov>=2.0
black>=21.0
flake8>=3.8

# 运行时依赖
# 在这里添加项目依赖
'''
        
        elif file_path == 'README.md':
            return f'''# {variables['project_name']}

{variables['description']}

## 安装

### 开发安装

```bash
# 克隆仓库
git clone <repository-url>
cd {variables['project_name'].lower().replace(' ', '-')}

# 安装开发依赖
pip install -r requirements.txt

# 开发模式安装
pip install -e .
```

### 用户安装

```bash
pip install {variables['project_name'].lower().replace(' ', '-')}
```

## 使用方法

```python
from {variables['project_name'].lower().replace(' ', '_')} import main

# 运行主函数
main()
```

或者使用命令行:

```bash
{variables['project_name'].lower().replace(' ', '-')}
```

## 开发

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black src/ tests/
```

### 代码检查

```bash
flake8 src/ tests/
```

## 项目结构

```
{variables['project_name'].lower().replace(' ', '-')}/
├── src/
│   └── {variables['project_name'].lower().replace(' ', '_')}/
│       ├── __init__.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── setup.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## 作者

{variables['author']} - {variables['email']}

## 许可证

MIT License
'''
        
        return ""
    
    def _replace_variables(self, text: str, variables: Dict) -> str:
        """替换变量"""
        for key, value in variables.items():
            placeholder = f"${{{key}}}"
            text = text.replace(placeholder, str(value))
        return text
    
    def create_custom_template(self, template_name: str, template_dir: str) -> bool:
        """
        创建自定义模板
        
        Args:
            template_name: 模板名称
            template_dir: 模板目录路径
            
        Returns:
            是否成功
        """
        if not os.path.exists(template_dir):
            print(f"❌ 模板目录不存在: {template_dir}")
            return False
        
        # 创建模板目录
        template_path = os.path.join(self.templates_dir, template_name)
        if os.path.exists(template_path):
            print(f"❌ 模板已存在: {template_name}")
            return False
        
        try:
            # 复制模板文件
            shutil.copytree(template_dir, template_path)
            
            # 创建配置文件
            config = {
                'name': template_name,
                'description': f'自定义模板: {template_name}',
                'files': []
            }
            
            # 扫描文件
            for root, dirs, files in os.walk(template_path):
                for file in files:
                    if file != 'template.json':
                        rel_path = os.path.relpath(os.path.join(root, file), template_path)
                        config['files'].append(rel_path)
            
            # 保存配置
            config_file = os.path.join(template_path, 'template.json')
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 自定义模板已创建: {template_name}")
            return True
            
        except Exception as e:
            print(f"❌ 创建模板失败: {e}")
            return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="代码生成器 - 代码模板生成、脚手架工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 列出可用模板
  python code_generator.py --list
  
  # 生成Web应用
  python code_generator.py --template web-app --name my-web-app
  
  # 生成CLI工具
  python code_generator.py --template cli-tool --name my-cli-tool
  
  # 生成API服务
  python code_generator.py --template api-service --name my-api
  
  # 生成数据分析项目
  python code_generator.py --template data-analysis --name my-analysis
  
  # 生成Python包
  python code_generator.py --template package --name my-package
  
  # 使用自定义变量
  python code_generator.py --template web-app --name my-app --var author "张三" --var email "zhangsan@example.com"
  
  # 创建自定义模板
  python code_generator.py --create-template my-template /path/to/template/dir
        """
    )
    
    parser.add_argument('--list', action='store_true', help='列出可用模板')
    parser.add_argument('--template', help='模板ID')
    parser.add_argument('--name', help='项目名称')
    parser.add_argument('--output', help='输出目录')
    parser.add_argument('--var', nargs=2, action='append', metavar=('KEY', 'VALUE'), 
                       help='自定义变量 (可多次使用)')
    parser.add_argument('--create-template', nargs=2, metavar=('NAME', 'DIR'), 
                       help='创建自定义模板')
    
    args = parser.parse_args()
    
    # 创建代码生成器
    generator = CodeGenerator()
    
    try:
        if args.list:
            # 列出模板
            generator.list_templates()
        
        elif args.create_template:
            # 创建自定义模板
            template_name, template_dir = args.create_template
            generator.create_custom_template(template_name, template_dir)
        
        elif args.template and args.name:
            # 生成项目
            variables = {}
            if args.var:
                for key, value in args.var:
                    variables[key] = value
            
            success = generator.generate_project(
                args.template, args.name, args.output, variables
            )
            
            if success:
                print(f"\n🎉 项目 '{args.name}' 生成成功!")
                print(f"📁 项目目录: {args.output or os.path.join(os.getcwd(), args.name)}")
                print("\n💡 下一步:")
                print("  1. 进入项目目录")
                print("  2. 安装依赖: pip install -r requirements.txt")
                print("  3. 开始开发!")
        
        else:
            print("💡 使用 --help 查看使用说明")
    
    except KeyboardInterrupt:
        print("\n⚠️  操作被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 