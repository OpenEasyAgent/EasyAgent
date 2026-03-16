from easyagent.core.base import SDK
from easyagent.core.base import Tool
from easyagent.tools.search import SearchEngine
from easyagent.tools.weather import WeatherAPI
from typing import Dict, Any, List, Optional


class ChatSDK(SDK):
    """聊天SDK，包含聊天相关的工具集合"""

    __sdk_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "SDK名称"},
            "description": {"type": "string", "description": "SDK描述"},
            "tools": {"type": "array", "description": "包含的工具列表"},
        },
    }

    def __init__(self, name: str = "ChatSDK", description: str = "通用聊天SDK"):
        super().__init__()
        self.name = name
        self.description = description
        self.tools: List[Tool] = []

    @property
    def schema(self) -> Dict[str, Any]:
        return {
            **self.__sdk_schema,
            "properties": {
                **self.__sdk_schema["properties"],
                "name": {"type": "string", "description": self.name},
                "description": {"type": "string", "description": self.description},
            },
        }

    def append(self, tool: Tool) -> None:
        """添加工具到SDK

        Args:
            tool: 要添加的工具实例
        """
        self.tools.append(tool)

    def remove(self, tool: Tool) -> None:
        """从SDK中移除工具

        Args:
            tool: 要移除的工具实例
        """
        if tool in self.tools:
            self.tools.remove(tool)

    def get_tools(self) -> List[Tool]:
        """获取所有工具

        Returns:
            工具列表
        """
        return self.tools

    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """获取所有工具的schema定义

        Returns:
            工具schema列表
        """
        return [tool.schema for tool in self.tools]

    def get_tool_names(self) -> List[str]:
        """获取所有工具的名称

        Returns:
            工具名称列表
        """
        return [
            tool.schema.get("function", {}).get("name", "unknown")
            for tool in self.tools
        ]

    def find_tool(self, name: str) -> Optional[Tool]:
        """根据名称查找工具

        Args:
            name: 工具名称

        Returns:
            找到的工具实例，未找到返回None
        """
        for tool in self.tools:
            tool_name = tool.schema.get("function", {}).get("name", "")
            if tool_name == name:
                return tool
        return None

    def call(self, tool_name: str, *args, **kwargs):
        """调用SDK中的工具

        Args:
            tool_name: 工具名称
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            工具调用结果
        """
        tool = self.find_tool(tool_name)
        if tool is None:
            raise ValueError(f"未找到工具: {tool_name}")
        return tool(*args, **kwargs)


class DefaultChatSDK(ChatSDK):
    """默认聊天SDK，预置常用工具"""

    def __init__(
        self,
        search_api_key: Optional[str] = None,
        weather_api_key: Optional[str] = None,
    ):
        super().__init__(
            name="DefaultChatSDK", description="默认聊天SDK，包含搜索和天气工具"
        )

        if search_api_key:
            self.append(SearchEngine(api_key=search_api_key))

        if weather_api_key:
            self.append(WeatherAPI(api_key=weather_api_key))
