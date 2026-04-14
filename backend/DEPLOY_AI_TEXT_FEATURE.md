# AI 生成播报文本功能 - 后端部署说明

## 📦 部署包信息

**文件名**: `function-v8-ai-text.zip`
**大小**: 6.1KB
**上传时间**: 2026-04-14 16:57
**OSS URL**: https://avatar-broadcast-v2.oss-cn-hangzhou.aliyuncs.com/function-codes/function-v8-ai-text.zip

---

## 🚀 部署步骤

### 方式 1：阿里云控制台手动更新（推荐）

1. **登录阿里云函数计算控制台**
   - 地址：https://fcnext.console.aliyun.com/
   - 地域：**华东 1（杭州）**

2. **找到服务**
   - 服务名称：`avatar-broadcast-v2`
   - 函数名称：`avatar-broadcast-v2`（或你的函数名）

3. **更新函数代码**
   - 点击「代码」标签页
   - 点击「上传 ZIP 包」
   - 选择本地文件：`backend/function-v8-ai-text.zip`
   - 或者从 OSS 选择：`oss://avatar-broadcast-v2/function-codes/function-v8-ai-text.zip`
   - 点击「确定」

4. **配置环境变量**（如果未配置）
   - 点击「配置」标签页
   - 找到「环境变量」部分
   - 添加以下变量：
     ```
     DOUBAO_API_KEY=9bfb84f3-c0e4-493a-b10c-404a6a7f7559
     DOUBAO_MODEL_ID=ep-m-20260411125426-288zp
     ```
   - 点击「保存」

5. **保存并部署**
   - 点击「保存并部署」按钮
   - 等待部署完成（约 30 秒）

---

### 方式 2：使用阿里云 CLI

```bash
# 安装阿里云 CLI（如果未安装）
pip install aliyun-cli

# 配置凭证
aliyun configure

# 更新函数
aliyun fc function update \
  --service-name avatar-broadcast-v2 \
  --function-name avatar-broadcast-v2 \
  --code-file function-v8-ai-text.zip \
  --region cn-hangzhou
```

---

## ✅ 验证部署

### 1. 测试 API 端点

```bash
curl -X POST "https://你的函数地址.cn-hangzhou.fcapp.run/ai/generate-broadcast-text" \
  -H "Content-Type: application/json" \
  -d '{
    "ppt_pages": [
      {
        "page_num": 1,
        "page_title": "封面",
        "page_text": "公司介绍"
      }
    ],
    "ppt_title": "测试 PPT",
    "total_pages": 1
  }'
```

### 2. 预期响应

```json
{
  "code": 0,
  "data": {
    "broadcast_text": "尊敬的各位来宾，大家好。欢迎参加本次产品介绍会..."
  }
}
```

---

## 📝 新增功能说明

### API 端点
- **路径**: `/ai/generate-broadcast-text`
- **方法**: `POST`
- **描述**: AI 生成播报文本

### 请求参数
```json
{
  "ppt_pages": [
    {
      "page_num": 1,
      "page_title": "页面标题",
      "page_text": "页面内容"
    }
  ],
  "ppt_title": "PPT 标题",
  "total_pages": 1
}
```

### 响应格式
```json
{
  "code": 0,
  "data": {
    "broadcast_text": "生成的播报文本"
  }
}
```

---

## ⚠️ 注意事项

1. **环境变量必须配置**
   - `DOUBAO_API_KEY`: 豆包 API Key
   - `DOUBAO_MODEL_ID`: 豆包模型 ID

2. **超时设置**
   - 函数超时时间建议设置为 60 秒
   - 豆包 API 调用超时为 30 秒

3. **依赖库**
   - `requests` 已在 requirements.txt 中

4. **提示词**
   - 使用最终版四项核心准则提示词
   - 严格遵循讯飞数字人播报合规要求

---

## 🔧 故障排查

### 问题 1：未配置豆包 API
**错误**: `未配置豆包 API Key 或 Model ID`
**解决**: 检查环境变量是否正确配置

### 问题 2：API 调用失败
**错误**: `豆包 API 调用失败：{...}`
**解决**: 
- 检查 API Key 是否正确
- 检查 Model ID 是否正确
- 查看函数日志

### 问题 3：生成文本包含 Markdown
**解决**: 后处理代码已自动清理，如仍有问题检查提示词

---

**部署时间**: 2026-04-14
**版本**: v8-AI-Text-Generate
**备份位置**: `backup_before_ai_generate_20260414_1653/`
