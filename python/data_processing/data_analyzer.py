#!/usr/bin/env python3
"""
数据分析器 - 高级数据分析和统计工具

功能:
- 描述性统计分析
- 相关性分析
- 异常值检测
- 数据分布分析
- 时间序列分析
- 机器学习预处理

作者: ToolCollection Team
版本: 1.0.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
import json

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 设置matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class DataAnalyzer:
    """数据分析器类"""
    
    def __init__(self, data: Optional[pd.DataFrame] = None):
        """
        初始化数据分析器
        
        Args:
            data: 输入数据框
        """
        self.data = data
        self.analysis_results = {}
    
    def load_data(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        加载数据
        
        Args:
            file_path: 数据文件路径
            **kwargs: pandas读取参数
            
        Returns:
            加载的数据框
        """
        try:
            if file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path, **kwargs)
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                self.data = pd.read_excel(file_path, **kwargs)
            elif file_path.endswith('.json'):
                self.data = pd.read_json(file_path, **kwargs)
            else:
                raise ValueError(f"不支持的文件格式: {file_path}")
            
            logger.info(f"成功加载数据: {file_path}, 形状: {self.data.shape}")
            return self.data
        except Exception as e:
            logger.error(f"加载数据失败: {e}")
            raise
    
    def descriptive_statistics(self, columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        描述性统计分析
        
        Args:
            columns: 要分析的列名，None表示所有数值列
            
        Returns:
            描述性统计结果
        """
        if self.data is None:
            raise ValueError("没有数据可分析")
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        numeric_data = self.data[columns]
        
        stats_result = {
            'basic_stats': numeric_data.describe(),
            'skewness': numeric_data.skew(),
            'kurtosis': numeric_data.kurtosis(),
            'missing_values': numeric_data.isnull().sum(),
            'unique_values': numeric_data.nunique()
        }
        
        # 添加分位数信息
        percentiles = [0.05, 0.25, 0.5, 0.75, 0.95]
        stats_result['percentiles'] = numeric_data.quantile(percentiles)
        
        self.analysis_results['descriptive'] = stats_result
        return stats_result
    
    def correlation_analysis(self, method: str = 'pearson', 
                           plot: bool = True) -> pd.DataFrame:
        """
        相关性分析
        
        Args:
            method: 相关系数计算方法 ('pearson', 'spearman', 'kendall')
            plot: 是否绘制相关性热力图
            
        Returns:
            相关系数矩阵
        """
        if self.data is None:
            raise ValueError("没有数据可分析")
        
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if len(numeric_data.columns) < 2:
            raise ValueError("需要至少两个数值列进行相关性分析")
        
        correlation_matrix = numeric_data.corr(method=method)
        
        if plot:
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, linewidths=0.5)
            plt.title(f'{method.capitalize()}相关系数矩阵')
            plt.tight_layout()
            plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        self.analysis_results['correlation'] = correlation_matrix
        return correlation_matrix
    
    def outlier_detection(self, method: str = 'iqr', 
                         columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        异常值检测
        
        Args:
            method: 检测方法 ('iqr', 'zscore', 'isolation_forest')
            columns: 要检测的列名
            
        Returns:
            异常值检测结果
        """
        if self.data is None:
            raise ValueError("没有数据可分析")
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        numeric_data = self.data[columns]
        outliers = {}
        
        if method == 'iqr':
            for col in columns:
                Q1 = numeric_data[col].quantile(0.25)
                Q3 = numeric_data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outlier_mask = (numeric_data[col] < lower_bound) | (numeric_data[col] > upper_bound)
                outliers[col] = {
                    'count': outlier_mask.sum(),
                    'percentage': (outlier_mask.sum() / len(numeric_data)) * 100,
                    'indices': numeric_data[outlier_mask].index.tolist(),
                    'values': numeric_data[col][outlier_mask].tolist()
                }
        
        elif method == 'zscore':
            for col in columns:
                z_scores = np.abs(stats.zscore(numeric_data[col].dropna()))
                outlier_mask = z_scores > 3
                outliers[col] = {
                    'count': outlier_mask.sum(),
                    'percentage': (outlier_mask.sum() / len(numeric_data)) * 100,
                    'indices': numeric_data[col].dropna()[outlier_mask].index.tolist(),
                    'values': numeric_data[col].dropna()[outlier_mask].tolist()
                }
        
        self.analysis_results['outliers'] = outliers
        return outliers
    
    def distribution_analysis(self, columns: Optional[List[str]] = None,
                            plot: bool = True) -> Dict[str, Any]:
        """
        数据分布分析
        
        Args:
            columns: 要分析的列名
            plot: 是否绘制分布图
            
        Returns:
            分布分析结果
        """
        if self.data is None:
            raise ValueError("没有数据可分析")
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        numeric_data = self.data[columns]
        distribution_results = {}
        
        for col in columns:
            data = numeric_data[col].dropna()
            
            # 正态性检验
            shapiro_stat, shapiro_p = stats.shapiro(data)
            ks_stat, ks_p = stats.kstest(data, 'norm', args=(data.mean(), data.std()))
            
            distribution_results[col] = {
                'shapiro_test': {'statistic': shapiro_stat, 'p_value': shapiro_p},
                'ks_test': {'statistic': ks_stat, 'p_value': ks_p},
                'is_normal': shapiro_p > 0.05,
                'mean': data.mean(),
                'std': data.std(),
                'median': data.median(),
                'mode': data.mode().iloc[0] if len(data.mode()) > 0 else None
            }
            
            if plot:
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                
                # 直方图
                ax1.hist(data, bins=30, alpha=0.7, density=True, color='skyblue')
                ax1.axvline(data.mean(), color='red', linestyle='--', label=f'均值: {data.mean():.2f}')
                ax1.axvline(data.median(), color='green', linestyle='--', label=f'中位数: {data.median():.2f}')
                ax1.set_title(f'{col} 分布直方图')
                ax1.legend()
                
                # Q-Q图
                stats.probplot(data, dist="norm", plot=ax2)
                ax2.set_title(f'{col} Q-Q图')
                
                plt.tight_layout()
                plt.savefig(f'distribution_{col}.png', dpi=300, bbox_inches='tight')
                plt.show()
        
        self.analysis_results['distribution'] = distribution_results
        return distribution_results
    
    def time_series_analysis(self, date_column: str, value_column: str,
                           freq: str = 'D') -> Dict[str, Any]:
        """
        时间序列分析
        
        Args:
            date_column: 日期列名
            value_column: 数值列名
            freq: 时间频率 ('D', 'W', 'M', 'Y')
            
        Returns:
            时间序列分析结果
        """
        if self.data is None:
            raise ValueError("没有数据可分析")
        
        # 确保日期列格式正确
        self.data[date_column] = pd.to_datetime(self.data[date_column])
        
        # 设置日期索引
        ts_data = self.data.set_index(date_column)[value_column].sort_index()
        
        # 重采样
        resampled = ts_data.resample(freq).mean()
        
        # 时间序列统计
        ts_stats = {
            'trend': resampled.rolling(window=min(30, len(resampled)//4)).mean(),
            'seasonal': resampled.groupby(resampled.index.month).mean() if freq == 'M' else None,
            'autocorrelation': resampled.autocorr(),
            'stationarity_test': self._adf_test(resampled)
        }
        
        # 绘制时间序列图
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 1, 1)
        plt.plot(resampled.index, resampled.values, label='原始数据')
        plt.plot(ts_stats['trend'].index, ts_stats['trend'].values, 
                label='趋势线', color='red')
        plt.title(f'{value_column} 时间序列分析')
        plt.legend()
        
        if ts_stats['seasonal'] is not None:
            plt.subplot(2, 1, 2)
            plt.plot(ts_stats['seasonal'].index, ts_stats['seasonal'].values, 
                    marker='o', color='green')
            plt.title('季节性模式')
            plt.xlabel('月份')
            plt.ylabel('平均值')
        
        plt.tight_layout()
        plt.savefig('time_series_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        self.analysis_results['time_series'] = ts_stats
        return ts_stats
    
    def _adf_test(self, series: pd.Series) -> Dict[str, float]:
        """ADF单位根检验"""
        try:
            from statsmodels.tsa.stattools import adfuller
            result = adfuller(series.dropna())
            return {
                'adf_statistic': result[0],
                'p_value': result[1],
                'critical_values': result[4],
                'is_stationary': result[1] < 0.05
            }
        except ImportError:
            logger.warning("statsmodels未安装，跳过ADF检验")
            return {}
    
    def dimensionality_reduction(self, columns: Optional[List[str]] = None,
                               method: str = 'pca', n_components: int = 2) -> Dict[str, Any]:
        """
        降维分析
        
        Args:
            columns: 要分析的列名
            method: 降维方法 ('pca', 'kmeans')
            n_components: 目标维度
            
        Returns:
            降维结果
        """
        if self.data is None:
            raise ValueError("没有数据可分析")
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        numeric_data = self.data[columns].dropna()
        
        if method == 'pca':
            # 标准化数据
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(numeric_data)
            
            # PCA降维
            pca = PCA(n_components=min(n_components, len(columns)))
            pca_result = pca.fit_transform(scaled_data)
            
            # 解释方差比例
            explained_variance_ratio = pca.explained_variance_ratio_
            cumulative_variance_ratio = np.cumsum(explained_variance_ratio)
            
            result = {
                'transformed_data': pca_result,
                'explained_variance_ratio': explained_variance_ratio,
                'cumulative_variance_ratio': cumulative_variance_ratio,
                'components': pca.components_,
                'feature_names': columns
            }
            
            # 绘制解释方差比例图
            plt.figure(figsize=(10, 6))
            plt.plot(range(1, len(explained_variance_ratio) + 1), 
                    cumulative_variance_ratio, 'bo-')
            plt.xlabel('主成分数量')
            plt.ylabel('累积解释方差比例')
            plt.title('PCA解释方差比例')
            plt.grid(True)
            plt.savefig('pca_variance_ratio.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        elif method == 'kmeans':
            # K-means聚类
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(numeric_data)
            
            kmeans = KMeans(n_clusters=n_components, random_state=42)
            cluster_labels = kmeans.fit_predict(scaled_data)
            
            result = {
                'cluster_labels': cluster_labels,
                'cluster_centers': kmeans.cluster_centers_,
                'inertia': kmeans.inertia_
            }
            
            # 绘制聚类结果（如果降到2维）
            if len(columns) >= 2:
                plt.figure(figsize=(10, 8))
                scatter = plt.scatter(scaled_data[:, 0], scaled_data[:, 1], 
                                    c=cluster_labels, cmap='viridis')
                plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
                           c='red', marker='x', s=200, linewidths=3, label='聚类中心')
                plt.xlabel(columns[0])
                plt.ylabel(columns[1])
                plt.title('K-means聚类结果')
                plt.legend()
                plt.colorbar(scatter)
                plt.savefig('kmeans_clustering.png', dpi=300, bbox_inches='tight')
                plt.show()
        
        self.analysis_results['dimensionality_reduction'] = result
        return result
    
    def generate_report(self, output_file: str = 'data_analysis_report.html') -> None:
        """
        生成分析报告
        
        Args:
            output_file: 输出文件路径
        """
        if not self.analysis_results:
            logger.warning("没有分析结果可生成报告")
            return
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>数据分析报告</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1, h2, h3 { color: #333; }
                .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
                .metric { display: inline-block; margin: 10px; padding: 10px; background: #f5f5f5; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>数据分析报告</h1>
            <p>生成时间: {timestamp}</p>
        """.format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # 添加各个分析结果
        for analysis_type, results in self.analysis_results.items():
            html_content += f"<div class='section'><h2>{analysis_type.replace('_', ' ').title()}</h2>"
            
            if analysis_type == 'descriptive':
                html_content += "<h3>基本统计信息</h3>"
                html_content += results['basic_stats'].to_html()
                
                html_content += "<h3>偏度和峰度</h3>"
                html_content += "<table><tr><th>列名</th><th>偏度</th><th>峰度</th></tr>"
                for col in results['skewness'].index:
                    html_content += f"<tr><td>{col}</td><td>{results['skewness'][col]:.4f}</td><td>{results['kurtosis'][col]:.4f}</td></tr>"
                html_content += "</table>"
            
            elif analysis_type == 'correlation':
                html_content += "<h3>相关系数矩阵</h3>"
                html_content += results.to_html()
            
            elif analysis_type == 'outliers':
                html_content += "<h3>异常值检测结果</h3>"
                for col, outlier_info in results.items():
                    html_content += f"<div class='metric'><strong>{col}</strong><br>"
                    html_content += f"异常值数量: {outlier_info['count']}<br>"
                    html_content += f"异常值比例: {outlier_info['percentage']:.2f}%</div>"
            
            html_content += "</div>"
        
        html_content += """
        </body>
        </html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"分析报告已生成: {output_file}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='高级数据分析和统计工具')
    parser.add_argument('input', help='输入数据文件路径')
    parser.add_argument('--columns', nargs='+', help='要分析的列名')
    parser.add_argument('--descriptive', action='store_true', help='描述性统计分析')
    parser.add_argument('--correlation', action='store_true', help='相关性分析')
    parser.add_argument('--outliers', action='store_true', help='异常值检测')
    parser.add_argument('--distribution', action='store_true', help='分布分析')
    parser.add_argument('--timeseries', nargs=2, metavar=('DATE_COL', 'VALUE_COL'), 
                       help='时间序列分析')
    parser.add_argument('--dimension', nargs=2, metavar=('METHOD', 'N_COMPONENTS'), 
                       help='降维分析')
    parser.add_argument('--report', help='生成HTML报告文件路径')
    
    args = parser.parse_args()
    
    try:
        # 创建分析器
        analyzer = DataAnalyzer()
        
        # 加载数据
        analyzer.load_data(args.input)
        
        # 执行分析
        if args.descriptive:
            analyzer.descriptive_statistics(args.columns)
        
        if args.correlation:
            analyzer.correlation_analysis()
        
        if args.outliers:
            analyzer.outlier_detection(columns=args.columns)
        
        if args.distribution:
            analyzer.distribution_analysis(columns=args.columns)
        
        if args.timeseries:
            analyzer.time_series_analysis(args.timeseries[0], args.timeseries[1])
        
        if args.dimension:
            method, n_components = args.dimension
            analyzer.dimensionality_reduction(columns=args.columns, 
                                           method=method, 
                                           n_components=int(n_components))
        
        # 生成报告
        if args.report:
            analyzer.generate_report(args.report)
        
    except Exception as e:
        logger.error(f"分析失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 