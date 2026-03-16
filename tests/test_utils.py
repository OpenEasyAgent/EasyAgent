import pytest
from easyagent.messages.text import TextMessage
from easyagent.utils.trans import text_list_to_openai_messages
from easyagent.utils.logging import (
    setup_logger,
    get_logger,
    LogLevel,
    log_request,
    log_response,
    log_tool_call,
    log_error,
)
import logging


class TestTransUtils:
    """翻译工具测试类"""

    def test_single_message_conversion(self):
        """测试单条消息转换"""
        msg = TextMessage("Hello", source="user")
        result = text_list_to_openai_messages([msg])

        assert len(result) == 1
        assert result[0]["role"] == "user"
        assert result[0]["content"] == "Hello"

    def test_multiple_messages_conversion(self):
        """测试多条消息转换"""
        messages = [
            TextMessage("System prompt", source="system"),
            TextMessage("Hello", source="user"),
            TextMessage("Hi there", source="assistant"),
        ]
        result = text_list_to_openai_messages(messages)

        assert len(result) == 3
        assert result[0]["role"] == "system"
        assert result[1]["role"] == "user"
        assert result[2]["role"] == "assistant"

    def test_mixed_sources(self):
        """测试混合来源"""
        messages = [
            TextMessage("First", source="user"),
            TextMessage("Second", source="assistant"),
            TextMessage("Third", source="user"),
        ]
        result = text_list_to_openai_messages(messages)

        assert result[0]["role"] == "user"
        assert result[1]["role"] == "assistant"
        assert result[2]["role"] == "user"


class TestLoggingUtils:
    """日志工具测试类"""

    def test_setup_logger(self):
        """测试设置日志记录器"""
        logger = setup_logger(name="test_logger", level=LogLevel.INFO)

        assert logger is not None
        assert logger.name == "test_logger"
        assert logger.level == logging.INFO

    def test_get_logger(self):
        """测试获取日志记录器"""
        setup_logger(name="test_get_logger")
        logger = get_logger("test_get_logger")

        assert logger is not None
        assert logger.name == "test_get_logger"

    def test_default_logger(self):
        """测试默认日志记录器"""
        logger = get_logger()

        assert logger is not None

    def test_log_request(self):
        """测试请求日志"""
        logger = setup_logger(name="test_request", level=LogLevel.DEBUG)

        log_request(logger, "Test prompt", "gpt-4")

    def test_log_response(self):
        """测试响应日志"""
        logger = setup_logger(name="test_response", level=LogLevel.DEBUG)

        log_response(logger, "Response text", "gpt-4", 1.5)

    def test_log_tool_call(self):
        """测试工具调用日志"""
        logger = setup_logger(name="test_tool", level=LogLevel.DEBUG)

        log_tool_call(logger, "search_engine", {"query": "Python"})

    def test_log_error(self):
        """测试错误日志"""
        logger = setup_logger(name="test_error", level=LogLevel.DEBUG)

        try:
            raise ValueError("Test error")
        except ValueError as e:
            log_error(logger, e, "Test context")

    def test_log_level_enum(self):
        """测试日志级别枚举"""
        assert LogLevel.DEBUG.value == logging.DEBUG
        assert LogLevel.INFO.value == logging.INFO
        assert LogLevel.WARNING.value == logging.WARNING
        assert LogLevel.ERROR.value == logging.ERROR
        assert LogLevel.CRITICAL.value == logging.CRITICAL
