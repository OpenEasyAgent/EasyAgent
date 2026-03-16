import logging
import sys
from typing import Optional
from pathlib import Path
from enum import Enum


class LogLevel(Enum):
    """日志级别"""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class EasyAgentLogger:
    """EasyAgent 日志管理器"""

    _loggers = {}
    _default_logger: Optional[logging.Logger] = None

    @classmethod
    def setup_logger(
        cls,
        name: str = "easyagent",
        level: LogLevel = LogLevel.INFO,
        log_file: Optional[str] = None,
        log_format: str = DEFAULT_FORMAT,
        date_format: str = DEFAULT_DATE_FORMAT,
    ) -> logging.Logger:
        """设置日志记录器

        Args:
            name: 日志记录器名称
            level: 日志级别
            log_file: 日志文件路径，如果为None则只输出到控制台
            log_format: 日志格式
            date_format: 日期格式

        Returns:
            配置好的日志记录器
        """
        logger = logging.getLogger(name)
        logger.setLevel(level.value)

        if logger.hasHandlers():
            logger.handlers.clear()

        formatter = logging.Formatter(log_format, date_format)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level.value)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(level.value)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        cls._loggers[name] = logger

        if name == "easyagent":
            cls._default_logger = logger

        return logger

    @classmethod
    def get_logger(cls, name: str = "easyagent") -> logging.Logger:
        """获取日志记录器

        Args:
            name: 日志记录器名称

        Returns:
            日志记录器
        """
        if name in cls._loggers:
            return cls._loggers[name]

        if cls._default_logger is None:
            cls.setup_logger(name)

        return cls._loggers.get(name, cls._default_logger)


def setup_logger(
    name: str = "easyagent",
    level: LogLevel = LogLevel.INFO,
    log_file: Optional[str] = None,
    log_format: str = DEFAULT_FORMAT,
    date_format: str = DEFAULT_DATE_FORMAT,
) -> logging.Logger:
    """设置日志记录器的便捷函数

    Args:
        name: 日志记录器名称
        level: 日志级别
        log_file: 日志文件路径
        log_format: 日志格式
        date_format: 日期格式

    Returns:
        配置好的日志记录器
    """
    return EasyAgentLogger.setup_logger(name, level, log_file, log_format, date_format)


def get_logger(name: str = "easyagent") -> logging.Logger:
    """获取日志记录器的便捷函数

    Args:
        name: 日志记录器名称

    Returns:
        日志记录器
    """
    return EasyAgentLogger.get_logger(name)


def log_request(logger: logging.Logger, prompt: str, model: str):
    """记录API请求日志

    Args:
        logger: 日志记录器
        prompt: 请求提示
        model: 模型名称
    """
    logger.debug(f"API Request - Model: {model}")
    logger.debug(f"Prompt: {prompt[:100]}...")


def log_response(logger: logging.Logger, response: str, model: str, duration: float):
    """记录API响应日志

    Args:
        logger: 日志记录器
        response: 响应内容
        model: 模型名称
        duration: 耗时（秒）
    """
    logger.info(f"API Response - Model: {model}, Duration: {duration:.2f}s")
    logger.debug(f"Response: {response[:100]}...")


def log_tool_call(logger: logging.Logger, tool_name: str, args: dict):
    """记录工具调用日志

    Args:
        logger: 日志记录器
        tool_name: 工具名称
        args: 工具参数
    """
    logger.info(f"Tool Call: {tool_name}")
    logger.debug(f"Arguments: {args}")


def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """记录错误日志

    Args:
        logger: 日志记录器
        error: 异常对象
        context: 错误上下文信息
    """
    if context:
        logger.error(f"{context} - Error: {type(error).__name__}: {str(error)}")
    else:
        logger.error(f"Error: {type(error).__name__}: {str(error)}")
