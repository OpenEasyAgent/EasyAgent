# EasyAgent

<div align="center"> 
  <p><strong>快速构建你的AI Agent！</strong></p> 
  <p>🐧交流群（QQ）：1040311839</p>
</div>

## 📖 项目简介

EasyAgent 是一个简单、灵活、易用的 Python AI Agent 框架，旨在帮助开发者快速构建强大的 AI 应用。遵循 Pythonic 的设计理念，EasyAgent 提供了一套直观的 API，使得创建和部署 AI Agent 变得前所未有的简单。

> **愿景**: 让每一位开发者都能轻松驾驭大语言模型，构建出真正有用的AI助手。

## 🚧 项目现状

EasyAgent 目前处于 **早期开发阶段**。我们已经:

- ✅ 完成了核心架构设计
- ✅ 定义了主要模块接口
- ✅ 开始实现基础组件

正在进行中:

- 🔄 实现核心模块功能
- 🔄 编写基础文档
- 🔄 设计示例应用
- 🔄 实现Web UI程序调试台
- 🔄 实现日志功能

## 🏗️ 架构概览

EasyAgent 由以下核心组件构成:

- **Model**: 模型包装层，支持 OpenAI、千问等大语言模型
- **Message**: 多模态消息处理，支持文本、图像等
- **Tool**: 工具接口，扩展 AI 能力
- **SDK**: 工具集合，方便管理多个工具
- **Service**: 服务层，包括上下文和记忆管理
- **Agent**: 核心组件，协调模型与工具交互
- 想了解更多，请阅读[结构文档](./docs/ARCHITECTURE.md)

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
from easyagent.models import OpenAILLM
from easyagent.tools import SearchEngine, WeatherAPI
from easyagent.agents import ChatAgent
from easyagent.sdks import ChatSDK

# 创建模型
llm = OpenAILLM(model_name="gpt-4", api_key="your_api_key")

# 创建工具
search_tool = SearchEngine(engine="google")
weather_tool = WeatherAPI(api_key="your_weather_api_key")

# 创建SDK并添加工具
sdk = ChatSDK()
sdk.append(search_tool)
sdk.append(weather_tool)

# 创建Agent
agent = ChatAgent(model=llm, sdk=sdk)

# 使用Agent
response = agent("请告诉我今天北京的天气，以及有什么适合这种天气的户外活动")
print(response)
```

## 🤝 如何贡献

我们非常欢迎各类贡献，无论是代码、文档还是创意！

### 我们需要:

1. **开发者**: 帮助实现核心功能和工具接口
2. **文档贡献者**: 改进文档和撰写教程
3. **测试者**: 尝试使用框架并反馈问题
4. **创意贡献者**: 提供新功能想法和改进建议

### 贡献步骤:

1. Fork 本仓库  
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)  
3. 提交你的更改 (`git commit -m 'Add some amazing feature'`)  
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