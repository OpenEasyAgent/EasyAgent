# EasyAgent 设计文档

## 1. 项目概述

### 1.1 项目背景与目标

EasyAgent 是一个简单、灵活、易用的 Python AI Agent 框架，旨在帮助开发者快速构建强大的 AI 应用。遵循 Pythonic 的设计理念，EasyAgent 提供了一套直观的 API，使得创建和部署 AI Agent 变得前所未有的简单。

**愿景**: 让每一位开发者都能轻松驾驭大语言模型，构建出真正有用的AI助手。

### 1.2 项目现状

- ✅ 完成了核心架构设计
- ✅ 定义了主要模块接口
- ✅ 实现基础组件（Message, LLM, Core基类）
- ✅ 实现 WebUI 基础框架

**正在进行中**:
- 🔄 实现核心模块功能
- 🔄 编写基础文档
- 🔄 设计示例应用
- 🔄 实现Web UI程序调试台
- 🔄 实现日志功能

---

## 2. 架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         EasyAgent                               │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐         │
│  │  Agent  │   │   LLM   │   │   SDK   │   │ Service │         │
│  └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘         │
│       │             │             │             │              │
│       └─────────────┴──────┬──────┴─────────────┘              │
│                            │                                    │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐         │
│  │ Message │   │  Tool  │   │   API   │   │   Log   │         │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                      WebUI Layer                         │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 核心设计原则

1. **简单 (Simple)**: 保持API简洁易用，降低学习成本
2. **灵活 (Flexible)**: 支持自定义扩展，满足不同需求
3. **易用 (Usable)**: 遵循Pythonic设计理念，符合开发者习惯

---

## 3. 模块设计

### 3.1 Core 模块 (核心基类)

**文件位置**: `easyagent/core/base.py`

#### 3.1.1 Tool 基类

```python
class Tool(ABC):
    """工具基类，所有工具应继承此类"""
    __tool_schema: Dict[str, Any] = {}
    
    @property
    def schema(self) -> Dict[str, Any]:
        """返回工具的schema定义"""
        
    @abstractmethod
    def call(self, *args, **kwargs):
        """调用工具的方法，必须由子类实现"""
```

**设计说明**:
- Tool 是 AI Agent 扩展能力的核心抽象
- `__tool_schema` 用于定义工具的 OpenAI Function Calling 格式
- 支持直接调用（`__call__`）和通过 Agent 调用两种方式

**扩展实现示例**:
- `SearchEngine`: 搜索引擎工具
- `Calculator`: 计算器工具
- `WeatherAPI`: 天气查询工具

#### 3.1.2 Message 基类

```python
class Message(ABC):
    """消息基类，所有消息类型应继承此类"""
    __message_schema: Dict[str, Any] = {}
    
    def __init__(self, source: str = "system") -> None:
        self.source = source
        
    @property
    def schema(self) -> Dict[str, Any]:
        """返回消息的schema定义"""
```

**设计说明**:
- Message 支持多模态消息处理
- `source` 属性标识消息来源（system/user/assistant）
- 已实现子类：`TextMessage`, `ImageMessage`

#### 3.1.3 SDK 基类

```python
class SDK(ABC):
    """SDK基类，所有SDK应继承此类"""
    __sdk_schema: Dict[str, Any] = {}
    
    @property
    def schema(self) -> Dict[str, Any]:
        """返回SDK的schema定义"""
```

**设计说明**:
- SDK 是工具的集合，方便管理多个相关工具
- 支持动态添加工具（`append` 方法）
- 已规划实现：`ChatSDK`, `MathSDK`

#### 3.1.4 Service 基类

```python
class Service(ABC):
    """服务基类，所有服务应继承此类"""
    __service_schema: Dict[str, Any] = {}
    
    @abstractmethod
    def call(self, *args, **kwargs):
        """调用服务的方法，必须由子类实现"""
```

**设计说明**:
- Service 提供辅助功能，如上下文管理、记忆管理等
- 已规划实现：`ContextManager`, `MemoryManager`

#### 3.1.5 Agent 基类

```python
class Agent(ABC):
    """Agent基类，所有Agent应继承此类"""
    __agent_schema: Dict[str, Any] = {}
    
    @abstractmethod
    def call(self, *args, **kwargs):
        """调用Agent的方法，必须由子类实现"""
```

**设计说明**:
- Agent 是核心组件，协调模型与工具的交互
- 支持直接调用（`__call__`）方式触发 Agent
- 已规划实现：`ChatAgent`, `SearchAgent`

