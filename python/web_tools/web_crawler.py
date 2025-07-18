#!/usr/bin/env python3
"""
网页爬虫 - 简单的网页数据抓取工具

功能:
- 抓取网页内容
- 提取特定元素
- 支持CSS选择器和XPath
- 保存为JSON或CSV格式
- 支持多页面抓取
- 自定义请求头

作者: ToolCollection Team
版本: 1.0.0
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
import time
from urllib.parse import urljoin, urlparse

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WebCrawler:
    """网页爬虫类"""
    
    def __init__(self, headers: Optional[Dict[str, str]] = None, delay: float = 1.0):
        """
        初始化爬虫
        
        Args:
            headers: 自定义请求头
            delay: 请求间隔时间（秒）
        """
        self.session = requests.Session()
        self.delay = delay
        
        # 设置默认请求头
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        if headers:
            default_headers.update(headers)
        
        self.session.headers.update(default_headers)
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        获取网页内容
        
        Args:
            url: 网页URL
            
        Returns:
            BeautifulSoup对象或None
        """
        try:
            logger.info(f"正在抓取: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            logger.info(f"成功抓取页面，大小: {len(response.content)} 字节")
            
            # 延迟请求
            time.sleep(self.delay)
            
            return soup
            
        except requests.RequestException as e:
            logger.error(f"抓取页面失败 {url}: {e}")
            return None
    
    def extract_text(self, soup: BeautifulSoup, selector: str) -> List[str]:
        """
        使用CSS选择器提取文本
        
        Args:
            soup: BeautifulSoup对象
            selector: CSS选择器
            
        Returns:
            提取的文本列表
        """
        elements = soup.select(selector)
        return [elem.get_text(strip=True) for elem in elements]
    
    def extract_links(self, soup: BeautifulSoup, selector: str = 'a[href]') -> List[str]:
        """
        提取链接
        
        Args:
            soup: BeautifulSoup对象
            selector: CSS选择器
            
        Returns:
            链接列表
        """
        elements = soup.select(selector)
        links = []
        
        for elem in elements:
            href = elem.get('href')
            if href:
                links.append(href)
        
        return links
    
    def extract_attributes(self, soup: BeautifulSoup, selector: str, 
                          attributes: List[str]) -> List[Dict[str, str]]:
        """
        提取元素属性
        
        Args:
            soup: BeautifulSoup对象
            selector: CSS选择器
            attributes: 要提取的属性列表
            
        Returns:
            属性字典列表
        """
        elements = soup.select(selector)
        results = []
        
        for elem in elements:
            attrs = {}
            for attr in attributes:
                value = elem.get(attr)
                if value:
                    attrs[attr] = value
            if attrs:
                results.append(attrs)
        
        return results
    
    def crawl_single_page(self, url: str, selectors: Dict[str, str]) -> Dict[str, Any]:
        """
        抓取单个页面
        
        Args:
            url: 页面URL
            selectors: 选择器配置 {字段名: CSS选择器}
            
        Returns:
            抓取的数据字典
        """
        soup = self.fetch_page(url)
        if not soup:
            return {}
        
        data = {'url': url}
        
        for field, selector in selectors.items():
            if selector.startswith('attr:'):
                # 提取属性
                attr_selector = selector[5:]  # 去掉 'attr:' 前缀
                attr_name = attr_selector.split('[')[1].split(']')[0]
                elements = soup.select(attr_selector)
                data[field] = [elem.get(attr_name) for elem in elements if elem.get(attr_name)]
            else:
                # 提取文本
                data[field] = self.extract_text(soup, selector)
        
        return data
    
    def crawl_multiple_pages(self, urls: List[str], selectors: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        抓取多个页面
        
        Args:
            urls: URL列表
            selectors: 选择器配置
            
        Returns:
            抓取的数据列表
        """
        results = []
        
        for url in urls:
            data = self.crawl_single_page(url, selectors)
            if data:
                results.append(data)
        
        return results
    
    def save_to_json(self, data: List[Dict[str, Any]], output_file: str) -> None:
        """
        保存数据为JSON格式
        
        Args:
            data: 要保存的数据
            output_file: 输出文件路径
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已保存到: {output_file}")
        except Exception as e:
            logger.error(f"保存JSON文件失败: {e}")
    
    def save_to_csv(self, data: List[Dict[str, Any]], output_file: str) -> None:
        """
        保存数据为CSV格式
        
        Args:
            data: 要保存的数据
            output_file: 输出文件路径
        """
        if not data:
            logger.warning("没有数据可保存")
            return
        
        try:
            # 获取所有字段名
            fieldnames = set()
            for item in data:
                fieldnames.update(item.keys())
            fieldnames = sorted(list(fieldnames))
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for item in data:
                    # 处理列表类型的值
                    row = {}
                    for field in fieldnames:
                        value = item.get(field, '')
                        if isinstance(value, list):
                            row[field] = '; '.join(str(v) for v in value)
                        else:
                            row[field] = value
                    writer.writerow(row)
            
            logger.info(f"数据已保存到: {output_file}")
        except Exception as e:
            logger.error(f"保存CSV文件失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='网页数据抓取工具')
    parser.add_argument('url', help='要抓取的网页URL')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-f', '--format', choices=['json', 'csv'], default='json', 
                       help='输出格式（默认: json）')
    parser.add_argument('-s', '--selectors', nargs=2, action='append',
                       metavar=('FIELD', 'SELECTOR'), help='字段名和CSS选择器')
    parser.add_argument('--delay', type=float, default=1.0, help='请求间隔时间（秒）')
    parser.add_argument('--user-agent', help='自定义User-Agent')
    parser.add_argument('--extract-links', action='store_true', help='提取所有链接')
    parser.add_argument('--extract-images', action='store_true', help='提取所有图片')
    
    args = parser.parse_args()
    
    try:
        # 设置请求头
        headers = {}
        if args.user_agent:
            headers['User-Agent'] = args.user_agent
        
        # 创建爬虫
        crawler = WebCrawler(headers=headers, delay=args.delay)
        
        # 设置选择器
        selectors = {}
        if args.selectors:
            for field, selector in args.selectors:
                selectors[field] = selector
        
        # 默认选择器
        if not selectors:
            if args.extract_links:
                selectors['links'] = 'a[href]'
            elif args.extract_images:
                selectors['images'] = 'img[src]'
            else:
                # 默认提取标题和正文
                selectors = {
                    'title': 'title',
                    'headings': 'h1, h2, h3',
                    'paragraphs': 'p',
                    'links': 'a[href]'
                }
        
        # 抓取数据
        data = crawler.crawl_single_page(args.url, selectors)
        
        if not data:
            logger.error("没有抓取到数据")
            sys.exit(1)
        
        # 确定输出文件
        if not args.output:
            parsed_url = urlparse(args.url)
            domain = parsed_url.netloc.replace('.', '_')
            args.output = f"crawled_{domain}.{args.format}"
        
        # 保存数据
        if args.format == 'json':
            crawler.save_to_json([data], args.output)
        else:
            crawler.save_to_csv([data], args.output)
        
        # 显示结果摘要
        print(f"\n=== 抓取结果摘要 ===")
        print(f"URL: {args.url}")
        print(f"输出文件: {args.output}")
        for field, value in data.items():
            if isinstance(value, list):
                print(f"{field}: {len(value)} 项")
            else:
                print(f"{field}: {value}")
        
    except Exception as e:
        logger.error(f"抓取失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 