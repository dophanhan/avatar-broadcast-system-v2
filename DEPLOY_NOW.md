# 🚀 Cloudflare Pages 快速部署指南

**Token 已配置**: ✅  
**Account ID**: `a8a216caf165001ecfceae49382b3c7c`

---

## 📋 方法 1: 手动创建（推荐，只需 2 分钟）

### 步骤 1: 访问 Cloudflare Pages
https://dash.cloudflare.com/sign-up/pages

### 步骤 2: 连接 GitHub
1. 点击「Connect to Git」
2. 授权 Cloudflare 访问 GitHub
3. 选择仓库：`dophanhan/avatar-broadcast-system-v2`
4. 点击「Begin setup」

### 步骤 3: 配置项目
- **Project name**: `avatar-broadcast-system-v2`
- **Production branch**: `main`
- **Build command**: 留空
- **Build output directory**: `frontend`
- **Root Directory**: 留空

### 步骤 4: 部署
1. 点击「Save and Deploy」
2. 等待 1-2 分钟
3. 获得域名：`https://avatar-broadcast-system-v2.<subdomain>.workers.dev`

---

## 📋 方法 2: 使用 Wrangler CLI

### 安装 Wrangler
```bash
npm install -g wrangler
```

### 登录 Cloudflare
```bash
wrangler login
```

### 部署项目
```bash
cd /home/admin/.openclaw/workspace/avatar_broadcast_system_v2_dev/frontend
wrangler pages deploy . --project-name=avatar-broadcast-system-v2
```

---

## 📋 方法 3: GitHub Actions（需要配置 Secrets）

### 配置 GitHub Secrets

访问：https://github.com/dophanhan/avatar-broadcast-system-v2/settings/secrets/actions

添加以下 Secrets：

1. **CLOUDFLARE_API_TOKEN**
   - Value: `R9BKi_CC3lEfQMXOmX8UNd6d7p5pYhy8XwA3CPME`

2. **CLOUDFLARE_ACCOUNT_ID**
   - Value: `a8a216caf165001ecfceae49382b3c7c`

### 自动部署
配置完成后，每次 push 到 main 分支都会自动部署。

---

## ✅ 验证部署

### 1. 检查项目
https://dash.cloudflare.com/?to=/:account/workers-and-pages/pages

找到 `avatar-broadcast-system-v2` 项目

### 2. 访问页面
格式：`https://avatar-broadcast-system-v2.<subdomain>.workers.dev`

### 3. 测试 API 连接
打开页面，输入测试文本，检查是否能正常播报

---

## 🎯 推荐方案

**立即执行**：方法 1（手动创建）
- 只需 2 分钟
- 直观简单
- 一次配置，永久自动部署

**后续优化**：方法 3（GitHub Actions）
- 配置 Secrets 后完全自动化
- 适合频繁更新

---

**创建时间**: 2026-04-10 14:22  
**状态**: 等待 Cloudflare Pages 创建
