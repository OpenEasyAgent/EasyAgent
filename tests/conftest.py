import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_text():
    """提供示例文本"""
    return "This is a sample text for testing"


@pytest.fixture
def sample_message(sample_text):
    """提供示例消息"""
    from easyagent.messages.text import TextMessage

    return TextMessage(sample_text, source="user")


@pytest.fixture
def calculator():
    """提供计算器实例"""
    from easyagent.tools.calculator import Calculator

    return Calculator()


@pytest.fixture
def search_engine():
    """提供搜索引擎实例"""
    from easyagent.tools.search import SearchEngine

    return SearchEngine()


@pytest.fixture
def weather_api():
    """提供天气API实例"""
    from easyagent.tools.weather import WeatherAPI

    return WeatherAPI()


@pytest.fixture
def chat_sdk(search_engine, weather_api):
    """提供聊天SDK实例"""
    from easyagent.sdks.chat import ChatSDK

    sdk = ChatSDK()
    sdk.append(search_engine)
    sdk.append(weather_api)
    return sdk


@pytest.fixture
def math_sdk():
    """提供数学SDK实例"""
    from easyagent.sdks.math import MathSDK

    return MathSDK()


@pytest.fixture
def context_manager():
    """提供上下文管理器实例"""
    from easyagent.services.context import ContextManager

    return ContextManager()


@pytest.fixture
def memory_manager():
    """提供记忆管理器实例"""
    from easyagent.services.memory import MemoryManager

    return MemoryManager()


@pytest.fixture
def mock_openai_llm():
    """提供模拟的OpenAI LLM（不实际调用API）"""
    from easyagent.agents.llms import OpenAILLM
    from easyagent.messages.text import TextMessage

    class MockOpenAILLM(OpenAILLM):
        def call(self, prompt):
            return TextMessage("This is a mock response", source="assistant")

    return MockOpenAILLM(model_name="gpt-4", api_key="mock_key")


def pytest_configure(config):
    """Pytest 配置"""
    config.addinivalue_line("markers", "unit: Unit tests for individual components")
    config.addinivalue_line(
        "markers", "integration: Integration tests for multiple components"
    )
