#!/usr/bin/env python3
"""
主程序 - 协调所有收集器和生成器
"""
import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from collectors.ai_news import AINewsCollector
from collectors.us_stocks import USStockCollector
from collectors.hk_stocks import HKStockCollector
from generators.report_generator import ReportGenerator

def main():
    print("=" * 50)
    print("🤖 AI Daily Report Generator")
    print("=" * 50)
    
    # 1. 收集 AI 新闻
    print("\n📰 Collecting AI news...")
    ai_collector = AINewsCollector()
    ai_news = ai_collector.collect()
    print(f"✓ Collected {len(ai_news)} AI news articles")
    
    # 2. 收集美股数据
    print("\n📈 Collecting US stock data...")
    us_collector = USStockCollector()
    us_data = us_collector.collect()
    print(f"✓ Collected {len(us_data['indices'])} indices and {len(us_data['hot_stocks'])} stocks")
    
    # 3. 收集港股数据
    print("\n🇭🇰 Collecting HK stock data...")
    hk_collector = HKStockCollector()
    hk_data = hk_collector.collect()
    print(f"✓ Collected {len(hk_data['indices'])} indices and {len(hk_data['hot_stocks'])} stocks")
    
    # 4. 生成日报
    print("\n📝 Generating report...")
    generator = ReportGenerator()
    report_path = generator.generate(ai_news, us_data, hk_data)
    print(f"✓ Report saved to: {report_path}")
    
    print("\n" + "=" * 50)
    print("✅ Daily report generation completed!")
    print("=" * 50)

if __name__ == '__main__':
    main()