---

### 3.2 Messages 模块 (消息实现)

**文件位置**: 
- `easyagent/messages/text.py`
- `easyagent/messages/image.py`
- `easyagent/messages/structure.py`

#### 3.2.1 TextMessage

```python
class TextMessage(Message):
    """文本消息类"""
    __message_schema = {
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "文本内容"}
        },
        "required": ["text"]
    }
    
    def __init__(self, text: str, source: str = "system") -> None:
        super().__init__(source=source)
        self.text = text
```

**已实现特性**:
- 加法运算重载 (`+`, `+=`)
- 长度计算重载 (`len()`)
- 索引访问重载 (`[]`)
- 包含判断重载 (`in`)
- 相等判断重载 (`==`, `!=`)
- 字符串表示 (`__str__`, `__repr__`)

#### 3.2.2 ImageMessage

**设计说明**:
- 支持图像消息处理
- 包含 `img_url` 或图像二进制数据
- 规划实现 `save()` 方法用于保存图像

#### 3.2.3 StructureMessage

**设计说明**:
- 支持结构化数据消息
- 用于返回 JSON 等结构化信息

---

### 3.3 Agents 模块 (Agent 实现)

**文件位置**: `easyagent/agents/llms.py`

#### 3.3.1 LLM 基类

```python
class LLM(Agent):
    """LLM（大语言模型）基类，所有LLM应继承此类"""
    __agent_schema = {
        "type": "object",
        "properties": {
            "model_name": {"type": "string", "description": "模型名称"},
            "api_key": {"type": "string", "description": "API密钥"}
        },
        "required": ["model_name", "api_key"]
    }
    
    def call(self, prompt: TextMessage | List[TextMessage]) -> TextMessage:
        """调用LLM生成文本"""
```

#### 3.3.2 OpenAILLM

```python
class OpenAILLM(LLM):
    """OpenAI LLM实现"""
    
    def __init__(self,
                 model_name: str,
                 api_key: str,
                 temperature: float = 0.7,
                 max_tokens: int = 150,
                 top_p: float = 1.0,
                 frequency_penalty: float = 0.0,
                 presence_penalty: float = 0.0,
                 stop: list | None = None) -> None:
```

**已实现功能**:
- 支持 OpenAI ChatGPT 模型调用
- 支持所有 OpenAI API 参数
- 自动将 TextMessage 转换为 OpenAI 消息格式
- 依赖 `openai` Python 包

**规划扩展**:
- `QianwenLLM`: 阿里千问模型支持
- `ClaudeLLM`: Anthropic Claude 模型支持
- `GeminiLLM`: Google Gemini 模型支持

#### 3.3.3 ChatAgent

**设计说明**:
- 通用聊天 Agent
- 支持多轮对话
- 支持工具调用

#### 3.3.4 SearchAgent

**设计说明**:
- 搜索专用 Agent
- 自动选择合适的搜索工具

---

### 3.4 Tools 模块

**文件位置**: `easyagent/tools/`

**规划实现**:

#### 3.4.1 SearchEngine

```python
class SearchEngine(Tool):
    """搜索引擎工具"""
    __tool_schema = {
        "name": "search_engine",
        "description": "搜索互联网信息",
        "parameters": {
            "query": {"type": "string", "description": "搜索关键词"},
            "engine": {"type": "string", "description": "搜索引擎类型"}
        }
    }
    
    def __init__(self, engine: str = "google"):
        self.engine = engine
        
    def call(self, query: str) -> TextMessage:
        """执行搜索并返回结果"""
```

#### 3.4.2 Calculator

```python
class Calculator(Tool):
    """计算器工具"""
    
    def call(self, expression: str) -> TextMessage:
        """计算数学表达式并返回结果"""
```

#### 3.4.3 WeatherAPI

```python
class WeatherAPI(Tool):
    """天气查询工具"""
    
    def call(self, city: str) -> TextMessage:
        """查询指定城市的天气信息"""
```

---

### 3.5 SDKs 模块

**文件位置**: `easyagent/sdks/`

#### 3.5.1 ChatSDK

```python
class ChatSDK(SDK):
    """聊天SDK，包含聊天相关的工具集合"""
    
    def __init__(self):
        self.tools: List[Tool] = []
        
    def append(self, tool: Tool) -> None:
        """添加工具到SDK"""
        self.tools.append(tool)
    
    def get_tools_schema(self) -> List[Dict]:
        """获取所有工具的schema定义"""
```

#### 3.5.2 MathSDK

