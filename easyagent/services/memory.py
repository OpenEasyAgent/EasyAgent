from easyagent.core.base import Service
from easyagent.messages.text import TextMessage
from typing import List, Dict, Any, Optional
from datetime import datetime
import time


class MemoryManager(Service):
    """记忆管理器，实现长中短期记忆"""

    __service_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "short_term_capacity": {
                "type": "integer",
                "description": "短期记忆容量（消息数）",
            },
            "long_term_capacity": {
                "type": "integer",
                "description": "长期记忆容量（消息数）",
            },
            "importance_threshold": {"type": "number", "description": "重要性阈值"},
        },
    }

    def __init__(
        self,
        short_term_capacity: int = 10,
        long_term_capacity: int = 100,
        importance_threshold: float = 0.5,
    ):
        super().__init__()
        self.short_term_capacity = short_term_capacity
        self.long_term_capacity = long_term_capacity
        self.importance_threshold = importance_threshold

        self.short_term: List[Dict[str, Any]] = []
        self.long_term: List[Dict[str, Any]] = []
        self._memory_id = 0

    @property
    def schema(self) -> Dict[str, Any]:
        return {
            **self.__service_schema,
            "properties": {
                **self.__service_schema["properties"],
                "short_term_capacity": {
                    "type": "integer",
                    "description": str(self.short_term_capacity),
                },
                "long_term_capacity": {
                    "type": "integer",
                    "description": str(self.long_term_capacity),
                },
            },
        }

    def add_message(self, message: TextMessage, importance: float = 0.5) -> int:
        """添加消息到记忆

        Args:
            message: 消息对象
            importance: 重要性评分 (0-1)

        Returns:
            记忆ID
        """
        memory_entry = {
            "id": self._get_next_id(),
            "message": message,
            "importance": importance,
            "timestamp": time.time(),
            "access_count": 0,
            "last_access": time.time(),
        }

        self.short_term.append(memory_entry)

        if len(self.short_term) > self.short_term_capacity:
            self.consolidate_to_long_term()

        return memory_entry["id"]

    def add_to_short_term(self, message: TextMessage, importance: float = 0.5) -> int:
        """添加到短期记忆

        Args:
            message: 消息对象
            importance: 重要性评分

        Returns:
            记忆ID
        """
        return self.add_message(message, importance)

    def consolidate_to_long_term(self) -> None:
        """将短期记忆整合到长期记忆"""
        if not self.short_term:
            return

        important_memories = [
            m for m in self.short_term if m["importance"] >= self.importance_threshold
        ]

        for memory in important_memories:
            if len(self.long_term) >= self.long_term_capacity:
                self._remove_least_important()
            self.long_term.append(memory)

        self.short_term.clear()

    def _remove_least_important(self) -> None:
        """移除最不重要的记忆"""
        if not self.long_term:
            return

        for memory in sorted(
            self.long_term,
            key=lambda m: (
                m["importance"],
                m["access_count"],
                -(time.time() - m["last_access"]),
            ),
        ):
            self.long_term.remove(memory)
            return

    def retrieve(self, query: TextMessage, top_k: int = 5) -> List[TextMessage]:
        """根据查询检索记忆

        Args:
            query: 查询消息
            top_k: 返回结果数量

        Returns:
            相关的消息列表
        """
        all_memories = self.short_term + self.long_term

        if not all_memories:
            return []

        query_text = query.text.lower()

        scored_memories = []
        for memory in all_memories:
            message_text = memory["message"].text.lower()

            query_words = set(query_text.split())
            message_words = set(message_text.split())

            overlap = len(query_words & message_words)
            relevance = overlap / max(len(query_words), 1)

            recency = 1.0 / (1.0 + (time.time() - memory["last_access"]) / 3600)
            access_bonus = memory["access_count"] * 0.1

            final_score = (
                relevance * 0.4
                + memory["importance"] * 0.3
                + recency * 0.2
                + min(access_bonus, 0.1)
            )

            scored_memories.append((final_score, memory))

        scored_memories.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, memory in scored_memories[:top_k]:
            memory["access_count"] += 1
            memory["last_access"] = time.time()
            results.append(memory["message"])

        return results

    def get_short_term(self) -> List[TextMessage]:
        """获取短期记忆

        Returns:
            短期记忆消息列表
        """
        return [m["message"] for m in self.short_term]

    def get_long_term(self) -> List[TextMessage]:
        """获取长期记忆

        Returns:
            长期记忆消息列表
        """
        return [m["message"] for m in self.long_term]

    def get_all_memories(self) -> List[TextMessage]:
        """获取所有记忆

        Returns:
            所有记忆消息列表
        """
        return self.get_short_term() + self.get_long_term()

    def clear_short_term(self) -> None:
        """清空短期记忆"""
        self.short_term.clear()

    def clear_long_term(self) -> None:
        """清空长期记忆"""
        self.long_term.clear()

    def clear_all(self) -> None:
        """清空所有记忆"""
        self.clear_short_term()
        self.clear_long_term()

    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计信息

        Returns:
            统计信息字典
        """
        return {
            "short_term_count": len(self.short_term),
            "long_term_count": len(self.long_term),
            "short_term_capacity": self.short_term_capacity,
            "long_term_capacity": self.long_term_capacity,
            "total_access_count": sum(
                m["access_count"] for m in self.short_term + self.long_term
            ),
        }

    def _get_next_id(self) -> int:
        """获取下一个记忆ID"""
        self._memory_id += 1
        return self._memory_id

    def call(self, message: TextMessage, importance: float = 0.5) -> int:
        """处理输入并添加到记忆

        Args:
            message: 消息对象
            importance: 重要性评分

        Returns:
            记忆ID
        """
        return self.add_message(message, importance)
