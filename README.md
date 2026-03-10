# AI Daily Report

AI + 金融股票（美股/港股）每日自动日报

## 功能

- 🤖 AI 新闻聚合
- 📈 美股行情速览
- 🇭🇰 港股行情速览
- 📊 AI 智能分析
- 🌐 自动发布到 GitHub Pages

## 访问地址

https://[your-github-username].github.io/ai-daily-report/

## 技术栈

- Python 3.12
- Hugo 静态网站生成器
- GitHub Actions 定时任务
- SearXNG 搜索
- yfinance 股票数据

## 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 生成日报
python src/main.py

# 本地预览网站
cd website && hugo server -D
```

## 许可证

MIT
