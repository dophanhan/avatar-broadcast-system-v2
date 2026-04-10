# 🚀 Cloudflare Pages 部署指南 - v2.0

**项目**: 数字人播报系统 v2.0  
**创建时间**: 2026-04-10 13:53

---

## 📋 部署步骤

### 方法 1：GitHub 自动部署（推荐）

1. **访问 Cloudflare Dashboard**
   - https://dash.cloudflare.com/sign-up/pages

2. **创建新项目**
   - 点击「Upload assets」或「Connect to Git」
   - 选择「Connect to Git」

3. **选择仓库**
   - 仓库：`dophanhan/avatar-broadcast-system-v2`
   - 分支：`main`
   - 点击「Begin setup」

4. **配置构建设置**
   - **Project name**: `avatar-broadcast-system-v2`
   - **Build command**: 留空（静态网站无需构建）
   - **Build output directory**: `frontend`
   - **Root Directory**: 留空

5. **环境变量（可选）**
   - 无需特殊环境变量

6. **保存并部署**
   - 点击「Save and Deploy」
   - 等待部署完成（约 1-2 分钟）

7. **获取域名**
   - 部署完成后，获得域名如：
   - `https://avatar-broadcast-system-v2.<subdomain>.workers.dev`

---

### 方法 2：手动上传（快速测试）

1. **打包前端文件**
```bash
cd /home/admin/.openclaw/workspace/avatar_broadcast_system_v2_dev/frontend
zip -r frontend.zip .
```

2. **访问 Cloudflare Pages**
   - https://dash.cloudflare.com/?to=/:account/workers-and-pages/pages

3. **创建项目**
   - 点击「Create a project」
   - 选择「Upload assets」
   - 上传 `frontend.zip`

4. **配置项目**
   - **Project name**: `avatar-broadcast-system-v2`
   - **Deploy**: 点击「Deploy site」

---

## 🔧 自定义域名（可选）

1. **访问项目设置**
   - 进入项目 → Settings → Custom domains

2. **添加域名**
   - 点击「Add custom domain」
   - 输入域名：`avatar-v2.example.com`
   - 点击「Add domain」

3. **配置 DNS**
   - 按照提示配置 CNAME 记录
   - 等待 DNS 传播（通常几分钟）

---

## 📊 项目信息

### GitHub 仓库
- **地址**: https://github.com/dophanhan/avatar-broadcast-system-v2
- **分支**: main
- **自动部署**: ✅ 已启用

### 阿里云函数
- **函数名称**: avatar-broadcast-v2
- **函数 ID**: e5ed24b3-57a1-4522-8fd4-32ac5c5e96af
- **函数 URL**: https://avatar-adcast-v-uzttmfxmdi.cn-hangzhou.fcapp.run
- **触发器**: avatar-api-v2

### 前端配置
- **API 地址**: https://avatar-adcast-v-uzttmfxmdi.cn-hangzhou.fcapp.run
- **讯飞接口服务 ID**: 300806204110802944
- **APP ID**: c9e63f7c

---

## 🎯 验证部署

### 1. 检查 Cloudflare 部署状态
- 访问项目页面查看部署历史
- 确认最新部署状态为「Ready」

### 2. 测试前端页面
```bash
curl -I https://avatar-broadcast-system-v2.<subdomain>.workers.dev
```

### 3. 测试 API 连接
```bash
curl -X POST https://avatar-adcast-v-uzttmfxmdi.cn-hangzhou.fcapp.run \
  -H "Content-Type: application/json" \
  -d '{"fullText":"测试","avatarId":"111204004","vcn":"x4_yezi"}'
```

应返回：
```json
{
  "code": 0,
  "data": {
    "appId": "c9e63f7c",
    "sceneId": "300806204110802944",
    ...
  }
}
```

---

## 🔄 自动部署流程

```
GitHub Push → Cloudflare Webhook → 自动构建 → 自动部署
```

### 触发自动部署
```bash
cd /home/admin/.openclaw/workspace/avatar_broadcast_system_v2_dev
git add .
git commit -m "feat: 新功能描述"
git push origin main
```

Cloudflare 会自动检测代码变更并重新部署。

---

## ⚠️ 注意事项

1. **部署目录**: 确保设置为 `frontend` 目录
2. **构建命令**: 留空（纯静态网站）
3. **缓存**: Cloudflare 自动缓存，更新代码后自动刷新
4. **HTTPS**: 自动启用，无需配置
5. **CORS**: 阿里云函数已配置 `ALLOW_ORIGIN = *`

---

## 📞 故障排查

### 问题 1：页面 404
**解决**：
- 检查 Build output directory 是否设置为 `frontend`
- 确认 `index.html` 在 `frontend` 根目录

### 问题 2：API 请求失败
**解决**：
- 检查前端代码中的 API URL 是否正确
- 确认阿里云函数运行正常
- 检查 CORS 配置

### 问题 3：部署失败
**解决**：
- 查看 Cloudflare 部署日志
- 确认文件结构正确
- 检查文件大小（不超过 500MB）

---

**创建人**: AI Assistant  
**创建时间**: 2026-04-10 13:53  
**版本**: v2.0