**设计说明**:
- 数学相关工具集合
- 包含 Calculator 等工具

---

### 3.6 Services 模块

**文件位置**: `easyagent/services/`

#### 3.6.1 ContextManager

```python
class ContextManager(Service):
    """上下文管理器，控制对话上下文长度"""
    
    def __init__(self, max_length: int = 4096):
        self.max_length = max_length
        self.messages: List[TextMessage] = []
        
    def add_message(self, message: TextMessage) -> None:
        """添加消息到上下文"""
        
    def get_context(self) -> List[TextMessage]:
        """获取当前上下文"""
        
    def call(self, prompt: TextMessage) -> TextMessage:
        """处理输入并返回上下文相关的响应"""
```

**设计说明**:
- 管理对话历史
- 自动截断超长上下文
- 支持不同策略（最早消息保留、最近消息保留等）

#### 3.6.2 MemoryManager

```python
class MemoryManager(Service):
    """记忆管理器，实现长中短期记忆"""
    
    def __init__(self, 
                 short_term_capacity: int = 10,
                 long_term_capacity: int = 100):
        self.short_term: List[TextMessage] = []
        self.long_term: List[TextMessage] = []
        
    def add_to_short_term(self, message: TextMessage) -> None:
        """添加到短期记忆"""
        
    def consolidate_to_long_term(self) -> None:
        """将短期记忆整合到长期记忆"""
        
    def retrieve(self, query: TextMessage) -> List[TextMessage]:
        """根据查询检索记忆"""
```

**设计说明**:
- 短期记忆：最近N轮对话
- 长期记忆：重要信息持久化存储
- 支持记忆检索和总结

---

### 3.7 Utils 模块

**文件位置**: `easyagent/utils/`

#### 3.7.1 trans (翻译工具)

```python
def text_list_to_openai_messages(messages: List[TextMessage]) -> List[Dict]:
    """将TextMessage列表转换为OpenAI API格式"""
```

#### 3.7.2 logging (日志功能)

**规划实现**:
- 统一日志管理
- 支持日志级别配置
- 支持日志输出到文件/控制台

#### 3.7.3 config (配置功能)

**规划实现**:
- 配置文件管理
- 环境变量支持
- 默认配置管理

---

### 3.8 WebUI 模块

**文件位置**: `easyagent/webui/`

#### 3.8.1 架构设计

```
webui/
├── __init__.py          # Flask 应用初始化
├── routes.py            # 路由定义
├── templates/           # HTML 模板
│   └── dashboard.html   # 主控制面板
├── static/              # 静态资源
│   ├── css/
│   │   └── dashboard.css
│   ├── js/
│   │   └── dashboard.js
│   └── img/
└── utils/
    └── monitor.py       # 系统监控工具
```

#### 3.8.2 API 路由设计

| 路由 | 方法 | 说明 |
|------|------|------|
| `/dashboard` | GET | 渲染控制面板页面 |
| `/api/agent/status` | GET | 获取所有 Agent 运行状态 |
| `/api/model/update` | POST | 更新模型参数 |
| `/api/agent/create` | POST | 创建新 Agent |
| `/api/agent/delete` | DELETE | 删除 Agent |
| `/api/tool/register` | POST | 注册新工具 |

#### 3.8.3 SystemMonitor

```python
class SystemMonitor:
    """系统监控工具"""
    
    @staticmethod
    def get_agents_status() -> Dict:
        """获取所有Agent的状态"""
        
    @staticmethod
    def get_model_info() -> Dict:
        """获取当前模型信息"""
        
    @staticmethod
    def get_system_metrics() -> Dict:
        """获取系统指标（CPU、内存等）"""
```

#### 3.8.4 前端功能设计

**Dashboard 页面功能**:
1. Agent 列表展示与管理
2. 模型参数配置面板
3. 对话历史查看
4. 工具注册与管理
5. 系统状态监控
6. 实时日志查看

---

## 4. 使用示例

### 4.1 基础聊天

```python
from easyagent.models import OpenAILLM
from easyagent.agents import ChatAgent

# 创建模型
llm = OpenAILLM(model_name="gpt-4", api_key="your_api_key")

# 创建Agent
agent = ChatAgent(model=llm)

# 使用Agent
response = agent("你好，请介绍一下你自己")
print(response.text)
```

### 4.2 带工具的聊天

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
print(response.text)
```

### 4.3 自定义工具

```python
from easyagent.core.base import Tool
from easyagent.messages import TextMessage, ImageMessage

