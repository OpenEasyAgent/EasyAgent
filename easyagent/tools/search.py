from easyagent.core.base import Tool
from easyagent.messages.text import TextMessage
from typing import Dict, Any, Optional
import requests


class SearchEngine(Tool):
    """搜索引擎工具"""

    __tool_schema: Dict[str, Any] = {
        "type": "function",
        "function": {
            "name": "search_engine",
            "description": "搜索互联网信息，返回与查询相关的网页结果",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                    "engine": {
                        "type": "string",
                        "description": "搜索引擎类型，可选值: google, bing, baidu",
                        "enum": ["google", "bing", "baidu"],
                        "default": "google",
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "返回结果数量",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        },
    }

    def __init__(self, engine: str = "google", api_key: Optional[str] = None):
        super().__init__()
        self.engine = engine
        self.api_key = api_key

    @property
    def schema(self) -> Dict[str, Any]:
        return self.__tool_schema

    def call(
        self, query: str, engine: Optional[str] = None, num_results: int = 5
    ) -> TextMessage:
        """执行搜索并返回结果

        Args:
            query: 搜索关键词
            engine: 搜索引擎类型，可选值: google, bing, baidu
            num_results: 返回结果数量

        Returns:
            搜索结果文本消息
        """
        engine = engine or self.engine

        try:
            if engine == "google":
                results = self._search_google(query, num_results)
            elif engine == "bing":
                results = self._search_bing(query, num_results)
            elif engine == "baidu":
                results = self._search_baidu(query, num_results)
            else:
                results = f"不支持的搜索引擎: {engine}"
        except Exception as e:
            results = f"搜索出错: {str(e)}"

        return TextMessage(results, source="tool")

    def _search_google(self, query: str, num_results: int) -> str:
        """使用Google搜索"""
        if self.api_key:
            url = "https://customsearch.googleapis.com/customsearch/v1"
            params = {
                "key": self.api_key,
                "cx": self.engine,
                "q": query,
                "num": num_results,
            }
            response = requests.get(url, params=params)
            data = response.json()
            return self._format_results(data.get("items", []))

        return self._simulated_search(query, num_results, "Google")

    def _search_bing(self, query: str, num_results: int) -> str:
        """使用Bing搜索"""
        if self.api_key:
            url = "https://api.bing.microsoft.com/v7.0/search"
            headers = {"Ocp-Apim-Subscription-Key": self.api_key}
            params = {"q": query, "count": num_results}
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            return self._format_results(data.get("webPages", {}).get("value", []))

        return self._simulated_search(query, num_results, "Bing")

    def _search_baidu(self, query: str, num_results: int) -> str:
        """使用Baidu搜索"""
        if self.api_key:
            url = "https://api.baidu.com/json/sms/v1/SearchService"
            params = {"q": query, "num": num_results}
            headers = {"apikey": self.api_key}
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            return self._format_results(data.get("results", []))

        return self._simulated_search(query, num_results, "Baidu")

    def _simulated_search(self, query: str, num_results: int, engine: str) -> str:
        """模拟搜索结果（当没有API密钥时使用）"""
        results = [
            f"结果 {idx + 1}: 关于「{query}」的相关信息 - 来源: {engine}"
            for idx in range(num_results)
        ]
        return "\n".join(results[:num_results])

    def _format_results(self, items: list) -> str:
        """格式化搜索结果"""
        if not items:
            return "未找到相关结果"

        results = []
        for i, item in enumerate(items):
            title = item.get("title", "无标题")
            snippet = item.get("snippet", item.get("description", ""))
            link = item.get("link", item.get("url", ""))
            results.append(f"{i + 1}. {title}\n   {snippet}\n   链接: {link}")

        return "\n\n".join(results)
