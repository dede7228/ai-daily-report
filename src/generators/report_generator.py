#!/usr/bin/env python3
"""
日报生成器 - 增强版（含投资分析）
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
### {{ loop.index }}. {{ news.title_cn }}

**原文标题**: {{ news.title }}

🔍 **核心要点**: {{ news.core_point }}

📊 **投资指导**:
{{ news.investment }}

🔗 [阅读原文]({{ news.link }}) | 来源: {{ news.source }}

---

{% endfor %}

## 💰 今日投资机会汇总

基于今日 AI 新闻，以下是值得关注的投资方向：

{% set sectors = {} %}
{% for news in ai_news %}
{% if '芯片' in news.investment %}{% set _ = sectors.update({'芯片/硬件': sectors.get('芯片/硬件', 0) + 1}) %}{% endif %}
{% if '云计算' in news.investment %}{% set _ = sectors.update({'云计算': sectors.get('云计算', 0) + 1}) %}{% endif %}
{% if '机器人' in news.investment %}{% set _ = sectors.update({'机器人/自动驾驶': sectors.get('机器人/自动驾驶', 0) + 1}) %}{% endif %}
{% if '医疗' in news.investment %}{% set _ = sectors.update({'AI医疗': sectors.get('AI医疗', 0) + 1}) %}{% endif %}
{% if '金融' in news.investment %}{% set _ = sectors.update({'金融科技': sectors.get('金融科技', 0) + 1}) %}{% endif %}
{% if '安全' in news.investment %}{% set _ = sectors.update({'网络安全': sectors.get('网络安全', 0) + 1}) %}{% endif %}
{% if '教育' in news.investment %}{% set _ = sectors.update({'AI教育': sectors.get('AI教育', 0) + 1}) %}{% endif %}
{% if '通用AI' in news.investment %}{% set _ = sectors.update({'通用AI/大模型': sectors.get('通用AI/大模型', 0) + 1}) %}{% endif %}
{% endfor %}

{% for sector, count in sectors|dictsort(by='value', reverse=true) %}
### {{ sector }} ({{ count }}条相关)

{% if sector == '芯片/硬件' %}
- **美股**: NVIDIA (NVDA), AMD, Intel (INTC), Broadcom (AVGO)
- **港股**: 中芯国际 (00981), 华虹半导体 (01347)
- **逻辑**: AI算力需求持续增长，芯片是基础设施
{% elif sector == '云计算' %}
- **美股**: Microsoft (MSFT), Amazon (AMZN), Google (GOOGL), Alibaba (BABA)
- **港股**: 腾讯 (00700), 阿里巴巴 (09988)
- **逻辑**: 大模型训练和部署依赖云基础设施
{% elif sector == '机器人/自动驾驶' %}
- **美股**: Tesla (TSLA), Google (Waymo)
- **港股**: 小鹏汽车 (09868), 蔚来 (09866), 理想汽车 (02015)
- **逻辑**: AI技术推动自动驾驶和机器人商业化加速
{% elif sector == 'AI医疗' %}
- **美股**: Recursion (RXRX), Tempus AI (TEM)
- **港股**: 平安好医生 (01833), 医渡科技 (02158)
- **逻辑**: AI在药物研发和诊断领域应用深化
{% elif sector == '金融科技' %}
- **美股**: PayPal (PYPL), Block (SQ), Coinbase (COIN)
- **港股**: 众安在线 (06060), 金融壹账通 (OCFT)
- **逻辑**: AI提升金融服务效率和风控能力
{% elif sector == '网络安全' %}
- **美股**: CrowdStrike (CRWD), Palo Alto Networks (PANW)
- **港股**: 奇安信 (688561), 深信服 (300454)
- **逻辑**: AI安全需求随AI应用普及而增长
{% elif sector == 'AI教育' %}
- **美股**: Chegg (CHGG), Duolingo (DUOL)
- **港股**: 新东方 (09901), 好未来 (TAL)
- **逻辑**: AI个性化学习和辅助教学成为趋势
{% else %}
- **美股**: Microsoft (MSFT), Google (GOOGL), Meta (META), Apple (AAPL)
- **港股**: 腾讯 (00700), 阿里巴巴 (09988), 百度 (09888)
- **逻辑**: 头部科技公司在大模型竞赛中占据优势
{% endif %}

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

## 🎯 今日市场洞察

{% if us_indices %}
**美股概况**: 今日{{ us_indices[0].name }}{{ "上涨" if us_indices[0].change > 0 else "下跌" }}{{ us_indices[0].change_pct }}%，市场情绪{{ "积极" if us_indices[0].change > 0 else "谨慎" }}。
{% endif %}

{% if hk_indices %}
**港股概况**: 今日{{ hk_indices[0].name }}{{ "上涨" if hk_indices[0].change > 0 else "下跌" }}{{ hk_indices[0].change_pct }}%。
{% endif %}

**AI投资趋势**: 
{% if ai_news %}
{% set ai_trend = "今日AI领域" %}
{% if sectors %}
{% set top_sector = sectors|dictsort(by='value', reverse=true)|first %}
{{ ai_trend }}热点集中在**{{ top_sector[0] }}**方向，建议关注相关板块机会。
{% else %}
{{ ai_trend }}保持活跃，建议持续关注头部科技公司动态。
{% endif %}
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
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        filename = f"{today.strftime('%Y-%m-%d')}-daily-report.md"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Report generated: {filepath}")
        return filepath

if __name__ == '__main__':
    generator = ReportGenerator()
    test_news = [{
        'title': 'Test', 
        'title_cn': '测试标题',
        'summary': 'Test summary', 
        'core_point': '核心要点',
        'investment': '💡 **通用AI**: 关注大模型技术进展',
        'link': 'http://test.com', 
        'source': 'Test'
    }]
    test_us = {'indices': [], 'hot_stocks': []}
    test_hk = {'indices': [], 'hot_stocks': []}
    generator.generate(test_news, test_us, test_hk)
