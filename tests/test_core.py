import pytest
from easyagent.messages.text import TextMessage
from easyagent.tools.calculator import Calculator
from easyagent.tools.search import SearchEngine
from easyagent.tools.weather import WeatherAPI
from easyagent.sdks.chat import ChatSDK
from easyagent.sdks.math import MathSDK
from easyagent.services.context import ContextManager
from easyagent.services.memory import MemoryManager
from easyagent.agents.llms import LLM, OpenAILLM
from easyagent.core.base import Tool, SDK, Service, Agent


class TestTextMessage:
    """TextMessage 测试类"""

    def test_create_text_message(self):
        """测试创建文本消息"""
        msg = TextMessage("Hello, World!")
        assert msg.text == "Hello, World!"
        assert msg.source == "system"

    def test_create_with_source(self):
        """测试创建带来源的消息"""
        msg = TextMessage("User message", source="user")
        assert msg.text == "User message"
        assert msg.source == "user"

    def test_add_operator(self):
        """测试加法运算符"""
        msg1 = TextMessage("Hello")
        msg2 = TextMessage(" World")
        result = msg1 + msg2
        assert result.text == "Hello World"
        assert result.source == "system"

    def test_iadd_operator(self):
        """测试加法赋值运算符"""
        msg1 = TextMessage("Hello")
        msg1 += TextMessage(" World")
        assert msg1.text == "Hello World"

    def test_len(self):
        """测试长度计算"""
        msg = TextMessage("Hello")
        assert len(msg) == 5

    def test_contains(self):
        """测试包含判断"""
        msg = TextMessage("Hello World")
        assert "Hello" in msg
        assert "Python" not in msg

    def test_equality(self):
        """测试相等判断"""
        msg1 = TextMessage("Hello", source="user")
        msg2 = TextMessage("Hello", source="user")
        msg3 = TextMessage("Hello", source="assistant")

        assert msg1 == msg2
        assert msg1 != msg3

    def test_str_repr(self):
        """测试字符串表示"""
        msg = TextMessage("Hello", source="user")
        assert str(msg) == "Hello"
        assert "TextMessage" in repr(msg)


class TestCalculator:
    """Calculator 测试类"""

    def test_basic_arithmetic(self):
        """测试基本算术运算"""
        calc = Calculator()

        result = calc.call("2 + 2")
        assert "4" in result.text

        result = calc.call("10 - 5")
        assert "5" in result.text

        result = calc.call("3 * 4")
        assert "12" in result.text

        result = calc.call("10 / 2")
        assert "5" in result.text

    def test_parentheses(self):
        """测试括号运算"""
        calc = Calculator()
        result = calc.call("(2 + 3) * 4")
        assert "20" in result.text

    def test_power(self):
        """测试幂运算"""
        calc = Calculator()
        result = calc.call("2 ** 3")
        assert "8" in result.text

    def test_negative_numbers(self):
        """测试负数"""
        calc = Calculator()
        result = calc.call("-5 + 3")
        assert "-2" in result.text

    def test_invalid_expression(self):
        """测试无效表达式"""
        calc = Calculator()
        result = calc.call("abc + 123")
        assert "错误" in result.text


class TestSearchEngine:
    """SearchEngine 测试类"""

    def test_create_search_engine(self):
        """测试创建搜索引擎"""
        search = SearchEngine()
        assert search.engine == "google"

        search = SearchEngine(engine="bing")
        assert search.engine == "bing"

    def test_schema(self):
        """测试 schema 定义"""
        search = SearchEngine()
        schema = search.schema
        assert "function" in schema
        assert schema["function"]["name"] == "search_engine"

    def test_search_simulation(self):
        """测试搜索功能（模拟）"""
        search = SearchEngine()
        result = search.call("Python")
        assert isinstance(result.text, str)
        assert len(result.text) > 0


class TestWeatherAPI:
    """WeatherAPI 测试类"""

    def test_create_weather_api(self):
        """测试创建天气API"""
        weather = WeatherAPI()
        assert weather.api_key is None

        weather = WeatherAPI(api_key="test_key")
        assert weather.api_key == "test_key"

    def test_schema(self):
        """测试 schema 定义"""
        weather = WeatherAPI()
        schema = weather.schema
        assert "function" in schema
        assert schema["function"]["name"] == "weather"

    def test_weather_simulation(self):
        """测试天气查询（模拟）"""
        weather = WeatherAPI()
        result = weather.call("Beijing")
        assert isinstance(result.text, str)
        assert "Beijing" in result.text


class TestChatSDK:
    """ChatSDK 测试类"""

    def test_create_sdk(self):
        """测试创建 SDK"""
        sdk = ChatSDK()
        assert sdk.name == "ChatSDK"
        assert len(sdk.tools) == 0

    def test_append_tool(self):
        """测试添加工具"""
        sdk = ChatSDK()
        search = SearchEngine()
        sdk.append(search)
        assert len(sdk.tools) == 1

    def test_remove_tool(self):
        """测试移除工具"""
        sdk = ChatSDK()
        search = SearchEngine()
        sdk.append(search)
        sdk.remove(search)
        assert len(sdk.tools) == 0

    def test_get_tools_schema(self):
        """测试获取工具 schema"""
        sdk = ChatSDK()
        search = SearchEngine()
        sdk.append(search)

        schemas = sdk.get_tools_schema()
        assert len(schemas) == 1
        assert schemas[0]["function"]["name"] == "search_engine"

    def test_find_tool(self):
        """测试查找工具"""
        sdk = ChatSDK()
        search = SearchEngine()
        sdk.append(search)

        found = sdk.find_tool("search_engine")
        assert found is not None

        not_found = sdk.find_tool("nonexistent")
        assert not_found is None


