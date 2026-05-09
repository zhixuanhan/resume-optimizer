# 简历优化助手 - 部署指南

## 方案1：部署到 Railway（推荐 ⭐⭐⭐）

Railway 支持完整 Flask + 文件存储，适合本应用。

### 步骤：

**1. 注册 Railway**
- 访问 https://railway.app 并用 GitHub 账号登录
- 有免费额度（每月 500 小时）

**2. 创建新项目**
- 点击 "New Project" → "Deploy from GitHub repo"
- 选择这个项目仓库

**3. 配置环境变量**
- 在 Railway 控制台找到 "Variables"
- 添加：`SILICONFLOW_API_KEY` = 你的 API Key
  - 可以去 https://siliconflow.cn 申请（免费额度）
  - 或者继续用现有的（但不推荐生产环境）

**4. 部署**
- Railway 会自动检测 Dockerfile 并部署
- 等待 2-3 分钟完成
- 获取公网 URL：https://xxx.railway.app

**5. 分享给朋友**
- 直接发这个 URL 就能用！

---

## 方案2：部署到 Render

### 步骤：

**1. 注册 Render**
- 访问 https://render.com 并用 GitHub 账号登录

**2. 创建 Web Service**
- 点击 "New" → "Web Service"
- 连接 GitHub 仓库

**3. 配置**
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- 记得添加环境变量 `SILICONFLOW_API_KEY`

**4. 部署完成获取 URL**

---

## 方案3：ngrok（临时内网穿透）

如果只是想临时分享给朋友用，可以安装 ngrok：

**1. 注册 ngrok**
- 访问 https://ngrok.com 注册（免费）
- 获取 authtoken

**2. 安装并运行**
```bash
ngrok http 5000
```

**3. 复制 ngrok 提供的 URL 分享**

---

## 方案4：内网穿透 cpolar

类似 ngrok，需要注册获取 authtoken。

---

## 技术说明

本应用使用：
- **Flask** - Web 框架
- **PyPDF2 / pdfplumber** - PDF 解析
- **SiliconFlow API** - AI 生成（需要 API Key）
- **Gunicorn** - WSGI 服务器

部署后即可通过公网 URL 访问，支持简历上传、诊断、岗位分析、简历优化、面试话术生成等功能。
