from easyagent.agents.chat_agent import ChatAgent
from easyagent.tools.search import SearchEngine
from easyagent.tools.weather import WeatherAPI
from easyagent.sdks.chat import ChatSDK
from easyagent.messages.text import TextMessage
from typing import Union


class SearchAgent(ChatAgent):
    """搜索专用Agent，自动使用搜索工具"""

    def __init__(self, model, api_key: str = None, search_engine: str = "google"):
        sdk = ChatSDK()
        sdk.append(SearchEngine(engine=search_engine, api_key=api_key))

        system_prompt = """You are a search assistant. Your main task is to help users find information on the internet.
When a user asks for information that you don't have up-to-date knowledge about, you should use the search tool to find the relevant information.
Always provide accurate and helpful information based on the search results."""

        super().__init__(model=model, sdk=sdk, system_prompt=system_prompt)

        self.search_engine = search_engine

    def search(self, query: str) -> str:
        """执行搜索

        Args:
            query: 搜索关键词

        Returns:
            搜索结果
        """
        result = self.run_with_tools(TextMessage(query, source="user"))
        return result.text
