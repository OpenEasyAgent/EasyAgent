from easyagent.core.base import Agent
from easyagent.core.base import SDK
from easyagent.messages.text import TextMessage
from easyagent.agents.llms import LLM
from easyagent.services.context import ContextManager
from easyagent.utils.trans import text_list_to_openai_messages
from typing import List, Dict, Any, Optional, Union
import json


class ChatAgent(Agent):
    """聊天Agent，协调模型与工具的交互"""

    __agent_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "model": {"type": "object", "description": "语言模型"},
            "sdk": {"type": "object", "description": "工具SDK"},
            "context_manager": {"type": "object", "description": "上下文管理器"},
            "system_prompt": {"type": "string", "description": "系统提示词"},
        },
        "required": ["model"],
    }

    def __init__(
        self,
        model: LLM,
        sdk: Optional[SDK] = None,
        context_manager: Optional[ContextManager] = None,
        system_prompt: str = "You are a helpful AI assistant.",
    ):
        super().__init__()
        self.model = model
        self.sdk = sdk
        self.context_manager = context_manager or ContextManager()
        self.system_prompt = system_prompt

        if self.sdk and self.sdk.tools:
            self._add_tool_descriptions_to_system_prompt()

    @property
    def schema(self) -> Dict[str, Any]:
        return self.__agent_schema

    def _add_tool_descriptions_to_system_prompt(self) -> None:
        """将工具描述添加到系统提示词"""
        if not self.sdk or not self.sdk.tools:
            return

        tool_descriptions = []
        for tool in self.sdk.tools:
            schema = tool.schema
            func = schema.get("function", {})
            tool_descriptions.append(f"- {func.get('name')}: {func.get('description')}")

        tools_info = "\n".join(tool_descriptions)
        self.system_prompt += f"\n\nYou have access to the following tools:\n{tools_info}\n\nWhen you need to use a tool, respond with a JSON object."

        self.context_manager.add_system_message(self.system_prompt)

    def call(self, prompt: Union[str, TextMessage]) -> TextMessage:
        """调用Agent处理输入

        Args:
            prompt: 输入的文本或消息对象

        Returns:
            生成的响应消息
        """
        if isinstance(prompt, str):
            prompt = TextMessage(prompt, source="user")

        self.context_manager.add_message(prompt)

        context = self.context_manager.get_context()

        response = self.model.call(context)

        self.context_manager.add_message(response)

        return response

    def chat(self, message: str) -> str:
        """便捷的聊天方法

        Args:
            message: 用户消息

        Returns:
            助手回复文本
        """
        response = self.call(message)
        return response.text

    def run_with_tools(self, prompt: Union[str, TextMessage]) -> TextMessage:
        """使用工具调用运行Agent

        Args:
            prompt: 输入的文本或消息对象

        Returns:
            生成的响应消息
        """
        if not self.sdk or not self.sdk.tools:
            return self.call(prompt)

        if isinstance(prompt, str):
            prompt = TextMessage(prompt, source="user")

        self.context_manager.add_message(prompt)

        context = self.context_manager.get_context()

        response = self.model.call(context)

        if self._should_use_tools(response):
            tool_calls = self._extract_tool_calls(response)

            for tool_call in tool_calls:
                tool_result = self._execute_tool(tool_call)
                self.context_manager.add_message(
                    TextMessage(f"Tool result: {tool_result}", source="system")
                )

            final_response = self.model.call(self.context_manager.get_context())
            self.context_manager.add_message(final_response)
            return final_response

        self.context_manager.add_message(response)
        return response

    def _should_use_tools(self, response: TextMessage) -> bool:
        """判断是否应该使用工具"""
        try:
            data = json.loads(response.text)
            return "name" in data or "function" in data
        except (json.JSONDecodeError, AttributeError):
            return False

    def _extract_tool_calls(self, response: TextMessage) -> List[Dict[str, Any]]:
        """提取工具调用信息"""
        try:
            data = json.loads(response.text)
            if "function" in data:
                return [data]
            if "name" in data:
                return [{"name": data["name"], "arguments": data.get("arguments", {})}]
        except (json.JSONDecodeError, AttributeError):
            pass
        return []

    def _execute_tool(self, tool_call: Dict[str, Any]) -> str:
        """执行工具调用"""
        tool_name = tool_call.get("name") or tool_call.get("function", {}).get("name")
        arguments = tool_call.get("arguments") or tool_call.get("function", {}).get(
            "arguments", {}
        )

        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except json.JSONDecodeError:
                arguments = {}

        tool = self.sdk.find_tool(tool_name)
        if tool is None:
            return f"Error: Tool '{tool_name}' not found"

        try:
            result = tool(**arguments)
            return str(result)
        except Exception as e:
            return f"Error executing tool: {str(e)}"

    def clear_context(self) -> None:
        """清空对话上下文"""
        self.context_manager.clear()
        self.context_manager.add_system_message(self.system_prompt)

    def get_context(self) -> List[TextMessage]:
        """获取当前上下文"""
        return self.context_manager.get_context()
