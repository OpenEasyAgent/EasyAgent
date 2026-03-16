import pytest
from easyagent.messages.text import TextMessage
from easyagent.services.context import ContextManager
from easyagent.tools.search import SearchEngine
from easyagent.tools.calculator import Calculator
from easyagent.sdks.chat import ChatSDK


class MockLLM:
    """模拟 LLM 用于测试"""

    def __init__(self, response_text="Mock response"):
        self.response_text = response_text
        self.call_count = 0

    def call(self, prompt):
        self.call_count += 1
        return TextMessage(self.response_text, source="assistant")

    @property
    def schema(self):
        return {"type": "object", "properties": {}}

    @property
    def model_name(self):
        return "mock_model"

    @property
    def api_key(self):
        return "mock_key"


class TestChatAgent:
    """ChatAgent 测试类"""

    def test_create_chat_agent(self):
        """测试创建 ChatAgent"""
        from easyagent.agents.chat_agent import ChatAgent

        llm = MockLLM()
        agent = ChatAgent(model=llm)

        assert agent.model is not None
        assert agent.context_manager is not None

    def test_chat_agent_with_sdk(self):
        """测试带 SDK 的 ChatAgent"""
        from easyagent.agents.chat_agent import ChatAgent

        llm = MockLLM()
        sdk = ChatSDK()
        sdk.append(SearchEngine())

        agent = ChatAgent(model=llm, sdk=sdk)

        assert agent.sdk is not None
        assert len(agent.sdk.tools) > 0

    def test_chat_agent_call(self):
        """测试 Agent 调用"""
        from easyagent.agents.chat_agent import ChatAgent

        llm = MockLLM(response_text="Hello!")
        agent = ChatAgent(model=llm)

        response = agent("Hi there")

        assert isinstance(response, TextMessage)
        assert response.text == "Hello!"

    def test_chat_agent_chat_method(self):
        """测试 chat 方法"""
        from easyagent.agents.chat_agent import ChatAgent

        llm = MockLLM(response_text="Hello!")
        agent = ChatAgent(model=llm)

        response_text = agent.chat("Hi")

        assert response_text == "Hello!"

    def test_chat_agent_with_string_input(self):
        """测试字符串输入"""
        from easyagent.agents.chat_agent import ChatAgent

        llm = MockLLM(response_text="Response")
        agent = ChatAgent(model=llm)

        response = agent.call("Test message")

        assert isinstance(response, TextMessage)

    def test_clear_context(self):
        """测试清空上下文"""
        from easyagent.agents.chat_agent import ChatAgent

        llm = MockLLM()
        agent = ChatAgent(model=llm)

        agent("First message")
        agent("Second message")

        agent.clear_context()

        context = agent.get_context()
        assert len(context) <= 1

    def test_get_context(self):
        """测试获取上下文"""
        from easyagent.agents.chat_agent import ChatAgent

        llm = MockLLM()
        agent = ChatAgent(model=llm)

        agent("Test message")

        context = agent.get_context()
        assert len(context) > 0

    def test_context_manager_integration(self):
        """测试上下文管理器集成"""
        from easyagent.agents.chat_agent import ChatAgent

        ctx = ContextManager(max_length=100)
        llm = MockLLM()

        agent = ChatAgent(model=llm, context_manager=ctx)

        agent("Message 1")
        agent("Message 2")

        assert ctx.get_message_count() >= 2

    def test_system_prompt(self):
        """测试系统提示词"""
        from easyagent.agents.chat_agent import ChatAgent

        custom_prompt = "You are a helpful assistant."
        llm = MockLLM()

        agent = ChatAgent(model=llm, system_prompt=custom_prompt)

        assert agent.system_prompt == custom_prompt


class TestSearchAgent:
    """SearchAgent 测试类"""

    def test_create_search_agent(self):
        """测试创建 SearchAgent"""
        from easyagent.agents.search_agent import SearchAgent

        llm = MockLLM(response_text="Search results")
        agent = SearchAgent(model=llm)

        assert agent.model is not None
        assert agent.sdk is not None

    def test_search_agent_has_search_tool(self):
        """测试搜索 Agent 有搜索工具"""
        from easyagent.agents.search_agent import SearchAgent

        llm = MockLLM()
        agent = SearchAgent(model=llm)

        tool = agent.sdk.find_tool("search_engine")
        assert tool is not None
