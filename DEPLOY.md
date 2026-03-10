# 🚀 部署到 GitHub Pages

## 第一步：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名称：`ai-daily-report`
3. 选择 **Public**（公开）
4. 点击 **Create repository**

## 第二步：推送代码

```bash
# 在本地项目目录执行
cd /root/.openclaw/workspace/ai-daily-report

# 添加远程仓库
git remote add origin https://github.com/dede7228/ai-daily-report.git

# 推送代码
git branch -M main
git push -u origin main
```

## 第三步：配置 GitHub Pages

1. 打开仓库页面 → **Settings** → **Pages**
2. **Source** 选择 **GitHub Actions**
3. 等待首次部署完成

## 第四步：验证部署

- 访问 `https://dede7228.github.io/ai-daily-report/`
- 每天早8点会自动更新
- 也可以手动触发：Actions → Daily Report Generator → Run workflow

## 自定义域名（可选）

1. 在 `website/static/` 目录创建 `CNAME` 文件
2. 写入你的域名，如 `daily.yourdomain.com`
3. 在你的域名 DNS 添加 CNAME 记录指向 `YOUR_USERNAME.github.io`

## 配置说明

### 修改股票列表

编辑 `src/collectors/us_stocks.py` 和 `src/collectors/hk_stocks.py` 中的股票代码。

### 修改定时时间

编辑 `.github/workflows/daily-report.yml` 中的 cron 表达式：
- 当前：`0 0 * * *`（UTC 0点 = 北京时间早8点）

### 本地预览

```bash
# 生成日报
python src/main.py

# 本地预览网站
cd website && ./hugo server -D
```
