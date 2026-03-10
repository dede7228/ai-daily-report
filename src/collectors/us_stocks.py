#!/usr/bin/env python3
"""
美股数据收集器
使用 yfinance 获取免费股票数据
"""
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List

class USStockCollector:
    def __init__(self):
        # 主要指数和热门股票
        self.indices = {
            '^GSPC': '标普500',
            '^IXIC': '纳斯达克',
            '^DJI': '道琼斯',
        }
        self.hot_stocks = {
            'AAPL': '苹果',
            'MSFT': '微软',
            'GOOGL': '谷歌',
            'AMZN': '亚马逊',
            'TSLA': '特斯拉',
            'NVDA': '英伟达',
            'META': 'Meta',
            'AMD': 'AMD',
        }
    
    def get_stock_data(self, symbol: str, name: str) -> Dict:
        """获取单个股票数据"""
        try:
            ticker = yf.Ticker(symbol)
            # 获取最近2天的数据
            hist = ticker.history(period='2d')
            
            if len(hist) < 2:
                return None
            
            latest = hist.iloc[-1]
            previous = hist.iloc[-2]
            
            current_price = latest['Close']
            prev_close = previous['Close']
            change = current_price - prev_close
            change_pct = (change / prev_close) * 100
            
            return {
                'symbol': symbol,
                'name': name,
                'price': round(current_price, 2),
                'change': round(change, 2),
                'change_pct': round(change_pct, 2),
                'volume': int(latest['Volume']),
                'high': round(latest['High'], 2),
                'low': round(latest['Low'], 2),
            }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None
    
    def collect_indices(self) -> List[Dict]:
        """收集主要指数"""
        data = []
        for symbol, name in self.indices.items():
            stock_data = self.get_stock_data(symbol, name)
            if stock_data:
                data.append(stock_data)
        return data
    
    def collect_hot_stocks(self) -> List[Dict]:
        """收集热门股票"""
        data = []
        for symbol, name in self.hot_stocks.items():
            stock_data = self.get_stock_data(symbol, name)
            if stock_data:
                data.append(stock_data)
        return data
    
    def collect(self) -> Dict:
        """收集所有美股数据"""
        return {
            'indices': self.collect_indices(),
            'hot_stocks': self.collect_hot_stocks(),
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

if __name__ == '__main__':
    collector = USStockCollector()
    data = collector.collect()
    print(f"Collected {len(data['indices'])} indices and {len(data['hot_stocks'])} stocks")
    for idx in data['indices']:
        print(f"- {idx['name']}: {idx['price']} ({idx['change_pct']}%)")
