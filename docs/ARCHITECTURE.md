# Project: EasyAgent

## 设计理念
- 简单，灵活，易用，更加符合python使用者的习惯（pythonic）
  
## 方案：
### Core元素

---

**Message**
- 信息，可以有多种模态。
- Message是一个基类，会继承实现TextMessage，ImageMessage，AudioMessage等

```python
text_message = TextMessage(content="Hello, world!")
image_message = ImageMessage(img_url="xxx")
```

---

**Tool**
- 工具，agent可以帮助model使用的接口。
- Tool是一个基类，会继承实现SearchEngine，Calculator等。
```python
search_engine = SearchEngine(engine="google")
calculator = Calculator()
```

---

**SDK**
- 工具的集合，方便进行管理。
- SDK是一个基类，会继承实现ChatSDK，MathSDK等。
```python
chatsdk = ChatSDK()
mathsdk = MathSDK()
```

---

**Service**
- 服务，如上下文管理，长中短期记忆管理
- Service是一个基类，会继承实现ContextManager，MemoryManager等。
```python
context_manager = ContextManager(max_length=4096)
memory_manager = MemoryManager(...) #参数没想好，到时候再说吧。
```

---

**Agent**
- AI Agent的核心，。
- Agent是一个基类，会继承实现ChatAgent，SearchAgent等。
```python
model = OpenAILLM(base_url="xxx", api_key="xxx")
sdk1 = ChatSDK()
sdk2 = SDK(SearchEngine(engine="google"))
agent1 = ChatAgent(model=model, sdk=sdk1)
agent2 = SearchAgent(model=model, sdk=sdk2)

```

---
### 构想的示例
```python
from easyagent.messages import TextMessage, ImageMessage
from easyagent.agents import ChatAgent, StableDiffusion, OpenAILLM
from easyagent.sdks import ChatSDK
from easyagent.core import Tool

class GetPaint(Tool):
    """
    对Tool基类进行二次开发
    实现了从文本生成图片
    """

    __tool_schema = {
        "name": "get_paint",
        "decription": "get a paint about a string 'query'.",
        "parameters": [
            {
                "name": "query",
                "type": "str",
                "description": "the paint's theme."
            }
        ]
    }

    def __init__(self, model):
        # model is a stable diffusion.
        super().__init__()
        self.model = model
    
    def call(self, query: str) -> ImageMessage:
        return model(query)


paint_model = StableDiffusion(...)  # 参数到时候再说
language_model = OpenAILLM(base_url="xxx", api_key="xxx", 
                           temperature=0.7, max_token=1024)

paint_tool = GetPaint(model=paint_model)
sdk = ChatSDK()
sdk.append(paint_tool)

agent = ChatAgent(model=language_model, sdk=sdk)

response = agent("Give me a picture about a cat girl, but in today's weather.")
# 实际上应该传入agent一个TextMessage类型，但我们会在内部兼容字符串。
# the agent will call the tool "weather_search", then call the tool "get_paint".

response.save("cat_girl.jpg")   # response: ImageMessage, and we will implement the method "save".

```
---
### 项目结构
```
easyagent/
├── __init__.py               # 包初始化文件，导出主要API
│ 
├── core/                     # 核心功能和基类
│   ├── __init__.py           # 导出所有核心类
│   └── base.py               # 所有抽象基类的实现 (Message, Tool, SDK, Service, Agent)
│  
├── messages/                  # 消息类型实现
│   ├── __init__.py            # 导出所有消息类
│   ├── text.py                # 文本消息实现
│   └── image.py               # 图像消息实现
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
│   ├── chat_agent.py          # 聊天Agent实现
│   └── search_agent.py        # 搜索Agent实现
│  
├── utils/                     # 工具函数
│   ├── __init__.py            # 导出所有工具函数
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
