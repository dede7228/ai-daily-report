#!/usr/bin/env python3
"""
AI新闻收集器
"""
import feedparser
import requests
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
    
    def fetch_rss(self, name: str, url: str) -> List[Dict]:
        """获取RSS订阅"""
        try:
            feed = feedparser.parse(url)
            articles = []
            for entry in feed.entries[:5]:  # 每个源取前5条
                articles.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', '')[:200] + '...' if len(entry.get('summary', '')) > 200 else entry.get('summary', ''),
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
                'time_range': 'day'  # 最近24小时
            }
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            articles = []
            for result in data.get('results', [])[:8]:
                articles.append({
                    'title': result.get('title', ''),
                    'link': result.get('url', ''),
                    'summary': result.get('content', '')[:300] + '...' if len(result.get('content', '')) > 300 else result.get('content', ''),
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
        
        return unique_news[:10]  # 返回前10条

if __name__ == '__main__':
    collector = AINewsCollector()
    news = collector.collect()
    print(f"Collected {len(news)} AI news articles")
    for item in news[:3]:
        print(f"- {item['title'][:60]}... ({item['source']})")
