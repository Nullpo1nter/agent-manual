# agent-manual

一个简单的 Python 示例，演示如何调用 DeepSeek Chat Completions API 与大模型对话。

## 环境要求

- Python 3.10+
- [requests](https://pypi.org/project/requests/) 库

## 安装依赖

```bash
pip install requests
```

## 配置 API Key

在运行前设置环境变量 `DEEPSEEK_API_KEY`：

**Windows (PowerShell)**

```powershell
$env:DEEPSEEK_API_KEY = "your-api-key"
```

**Linux / macOS**

```bash
export DEEPSEEK_API_KEY="your-api-key"
```

## 运行

```bash
python FirstChat.py
```

脚本会发送一条示例问题（「请你用一句话介绍一下 Python」），并在终端打印模型回复及 token 用量。

## 文件说明

| 文件 | 说明 |
|------|------|
| `FirstChat.py` | 调用 DeepSeek API 的示例脚本 |
