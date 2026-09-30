# 康伴 · AI 个人健康问答助手

> 赛道：软件赛道 · 医药健康 —— **AI 个人健康问答助手**
>
> 基于 Streamlit + DeepSeek 大模型构建的可在线演示的健康科普与问答助手。

## 功能特性

| 模块 | 说明 |
|------|------|
| **智能问答** | 多轮对话，流式输出，支持建议追问引导 |
| **症状分诊** | 选择症状 / 持续时间 / 年龄 / 严重程度，生成初步参考建议 |
| **健康知识库** | 内置常见健康主题，支持关键词搜索与分类筛选 |
| **问答历史** | 查看本次会话记录，可导出为文本 |
| **安全护栏** | 紧急症状 / 心理危机识别，优先引导拨打 120 或求助热线 |

## 技术栈

- **前端界面**：Streamlit（原生组件 + 自定义主题）
- **大模型**：DeepSeek（OpenAI 兼容接口，`deepseek-chat` 模型）
- **语言**：Python 3.10+

## 快速开始（本地运行）

### 方式一：双击启动（推荐，零命令行）

在 Windows 上直接**双击 `启动助手.bat`**，脚本会自动安装依赖并启动应用，浏览器自动打开页面。

### 方式二：命令行

```bash
# 1. 进入项目目录
cd health-ai-assistant

# 2. 安装依赖（建议先创建虚拟环境）
pip install -r requirements.txt

# 3. 启动应用
streamlit run streamlit_app.py
```

启动后浏览器会自动打开 `http://localhost:8501`。

> **无需 API Key 也能运行**：未配置密钥时，应用会自动进入「演示模式」，内置示例回答，
> 保证作品**开箱即可演示**。

## 配置 DeepSeek API Key（启用完整智能问答）

1. 注册并获取 API Key：<https://platform.deepseek.com/>
2. 复制 `.streamlit/secrets.toml.example` 为 `.streamlit/secrets.toml`
3. 填入你的密钥：

```toml
DEEPSEEK_API_KEY = "sk-你的密钥"
```

4. 重启应用，侧边栏会显示「已连接 DeepSeek 大模型」。

## 部署为在线演示（Streamlit Cloud）

1. 将本项目推送到 GitHub 仓库（**不要提交 `secrets.toml`**，已在 `.gitignore` 中排除）。
2. 打开 <https://share.streamlit.io/>，点击 **Create app**，选择你的仓库与 `streamlit_app.py`。
3. 在 **Secrets** 中填入：

```toml
DEEPSEEK_API_KEY = "sk-你的密钥"
```

4. 部署完成后即可获得一个公开 URL，用于比赛在线演示。

## 目录结构

```
health-ai-assistant/
├── streamlit_app.py          # 应用入口（导航 + 全局状态 + 侧边栏）
├── 启动助手.bat               # 双击即可启动（自动装依赖+运行）
├── app_pages/
│   ├── chat.py               # 智能问答
│   ├── triage.py             # 症状分诊
│   ├── knowledge.py          # 健康知识库 + 问答历史
│   └── about.py              # 安全与免责说明
├── utils/
│   ├── deepseek.py           # DeepSeek 接入 + 演示模式回退
│   ├── safety.py             # 紧急症状 / 心理危机识别
│   └── knowledge_base.py     # 内置健康知识库数据
├── .streamlit/
│   ├── config.toml           # 主题配置
│   └── secrets.toml.example  # 密钥模板（复制为 secrets.toml 使用）
├── requirements.txt
└── README.md
```

## 安全设计说明

健康类应用的核心是「不误导」。本作品内置了如下护栏：

- **紧急症状识别**：检测到胸痛、呼吸困难、大出血、意识丧失、中风征兆等表述时，
  **优先引导拨打 120 或就近急诊**，而非由 AI 给出常规建议。
- **心理危机识别**：检测到自杀 / 自残等倾向时，优先提供心理援助热线与陪伴引导。
- **常驻免责声明**：所有页面顶部与侧边栏均提示「不构成医疗建议」。
- **提示词约束**：系统提示词明确要求 AI 不诊断、不处方、不替代医生。

## 免责声明

本产品仅用于健康科普与一般性健康管理参考，**不构成医疗建议**，不能替代执业医师的诊断与治疗。
如有身体不适，请及时到正规医疗机构就诊；紧急情况请拨打 **120**。