class GetPaint(Tool):
    """对Tool基类进行二次开发，实现了从文本生成图片"""
    
    __tool_schema = {
        "name": "get_paint",
        "description": "get a paint about a string 'query'.",
        "parameters": [
            {
                "name": "query",
                "type": "str",
                "description": "the paint's theme."
            }
        ]
    }

    def __init__(self, model):
        super().__init__()
        self.model = model
    
    def call(self, query: str) -> ImageMessage:
        return self.model(query)

# 使用自定义工具
paint_model = StableDiffusion(...)
language_model = OpenAILLM(base_url="xxx", api_key="xxx", temperature=0.7)

paint_tool = GetPaint(model=paint_model)
sdk = ChatSDK()
sdk.append(paint_tool)

agent = ChatAgent(model=language_model, sdk=sdk)
response = agent("Give me a picture about a cat girl")
response.save("cat_girl.jpg")
```

---

## 5. API 参考

### 5.1 Message API

| 类名 | 说明 | 关键方法 |
|------|------|----------|
| `Message` | 消息基类 | `schema`, `set_source` |
| `TextMessage` | 文本消息 | `text`, `source`, `+`, `+=`, `len`, `[]`, `in`, `==` |
| `ImageMessage` | 图像消息 | `img_url`, `save` |

### 5.2 Tool API

| 类名 | 说明 | 关键方法 |
|------|------|----------|
| `Tool` | 工具基类 | `schema`, `call` |
| `SearchEngine` | 搜索引擎 | `call(query)` |
| `Calculator` | 计算器 | `call(expression)` |
| `WeatherAPI` | 天气查询 | `call(city)` |

### 5.3 SDK API

| 类名 | 说明 | 关键方法 |
|------|------|----------|
| `SDK` | SDK基类 | `schema`, `append`, `get_tools_schema` |
| `ChatSDK` | 聊天SDK | 继承自SDK |
| `MathSDK` | 数学SDK | 继承自SDK |

### 5.4 Service API

| 类名 | 说明 | 关键方法 |
|------|------|----------|
| `Service` | 服务基类 | `schema`, `call` |
| `ContextManager` | 上下文管理 | `add_message`, `get_context` |
| `MemoryManager` | 记忆管理 | `add_to_short_term`, `consolidate_to_long_term`, `retrieve` |

### 5.5 Agent API

| 类名 | 说明 | 关键方法 |
|------|------|----------|
| `Agent` | Agent基类 | `schema`, `call` |
| `LLM` | 大语言模型基类 | `call(prompt)` |
| `OpenAILLM` | OpenAI实现 | 继承自LLM，支持完整OpenAI参数 |
| `ChatAgent` | 聊天Agent | 继承自Agent |
| `SearchAgent` | 搜索Agent | 继承自Agent |

---

## 6. 扩展指南

### 6.1 添加新的 LLM 支持

```python
from easyagent.agents.llms import LLM
from easyagent.messages import TextMessage

class CustomLLM(LLM):
    """自定义LLM实现"""
    
    __agent_schema = {
        "type": "object",
        "properties": {
            "model_name": {"type": "string"},
            "api_key": {"type": "string"},
            # 自定义参数...
        },
        "required": ["model_name", "api_key"]
    }
    
    def __init__(self, model_name: str, api_key: str, **kwargs):
        super().__init__(model_name, api_key)
        # 初始化自定义参数
        
    def call(self, prompt: TextMessage | List[TextMessage]) -> TextMessage:
        # 实现模型调用逻辑
        pass
```

### 6.2 添加新的 Tool

```python
from easyagent.core.base import Tool
from easyagent.messages import TextMessage

class CustomTool(Tool):
    """自定义工具"""
    
    __tool_schema = {
        "name": "custom_tool",
        "description": "工具描述",
        "parameters": {
            "param1": {"type": "string", "description": "参数1描述"},
            "param2": {"type": "integer", "description": "参数2描述"}
        }
    }
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def call(self, param1: str, param2: int = 0) -> TextMessage:
        # 实现工具逻辑
        pass
```

### 6.3 添加新的 Agent 类型

```python
from easyagent.core.base import Agent
from easyagent.messages import TextMessage

class CustomAgent(Agent):
    """自定义Agent"""
    
    __agent_schema = {
        "type": "object",
        "properties": {
            "model": {"type": "object"},
            "sdk": {"type": "object"},
            # 自定义属性
        },
        "required": ["model"]
    }
    
    def __init__(self, model, sdk=None, **kwargs):
        super().__init__()
        self.model = model
        self.sdk = sdk
        
    def call(self, prompt: TextMessage) -> TextMessage:
        # 实现Agent逻辑
        pass
