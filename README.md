# EasyAgent

<div align="center"> 
  <p><strong>快速构建你的AI Agent！</strong></p> 
  <p>🐧交流群（QQ）：1040311839</p>
  <p>
    <img src="https://img.shields.io/badge/tests-76%20passed-green" alt="Tests">
    <img src="https://img.shields.io/badge/python-3.8+-blue" alt="Python">
  </p>
</div>

## 📖 项目简介

EasyAgent 是一个简单、灵活、易用的 Python AI Agent 框架，旨在帮助开发者快速构建强大的 AI 应用。遵循 Pythonic 的设计理念，EasyAgent 提供了一套直观的 API，使得创建和部署 AI Agent 变得前所未有的简单。

> **愿景**: 让每一位开发者都能轻松驾驭大语言模型，构建出真正有用的AI助手。

## 🏗️ 架构概览

EasyAgent 由以下核心组件构成:

- **Message**: 多模态消息处理，支持文本、图像等
- **Tool**: 工具接口，扩展 AI 能力
- **SDK**: 工具集合，方便管理多个工具
- **Service**: 服务层，包括上下文和记忆管理
- **LLM**: 模型包装层，支持 OpenAI 等大语言模型
- **Agent**: 核心组件，协调模型与工具交互

想了解更多，请阅读[设计文档](./docs/DESIGN.md)或[架构文档](./docs/ARCHITECTURE.md)。

## ✨ 功能特性

- 🔧 **丰富的工具**: 内置搜索引擎、计算器、天气查询等工具
- 🧠 **智能记忆**: 支持上下文管理和长短期记忆
- 🔄 **灵活扩展**: 易于添加自定义工具和 Agent
- 🧪 **完整测试**: 76 个单元测试，全面覆盖
- 🌐 **Web UI**: 可视化控制台（开发中）

## 🚀 快速开始

### 安装

```bash
pip install easy-agent
```

### 开发环境安装

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 快速开始示例

```python
from easyagent import OpenAILLM, ChatAgent, ChatSDK, SearchEngine, WeatherAPI

# 创建模型
llm = OpenAILLM(model_name="gpt-4", api_key="your_api_key")

# 创建工具
search_tool = SearchEngine()
weather_tool = WeatherAPI(api_key="your_weather_api_key")

# 创建SDK并添加工具
sdk = ChatSDK()
sdk.append(search_tool)
sdk.append(weather_tool)

# 创建Agent
agent = ChatAgent(model=llm, sdk=sdk)

# 使用Agent
response = agent("请告诉我今天北京的天气")
print(response.text)
```

### 更多示例

#### 使用上下文管理器

```python
from easyagent import OpenAILLM, ChatAgent, ContextManager

llm = OpenAILLM(model_name="gpt-4", api_key="your_api_key")
ctx = ContextManager(max_length=2000)

agent = ChatAgent(model=llm, context_manager=ctx)

# 多轮对话
agent("你好，我叫小明")
agent("你知道我的名字吗？")
```

#### 使用记忆管理器

```python
from easyagent import OpenAILLM, ChatAgent, MemoryManager

llm = OpenAILLM(model_name="gpt-4", api_key="your_api_key")
memory = MemoryManager(short_term_capacity=5)

agent = ChatAgent(model=llm)

# 添加重要信息到记忆
memory.add_message(TextMessage("我喜欢Python编程"), importance=0.9)

# 检索相关记忆
related = memory.retrieve(TextMessage("编程语言"))
```

## 📦 模块说明

| 模块 | 说明 | 状态 |
|------|------|------|
| `easyagent.messages` | 消息类型 (TextMessage, ImageMessage) | ✅ |
| `easyagent.tools` | 工具 (SearchEngine, Calculator, WeatherAPI) | ✅ |
| `easyagent.sdks` | 工具集合 (ChatSDK, MathSDK) | ✅ |
| `easyagent.services` | 服务 (ContextManager, MemoryManager) | ✅ |
| `easyagent.agents` | Agent (ChatAgent, SearchAgent) | ✅ |
| `easyagent.llms` | LLM (OpenAILLM) | ✅ |
| `easyagent.utils` | 工具函数 (logging, trans) | ✅ |
| `easyagent.webui` | Web 控制台 | 🔄 |

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_core.py -v

# 生成覆盖率报告
pytest --cov=easyagent
```

当前测试覆盖: **76 tests passed**

## 📁 项目结构

```
easyagent/
├── core/              # 核心基类
├── messages/          # 消息类型
├── tools/             # 工具实现
├── sdks/              # SDK实现
├── services/          # 服务实现
├── agents/            # Agent实现
├── utils/             # 工具函数
├── webui/             # Web UI
└── tests/             # 测试
```

## 🤝 如何贡献

我们非常欢迎各类贡献！

### 贡献步骤

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件

## 📬 联系我们

- **GitHub Issues**: [提交问题或建议](https://github.com/OpenEasyAgent/EasyAgent/issues)
- **QQ交流群**: 1040311839

---

<div align="center">
  <p>⭐️ 如果你喜欢这个项目，别忘了给它一个星！ ⭐️</p>
  <p>一起构建下一代AI应用！</p>
</div>
