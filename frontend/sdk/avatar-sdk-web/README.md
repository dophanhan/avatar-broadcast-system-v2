# 讯飞虚拟人 Web SDK 目录

## 📥 如何获取 SDK

### 方式 1：从讯飞交互平台下载

1. 登录讯飞虚拟人交互平台：https://avatar.xfyun.cn/
2. 进入「开发者中心」→「SDK 下载」
3. 下载 Web SDK 安装包（avatar-sdk-web-x.x.x.zip）
4. 解压后将所有文件放入此目录

### 方式 2：从语雀文档下载

参考文档：https://www.yuque.com/xnrpt/bbc1du/ht4a2a2vstvb13se

文档中包含 SDK 下载链接和集成指南。

## 📁 所需文件

SDK 解压后应包含以下文件：

```
avatar-sdk-web/
├── index.js          # SDK 主文件（必需）
├── index.d.ts        # TypeScript 类型定义（可选）
├── README.md         # SDK 说明文档
└── ...               # 其他依赖文件
```

## ⚠️ 注意事项

1. **必须放置在此目录**：前端 HTML 通过 `./sdk/avatar-sdk-web/index.js` 引入 SDK
2. **版本要求**：建议使用 3.1.0 及以上版本
3. **移动端支持**：Web SDK 主要面向 PC 端和大屏，移动端支持有限

## 🔧 验证安装

部署后，打开浏览器控制台检查：

```javascript
console.log(window.AvatarSDK);
// 应该输出 SDK 模块对象
```

如果显示 `undefined`，说明 SDK 未正确加载，请检查：
1. 文件路径是否正确
2. 文件名称是否匹配
3. 服务器 MIME 类型配置
