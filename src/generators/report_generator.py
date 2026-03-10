#!/usr/bin/env python3
"""
日报生成器 - 生成 Hugo 格式的 Markdown 文件
"""
import os
from datetime import datetime
from jinja2 import Template

class ReportGenerator:
    def __init__(self, output_dir='website/content/posts'):
        self.output_dir = output_dir
        self.template = Template('''---
title: "AI Daily Report - {{ date }}"
date: {{ iso_date }}
draft: false
---

# 🤖 AI Daily Report - {{ date }}

> 自动生成于 {{ update_time }}

---

## 📰 AI 头条

{% for news in ai_news %}
### {{ loop.index }}. {{ news.title }}

{{ news.summary }}

🔗 [阅读原文]({{ news.link }}) | 来源: {{ news.source }}

{% endfor %}

---

## 📈 美股速览

### 主要指数

| 指数 | 点位 | 涨跌 | 涨跌幅 |
|------|------|------|--------|
{% for idx in us_indices %}
| {{ idx.name }} | {{ idx.price }} | {{ "+" if idx.change > 0 else "" }}{{ idx.change }} | {{ "+" if idx.change_pct > 0 else "" }}{{ idx.change_pct }}% |
{% endfor %}

### 热门科技股

| 股票 | 名称 | 价格 | 涨跌 | 涨跌幅 |
|------|------|------|------|--------|
{% for stock in us_stocks %}
| {{ stock.symbol }} | {{ stock.name }} | {{ stock.price }} | {{ "+" if stock.change > 0 else "" }}{{ stock.change }} | {{ "+" if stock.change_pct > 0 else "" }}{{ stock.change_pct }}% |
{% endfor %}

---

## 🇭🇰 港股速览

### 主要指数

| 指数 | 点位 | 涨跌 | 涨跌幅 |
|------|------|------|--------|
{% for idx in hk_indices %}
| {{ idx.name }} | {{ idx.price }} | {{ "+" if idx.change > 0 else "" }}{{ idx.change }} | {{ "+" if idx.change_pct > 0 else "" }}{{ idx.change_pct }}% |
{% endfor %}

### 热门科技股

| 股票 | 名称 | 价格 | 涨跌 | 涨跌幅 |
|------|------|------|------|--------|
{% for stock in hk_stocks %}
| {{ stock.symbol }} | {{ stock.name }} | {{ stock.price }} | {{ "+" if stock.change > 0 else "" }}{{ stock.change }} | {{ "+" if stock.change_pct > 0 else "" }}{{ stock.change_pct }}% |
{% endfor %}

---

## 💡 市场洞察

*基于当日数据自动生成的简要分析*

{% if us_indices %}
**美股概况**: 今日{{ us_indices[0].name }}{{ "上涨" if us_indices[0].change > 0 else "下跌" }}{{ us_indices[0].change_pct }}%，市场情绪{{ "积极" if us_indices[0].change > 0 else "谨慎" }}。
{% endif %}

{% if hk_indices %}
**港股概况**: 今日{{ hk_indices[0].name }}{{ "上涨" if hk_indices[0].change > 0 else "下跌" }}{{ hk_indices[0].change_pct }}%，
{% endif %}

---

*本报告由 AI 自动生成，仅供参考，不构成投资建议。*
''')
    
    def generate(self, ai_news: list, us_data: dict, hk_data: dict) -> str:
        """生成日报文件"""
        today = datetime.now()
        
        content = self.template.render(
            date=today.strftime('%Y年%m月%d日'),
            iso_date=today.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
            update_time=today.strftime('%Y-%m-%d %H:%M:%S'),
            ai_news=ai_news,
            us_indices=us_data.get('indices', []),
            us_stocks=us_data.get('hot_stocks', []),
            hk_indices=hk_data.get('indices', []),
            hk_stocks=hk_data.get('hot_stocks', [])
        )
        
        # 确保目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 生成文件名
        filename = f"{today.strftime('%Y-%m-%d')}-daily-report.md"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Report generated: {filepath}")
        return filepath

if __name__ == '__main__':
    generator = ReportGenerator()
    # 测试数据
    test_news = [{'title': 'Test', 'summary': 'Test summary', 'link': 'http://test.com', 'source': 'Test'}]
    test_us = {'indices': [], 'hot_stocks': []}
    test_hk = {'indices': [], 'hot_stocks': []}
    generator.generate(test_news, test_us, test_hk)