class TestMathSDK:
    """MathSDK 测试类"""

    def test_create_math_sdk(self):
        """测试创建数学 SDK"""
        sdk = MathSDK()
        assert sdk.name == "MathSDK"
        assert len(sdk.tools) == 1

    def test_calculator_included(self):
        """测试计算器已包含"""
        sdk = MathSDK()
        tool = sdk.find_tool("calculator")
        assert tool is not None


class TestContextManager:
    """ContextManager 测试类"""

    def test_create_context_manager(self):
        """测试创建上下文管理器"""
        ctx = ContextManager()
        assert ctx.max_length == 4096
        assert ctx.strategy == "latest"

    def test_add_message(self):
        """测试添加消息"""
        ctx = ContextManager()
        msg = TextMessage("Hello", source="user")
        ctx.add_message(msg)

        messages = ctx.get_context()
        assert len(messages) == 1

    def test_add_user_message(self):
        """测试添加用户消息"""
        ctx = ContextManager()
        msg = ctx.add_user_message("Hello")

        assert msg.source == "user"
        assert msg.text == "Hello"

    def test_add_assistant_message(self):
        """测试添加助手消息"""
        ctx = ContextManager()
        msg = ctx.add_assistant_message("Hi there")

        assert msg.source == "assistant"

    def test_clear(self):
        """测试清空上下文"""
        ctx = ContextManager()
        ctx.add_user_message("Hello")
        ctx.add_assistant_message("Hi")

        ctx.clear()

        assert len(ctx.get_context()) == 0

    def test_truncation_earliest(self):
        """测试保留最新消息策略"""
        ctx = ContextManager(max_length=10, strategy="earliest")
        ctx.add_message(TextMessage("Short message 1"))
        ctx.add_message(TextMessage("Short message 2"))

        messages = ctx.get_context()
        assert len(messages) >= 1


class TestMemoryManager:
    """MemoryManager 测试类"""

    def test_create_memory_manager(self):
        """测试创建记忆管理器"""
        mem = MemoryManager()
        assert mem.short_term_capacity == 10
        assert mem.long_term_capacity == 100

    def test_add_message(self):
        """测试添加消息到记忆"""
        mem = MemoryManager()
        msg = TextMessage("Test memory")
        mem_id = mem.add_message(msg)

        assert mem_id > 0
        assert len(mem.get_short_term()) == 1

    def test_consolidate(self):
        """测试记忆整合"""
        mem = MemoryManager(short_term_capacity=2, importance_threshold=0.5)

        mem.add_message(TextMessage("Important 1"), importance=0.8)
        mem.add_message(TextMessage("Important 2"), importance=0.6)

        mem.consolidate_to_long_term()

        assert len(mem.get_long_term()) >= 1

    def test_retrieve(self):
        """测试记忆检索"""
        mem = MemoryManager()
        mem.add_message(TextMessage("Python is a programming language"))
        mem.add_message(TextMessage("Java is another language"))

        results = mem.retrieve(TextMessage("Python programming"))

        assert len(results) > 0

    def test_clear(self):
        """测试清空记忆"""
        mem = MemoryManager()
        mem.add_message(TextMessage("Test"))

        mem.clear_all()

        assert len(mem.get_all_memories()) == 0

    def test_stats(self):
        """测试获取统计信息"""
        mem = MemoryManager()
        mem.add_message(TextMessage("Test"))

        stats = mem.get_memory_stats()

        assert "short_term_count" in stats
        assert "long_term_count" in stats


class TestOpenAILLM:
    """OpenAILLM 测试类"""

    def test_create_llm(self):
        """测试创建 LLM"""
        llm = OpenAILLM(model_name="gpt-4", api_key="test_key")

        assert llm.model_name == "gpt-4"
        assert llm.api_key == "test_key"
        assert llm.temperature == 0.7

    def test_schema(self):
        """测试 schema 定义"""
        llm = OpenAILLM(model_name="gpt-4", api_key="test_key")
        schema = llm.schema

        assert "properties" in schema
        assert "model_name" in schema["properties"]


class TestIntegration:
    """集成测试"""

    def test_sdk_with_tools(self):
        """测试 SDK 集成工具"""
        sdk = ChatSDK()
        search = SearchEngine()
        weather = WeatherAPI()

        sdk.append(search)
        sdk.append(weather)

        assert len(sdk.tools) == 2

        search_result = sdk.call("search_engine", query="Python")
        assert isinstance(search_result, TextMessage)

    def test_context_with_messages(self):
        """测试上下文与消息集成"""
        ctx = ContextManager()

        ctx.add_user_message("What is Python?")
        ctx.add_assistant_message("Python is a programming language.")

        context = ctx.get_context()

        assert len(context) == 2
        assert context[0].source == "user"
        assert context[1].source == "assistant"

    def test_memory_retrieval_flow(self):
        """测试记忆检索流程"""
        mem = MemoryManager()

        mem.add_message(TextMessage("My favorite color is blue"), importance=0.8)
        mem.add_message(TextMessage("I like coding in Python"), importance=0.9)

        results = mem.retrieve(TextMessage("programming Python"))

        assert len(results) > 0
