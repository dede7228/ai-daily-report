#!/usr/bin/env python3
"""
港股数据收集器
"""
import yfinance as yf
from datetime import datetime
from typing import Dict, List

class HKStockCollector:
    def __init__(self):
        # 主要指数和热门港股
        self.indices = {
            '^HSI': '恒生指数',
            '^HSTECH': '恒生科技指数',
        }
        self.hot_stocks = {
            '0700.HK': '腾讯控股',
            '9988.HK': '阿里巴巴',
            '3690.HK': '美团',
            '1810.HK': '小米集团',
            '9618.HK': '京东集团',
            '1024.HK': '快手',
            '2318.HK': '中国平安',
            '0005.HK': '汇丰控股',
        }
    
    def get_stock_data(self, symbol: str, name: str) -> Dict:
        """获取单个股票数据"""
        try:
            ticker = yf.Ticker(symbol)
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
                'symbol': symbol.replace('.HK', ''),
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
        """收集所有港股数据"""
        return {
            'indices': self.collect_indices(),
            'hot_stocks': self.collect_hot_stocks(),
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

if __name__ == '__main__':
    collector = HKStockCollector()
    data = collector.collect()
    print(f"Collected {len(data['indices'])} indices and {len(data['hot_stocks'])} stocks")
    for idx in data['indices']:
        print(f"- {idx['name']}: {idx['price']} ({idx['change_pct']}%)")
