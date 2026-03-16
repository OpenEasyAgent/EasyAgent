from easyagent.core.base import Service
from easyagent.messages.text import TextMessage
from typing import List, Dict, Any, Optional, Literal


class ContextManager(Service):
    """上下文管理器，控制对话上下文长度"""

    __service_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "max_length": {
                "type": "integer",
                "description": "最大上下文长度（字符数）",
            },
            "strategy": {
                "type": "string",
                "description": "截断策略",
                "enum": ["earliest", "latest", "smart"],
            },
        },
    }

    def __init__(
        self,
        max_length: int = 4096,
        strategy: Literal["earliest", "latest", "smart"] = "latest",
    ):
        super().__init__()
        self.max_length = max_length
        self.strategy = strategy
        self.messages: List[TextMessage] = []
        self._message_count = 0

    @property
    def schema(self) -> Dict[str, Any]:
        return {
            **self.__service_schema,
            "properties": {
                **self.__service_schema["properties"],
                "max_length": {"type": "integer", "description": str(self.max_length)},
                "strategy": {"type": "string", "description": self.strategy},
            },
        }

    def add_message(self, message: TextMessage) -> None:
        """添加消息到上下文

        Args:
            message: 要添加的消息
        """
        self.messages.append(message)
        self._message_count += 1
        self._truncate_if_needed()

    def add_user_message(self, text: str) -> TextMessage:
        """添加用户消息

        Args:
            text: 消息内容

        Returns:
            创建的消息对象
        """
        message = TextMessage(text, source="user")
        self.add_message(message)
        return message

    def add_assistant_message(self, text: str) -> TextMessage:
        """添加助手消息

        Args:
            text: 消息内容

        Returns:
            创建的消息对象
        """
        message = TextMessage(text, source="assistant")
        self.add_message(message)
        return message

    def add_system_message(self, text: str) -> TextMessage:
        """添加系统消息

        Args:
            text: 消息内容

        Returns:
            创建的消息对象
        """
        message = TextMessage(text, source="system")
        self.add_message(message)
        return message

    def get_context(self) -> List[TextMessage]:
        """获取当前上下文

        Returns:
            消息列表
        """
        return self.messages.copy()

    def get_messages_text(self) -> str:
        """获取所有消息的文本内容

        Returns:
            连接后的文本内容
        """
        return "\n".join([msg.text for msg in self.messages])

    def clear(self) -> None:
        """清空上下文"""
        self.messages.clear()

    def _truncate_if_needed(self) -> None:
        """根据策略截断过长的上下文"""
        current_length = len(self.get_messages_text())

        if current_length <= self.max_length:
            return

        if self.strategy == "earliest":
            self._truncate_earliest()
        elif self.strategy == "latest":
            self._truncate_latest()
        elif self.strategy == "smart":
            self._truncate_smart()

    def _truncate_earliest(self) -> None:
        """保留最新消息，删除最早的消息"""
        while (
            len(self.get_messages_text()) > self.max_length and len(self.messages) > 1
        ):
            self.messages.pop(0)

    def _truncate_latest(self) -> None:
        """保留最早的消息，删除最新的消息"""
        while (
            len(self.get_messages_text()) > self.max_length and len(self.messages) > 1
        ):
            self.messages.pop()

    def _truncate_smart(self) -> None:
        """智能截断：保留系统消息和最近的几轮对话"""
        system_messages = [msg for msg in self.messages if msg.source == "system"]
        other_messages = [msg for msg in self.messages if msg.source != "system"]

        target_length = self.max_length - sum(len(m.text) for m in system_messages)

        kept_messages = []
        for msg in reversed(other_messages):
            if sum(len(m.text) for m in kept_messages) + len(msg.text) <= target_length:
                kept_messages.insert(0, msg)
            else:
                break

        self.messages = system_messages + kept_messages

    def call(self, prompt: TextMessage) -> List[TextMessage]:
        """处理输入并返回上下文相关的响应

        Args:
            prompt: 输入的文本消息

        Returns:
            完整的消息列表
        """
        self.add_user_message(prompt.text)
        return self.get_context()

    def get_message_count(self) -> int:
        """获取消息总数

        Returns:
            消息数量
        """
        return self._message_count

    def get_token_count(self) -> int:
        """估算token数量

        Returns:
            估算的token数量
        """
        return len(self.get_messages_text()) // 4