```

---

## 7. 未来规划

### 7.1 短期目标

- [ ] 完成 Tool 模块实现（SearchEngine, Calculator, WeatherAPI）
- [ ] 完成 SDK 模块实现（ChatSDK, MathSDK）
- [ ] 完成 Service 模块实现（ContextManager, MemoryManager）
- [ ] 完成 ChatAgent 和 SearchAgent 实现
- [ ] 完善 Web UI 控制台功能
- [ ] 添加日志功能

### 7.2 中期目标

- [ ] 添加更多 LLM 支持（Qianwen, Claude, Gemini）
- [ ] 添加更多 Tool 实现（文件处理、代码执行等）
- [ ] 添加异步支持
- [ ] 添加流式输出支持
- [ ] 添加单元测试

### 7.3 长期目标

- [ ] 支持多 Agent 协作
- [ ] 添加 Agent 市场/社区
- [ ] 支持插件系统
- [ ] 添加可视化工作流编辑器
- [ ] 性能优化

---

## 8. 配置文件

### 8.1 项目配置

```toml
# pyproject.toml
[project]
name = "easy-agent"
version = "0.1.0"
description = "快速构建你的AI Agent"
requires-python = ">=3.8"
```

### 8.2 依赖项

**核心依赖**:
- `openai` - OpenAI API 客户端

**可选依赖**:
- `flask` - Web 框架
- `requests` - HTTP 请求库
- `aiohttp` - 异步 HTTP 库
- `langchain` - 集成支持

---

## 9. 目录结构

```
easyagent/
├── __init__.py               # 包初始化文件，导出主要API
│ 
├── core/                     # 核心功能和基类
│   ├── __init__.py           # 导出所有核心类
│   └── base.py               # 所有抽象基类的实现
│  
├── messages/                  # 消息类型实现
│   ├── __init__.py            # 导出所有消息类
│   ├── text.py                # 文本消息实现
│   ├── image.py               # 图像消息实现
│   └── structure.py           # 结构化消息实现
│  
├── tools/                     # 工具实现
│   ├── __init__.py            # 导出所有工具类
│   ├── base.py                # 工具的共享代码
│   ├── search.py              # 搜索引擎工具
│   └── calculator.py          # 计算器工具
│  
├── sdks/                      # SDK实现
│   ├── __init__.py            # 导出所有SDK类
│   ├── chat.py                # 聊天SDK实现
│   └── math.py                # 数学SDK实现
│  
├── services/                  # 服务实现
│   ├── __init__.py            # 导出所有服务类
│   ├── context.py             # 上下文管理器实现
│   └── memory.py              # 记忆管理器实现
│  
├── agents/                    # Agent实现
│   ├── __init__.py            # 导出所有Agent类
│   ├── llms.py               # LLM实现
│   ├── chat_agent.py          # 聊天Agent实现
│   └── search_agent.py        # 搜索Agent实现
│  
├── utils/                     # 工具函数
│   ├── __init__.py            # 导出所有工具函数
│   ├── trans.py               # 翻译相关功能
│   ├── logging.py             # 日志相关功能
│   └── config.py              # 配置相关功能
│
├── webui/                     # WebUI 核心模块
│   ├── __init__.py            # WebUI实现
│   ├── routes.py              # Flask 路由定义
│   ├── templates/             # 控制面板前端模板
│   │   └── dashboard.html     # 主控制面板
│   │
│   ├── static/                # Web静态文件
│   │   ├── css/
│   │   │   └── dashboard.css  # WebUI样式
│   │   ├── js/
│   │   │   └── dashboard.js   # 前端交互逻辑
│   │   │
│   │   └── img/               # 图标等资源
│   └── utils/
│       └── monitor.py         # 系统监控工具函数
│
└── run_web.py                 # Web服务启动入口
```

---

## 10. 错误处理

### 10.1 异常类设计

```python
class EasyAgentError(Exception):
    """基础异常类"""
    pass

class ModelError(EasyAgentError):
    """模型相关错误"""
    pass

class ToolError(EasyAgentError):
    """工具相关错误"""
    pass

class AgentError(EasyAgentError):
    """Agent相关错误"""
    pass

class ServiceError(EasyAgentError):
    """服务相关错误"""
    pass
```

---

## 11. 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 0.1.0 | - | 初始版本，完成核心架构设计 |

---

*本文档将随项目发展持续更新*
