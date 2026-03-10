#!/usr/bin/env python3
"""
AI新闻收集器 - 增强版（含翻译和摘要）
"""
import feedparser
import requests
import re
from datetime import datetime
from typing import List, Dict

class AINewsCollector:
    def __init__(self):
        self.rss_sources = {
            'arXiv AI': 'https://rss.arxiv.org/rss/cs.AI',
            'arXiv ML': 'https://rss.arxiv.org/rss/cs.LG',
            'Google DeepMind': 'https://deepmind.google/blog/rss.xml',
        }
        self.searxng_url = 'http://127.0.0.1:8888'
    
    def translate_title(self, title: str) -> str:
        """简单的英文标题翻译（使用关键词映射）"""
        translations = {
            'artificial intelligence': '人工智能',
            'machine learning': '机器学习',
            'deep learning': '深度学习',
            'neural network': '神经网络',
            'large language model': '大语言模型',
            'LLM': '大语言模型',
            'AI agent': 'AI智能体',
            'multimodal': '多模态',
            'reinforcement learning': '强化学习',
            'computer vision': '计算机视觉',
            'natural language processing': '自然语言处理',
            'NLP': '自然语言处理',
            'generative AI': '生成式AI',
            'transformer': 'Transformer架构',
            'diffusion model': '扩散模型',
            'robotics': '机器人',
            'autonomous': '自主的',
            'reasoning': '推理',
            'benchmark': '基准测试',
            'dataset': '数据集',
            'fine-tuning': '微调',
            'prompt': '提示词',
            'embedding': '嵌入',
            'vector': '向量',
            'clustering': '聚类',
            'optimization': '优化',
        }
        
        translated = title
        for en, cn in translations.items():
            translated = re.sub(r'\b' + re.escape(en) + r'\b', cn, translated, flags=re.IGNORECASE)
        return translated
    
    def extract_core_point(self, summary: str) -> str:
        """提取核心要点"""
        # 取前100个字符作为核心要点
        core = summary[:150] if len(summary) > 150 else summary
        # 清理HTML标签
        core = re.sub(r'<[^>]+>', '', core)
        return core.strip()
    
    def analyze_investment_implication(self, title: str, summary: str) -> str:
        """分析投资指导意义"""
        title_lower = title.lower()
        summary_lower = summary.lower()
        
        # 关键词映射到投资领域
        implications = []
        
        if any(k in title_lower or k in summary_lower for k in ['nvidia', 'gpu', 'chip', 'hardware', 'semiconductor']):
            implications.append("💡 **芯片/硬件**: 关注 NVIDIA、AMD 等 AI 芯片相关股票")
        
        if any(k in title_lower or k in summary_lower for k in ['cloud', 'infrastructure', 'data center', 'aws', 'azure']):
            implications.append("💡 **云计算**: 关注微软、亚马逊、谷歌等云服务提供商")
        
        if any(k in title_lower or k in summary_lower for k in ['robotics', 'autonomous', 'vehicle', 'car']):
            implications.append("💡 **机器人/自动驾驶**: 关注特斯拉、小鹏、蔚来等相关标的")
        
        if any(k in title_lower or k in summary_lower for k in ['healthcare', 'medical', 'drug', 'biotech']):
            implications.append("💡 **AI医疗**: 关注 AI 制药、医疗影像等相关公司")
        
        if any(k in title_lower or k in summary_lower for k in ['finance', 'trading', 'investment', 'fintech']):
            implications.append("💡 **金融科技**: 关注 AI 驱动的金融服务创新")
        
        if any(k in title_lower or k in summary_lower for k in ['security', 'cybersecurity', 'safety']):
            implications.append("💡 **网络安全**: 关注 AI 安全相关公司")
        
        if any(k in title_lower or k in summary_lower for k in ['education', 'learning']):
            implications.append("💡 **AI教育**: 关注在线教育、AI 辅助学习平台")
        
        if not implications:
            implications.append("💡 **通用AI**: 关注大模型技术进展，可能利好头部科技公司")
        
        return "\n".join(implications)
    
    def fetch_rss(self, name: str, url: str) -> List[Dict]:
        """获取RSS订阅"""
        try:
            feed = feedparser.parse(url)
            articles = []
            for entry in feed.entries[:5]:
                title = entry.get('title', '')
                summary = entry.get('summary', '')
                
                articles.append({
                    'title': title,
                    'title_cn': self.translate_title(title),
                    'link': entry.get('link', ''),
                    'summary': summary[:300] + '...' if len(summary) > 300 else summary,
                    'core_point': self.extract_core_point(summary),
                    'investment': self.analyze_investment_implication(title, summary),
                    'published': entry.get('published', ''),
                    'source': name
                })
            return articles
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            return []
    
    def search_news(self, query: str = "artificial intelligence AI latest news") -> List[Dict]:
        """使用SearXNG搜索新闻"""
        try:
            url = f"{self.searxng_url}/search"
            params = {
                'q': query,
                'format': 'json',
                'engines': 'google,duckduckgo,brave',
                'time_range': 'day'
            }
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            articles = []
            for result in data.get('results', [])[:8]:
                title = result.get('title', '')
                content = result.get('content', '')
                
                articles.append({
                    'title': title,
                    'title_cn': self.translate_title(title),
                    'link': result.get('url', ''),
                    'summary': content[:300] + '...' if len(content) > 300 else content,
                    'core_point': self.extract_core_point(content),
                    'investment': self.analyze_investment_implication(title, content),
                    'published': datetime.now().strftime('%Y-%m-%d'),
                    'source': f"Search ({result.get('engine', 'unknown')})"
                })
            return articles
        except Exception as e:
            print(f"Error searching news: {e}")
            return []
    
    def collect(self) -> List[Dict]:
        """收集所有AI新闻"""
        all_news = []
        
        # 从RSS收集
        for name, url in self.rss_sources.items():
            news = self.fetch_rss(name, url)
            all_news.extend(news)
        
        # 从搜索收集
        search_news = self.search_news()
        all_news.extend(search_news)
        
        # 去重
        seen = set()
        unique_news = []
        for item in all_news:
            if item['link'] not in seen:
                seen.add(item['link'])
                unique_news.append(item)
        
        return unique_news[:10]

if __name__ == '__main__':
    collector = AINewsCollector()
    news = collector.collect()
    print(f"Collected {len(news)} AI news articles")
    for item in news[:2]:
        print(f"\n标题: {item['title_cn']}")
        print(f"核心要点: {item['core_point'][:100]}...")
        print(f"投资指导: {item['investment'][:100]}...")
