# AI Domain Deep Research Agent

一个基于 Python 构建的 AI 深度研究 Agent 项目，旨在探索如何利用大语言模型与外部信息检索能力，辅助完成研究任务、信息收集与内容整理。

## ✨ 项目简介

AI Domain Deep Research Agent 将 Agent 逻辑、研究服务、数据解析和用户界面组织为独立模块，便于开发、测试和后续扩展。

项目集成了 DashScope 和 Tavily 相关配置，用于支持大模型调用及网络信息检索相关能力。

## 🚀 项目功能

- **Agent 模块**：组织 Agent 的创建逻辑与提示词。
- **研究服务**：集中处理研究任务相关的业务逻辑。
- **解析与数据模型**：负责结构化数据、解析逻辑及状态管理。
- **交互界面**：提供用户界面与内容渲染模块。
- **测试模块**：包含针对 Agent、工厂方法、解析器及研究服务的测试代码。
- **配置管理**：集中管理项目运行所需的配置。

> 具体功能以项目当前实现为准，后续可根据实际能力补充功能截图和使用示例。

## 🛠️ 技术栈

- Python
- 大语言模型接口：DashScope
- 信息检索：Tavily
- Python 虚拟环境与依赖管理
- 自动化测试：pytest（如项目测试依赖已配置）

## 📁 项目结构

```text
ai_domain_deep_research_agent/
├── agents/                 # Agent 创建逻辑与提示词
│   ├── factory.py
│   └── prompts.py
├── config/                 # 配置与常量
│   ├── constants.py
│   └── settings.py
├── core/                   # 核心模型、解析器、状态与异常
│   ├── exceptions.py
│   ├── models.py
│   ├── parser.py
│   └── state.py
├── services/               # 研究服务
│   └── research_service.py
├── tests/                  # 测试代码
├── ui/                     # 用户界面与内容渲染
├── app.py                  # 应用入口
├── requirements.txt        # Python 依赖
└── .gitignore              # Git 忽略规则
```

## 📋 环境要求

- Python 3.10 或更高版本（请以项目实际依赖要求为准）
- pip
- DashScope API Key
- Tavily API Key

## ⚙️ 安装与配置

### 1. 克隆项目

```bash
git clone https://github.com/LJY2600/ai_domain_deep_reaearch_agent.git
cd ai_domain_deep_reaearch_agent
```

### 2. 创建虚拟环境

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

如果虚拟环境已经创建并激活，可以跳过这一步。

### 3. 安装依赖

```bash
python -m pip install -r requirements.txt
```

### 4. 配置 API Key

在项目根目录创建 `.env` 文件，并根据项目实际读取的环境变量名称填写 API Key。

示例：

```dotenv
DASHSCOPE_API_KEY=your_dashscope_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**注意：** 上述变量名称仅为示例，请核对 `config/settings.py` 中实际使用的名称。如果项目使用其他环境变量名，应以代码为准。

API Key 获取入口：

- DashScope：<https://dashscope.console.aliyun.com/>
- Tavily：<https://tavily.com/>

请勿将真实 API Key 提交到 GitHub。确保 `.env` 已加入 `.gitignore`，也不要在 README、日志或截图中公开密钥。

## ▶️ 运行项目

应用入口为 `app.py`。请根据项目实际使用的 Web 框架启动应用。

如果项目使用 Streamlit，可尝试：

```bash
streamlit run app.py
```

如果项目使用其他框架，请以 `app.py` 中的启动方式为准。

## 🧪 运行测试

安装项目依赖后，可以使用 pytest 运行测试：

```bash
python -m pytest tests/
```

如果 pytest 尚未安装，请先安装对应测试依赖。

## 🔐 安全说明

- 不要将 `.env`、API Key 或其他凭证上传到公开仓库。
- 不要将虚拟环境目录 `.venv/` 提交到 Git。
- 不要将临时依赖目录、缓存文件或本地测试产物提交到仓库。
- 如果 API Key 意外泄露，请及时撤销或轮换。

## 🗺️ 后续计划

- [ ] 完善研究任务的输入与输出流程
- [ ] 优化研究结果的展示与整理
- [ ] 增加更多自动化测试
- [ ] 补充实际运行示例与界面截图
- [ ] 完善异常处理与配置校验

## 📄 License

目前尚未指定开源许可证。如计划公开发布或允许他人使用、修改和分发代码，建议根据项目需求选择合适的许可证。
