# 🔑 Cloudflare API Token 配置指南

**目的**: 让 GitHub Actions 自动部署到 Cloudflare Pages

---

## 📋 步骤 1: 获取 Cloudflare API Token

### 1. 访问 Cloudflare Dashboard
https://dash.cloudflare.com/profile/api-tokens

### 2. 创建 API Token
- 点击「Create Token」
- 选择「Create Custom Token」
- 点击「Get started」

### 3. 配置权限
**Token name**: `GitHub Actions Deploy`

**Permissions**:
```
Account - Cloudflare Pages:Edit
Account - Cloudflare Workers:Write (可选)
```

**Account**:
- 选择你的账户
- 点击「Continue to summary」

### 4. 复制 Token
- 点击「Create Token」
- **立即复制 Token**（只显示一次！）
- 格式：`eyJ1......`

---

## 📋 步骤 2: 获取 Cloudflare Account ID

### 方法 1: 从 Dashboard 获取
1. 访问 https://dash.cloudflare.com/
2. 右侧边栏找到你的账户
3. Account ID 显示在账户名称下方

### 方法 2: 通过 API 获取
```bash
curl -X GET "https://api.cloudflare.com/client/v4/accounts" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

---

## 📋 步骤 3: 配置 GitHub Secrets

### 1. 访问仓库 Settings
https://github.com/dophanhan/avatar-broadcast-system-v2/settings/secrets/actions

### 2. 添加 Secrets

#### 添加 CLOUDFLARE_API_TOKEN
- 点击「New repository secret」
- **Name**: `CLOUDFLARE_API_TOKEN`
- **Value**: 步骤 1 中复制的 Token
- 点击「Add secret」

#### 添加 CLOUDFLARE_ACCOUNT_ID
- 点击「New repository secret」
- **Name**: `CLOUDFLARE_ACCOUNT_ID`
- **Value**: 步骤 2 中获取的 Account ID
- 点击「Add secret」

---

## 📋 步骤 4: 首次创建 Pages 项目

### 手动创建（只需一次）
1. 访问：https://dash.cloudflare.com/sign-up/pages
2. 点击「Connect to Git」
3. 选择仓库：`dophanhan/avatar-broadcast-system-v2`
4. 配置：
   - **Project name**: `avatar-broadcast-system-v2`
   - **Production branch**: `main`
   - **Build command**: 留空
   - **Build output directory**: `frontend`
5. 点击「Save and Deploy」

### 或者使用 Wrangler CLI（需要登录）
```bash
wrangler login
wrangler pages deploy ./frontend --project-name=avatar-broadcast-system-v2
```

---

## ✅ 验证部署

### 1. 检查 GitHub Actions
https://github.com/dophanhan/avatar-broadcast-system-v2/actions

- 查看「Deploy to Cloudflare Pages」工作流
- 确认运行状态为绿色 ✅

### 2. 检查 Cloudflare Pages
https://dash.cloudflare.com/?to=/:account/workers-and-pages/pages

- 找到项目 `avatar-broadcast-system-v2`
- 查看部署历史

### 3. 访问部署的页面
- 格式：`https://avatar-broadcast-system-v2.<subdomain>.workers.dev`
- 子域名在创建项目时自动生成

---

## 🔄 自动部署流程

```
GitHub Push → GitHub Actions → Wrangler Deploy → Cloudflare Pages
```

### 触发自动部署
```bash
cd /home/admin/.openclaw/workspace/avatar_broadcast_system_v2_dev
git add .
git commit -m "feat: 新功能"
git push origin main
```

GitHub Actions 会自动：
1. 检出代码
2. 安装 Wrangler
3. 部署到 Cloudflare Pages
4. 更新生产环境

---

## ⚠️ 注意事项

1. **API Token 安全**
   - 不要将 Token 提交到代码库
   - 只保存在 GitHub Secrets
   - 定期轮换 Token

2. **首次部署**
   - 需要先手动创建 Pages 项目（一次）
   - 后续部署自动进行

3. **部署目录**
   - 确保 `frontend` 目录存在
   - `index.html` 在 `frontend` 根目录

4. **环境变量**
   - 如需环境变量，在 Cloudflare Dashboard 设置
   - Settings → Environment variables

---

## 🔧 故障排查

### 问题 1: GitHub Actions 失败
**解决**:
- 检查 Secrets 配置是否正确
- 查看 Action 日志了解详细错误
- 确认 API Token 权限足够

### 问题 2: Cloudflare Pages 未更新
**解决**:
- 检查 GitHub Actions 是否运行
- 确认分支是 `main`
- 查看 Cloudflare 部署历史

### 问题 3: 404 错误
**解决**:
- 确认 `frontend` 目录结构正确
- 检查 `index.html` 是否存在
- 查看 Cloudflare 部署日志

---

## 📞 相关链接

- **Cloudflare API 文档**: https://api.cloudflare.com/
- **GitHub Actions 文档**: https://docs.github.com/en/actions
- **Wrangler 文档**: https://developers.cloudflare.com/workers/wrangler/
- **Pages 文档**: https://developers.cloudflare.com/pages/

---

**创建时间**: 2026-04-10 14:20  
**版本**: v2.0
