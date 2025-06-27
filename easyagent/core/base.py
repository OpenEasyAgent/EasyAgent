from abc import ABC, abstractmethod
from typing import Dict, List, Any

class Tool(ABC):
    """工具基类，所有工具应继承此类"""
    __tool_schema: Dict[str, Any] = {}
    @property
    def schema(self) -> Dict[str, Any]:
        """返回工具的schema定义"""
        if hasattr(self, "__tool_schema"):
            return self.__tool_schema
        raise NotImplementedError("Tool schema not defined")
    
    @abstractmethod
    def call(self, *args, **kwargs):
        """调用工具的方法，必须由子类实现"""
        raise NotImplementedError("Tool call method not implemented")

class Message(ABC):
    """消息基类，所有消息类型应继承此类"""
    __message_schema: Dict[str, Any] = {}
    
    def __init__(self, source: str = "system") -> None:
        """
        初始化消息对象
        :param source: 消息来源，默认为"system"
        """
        self.source = source
        
    def set_source(self, source: str) -> None:
        """
        设置消息来源
        :param source: 消息来源
        """
        self.source = source
    
    @property
    def schema(self) -> Dict[str, Any]:
        """返回消息的schema定义"""
        if hasattr(self, "__message_schema"):
            return self.__message_schema
        raise NotImplementedError("Message schema not defined")

class SDK(ABC):
    """SDK基类，所有SDK应继承此类"""
    __sdk_schema: Dict[str, Any] = {}
    @property
    def schema(self) -> Dict[str, Any]:
        """返回SDK的schema定义"""
        if hasattr(self, "__sdk_schema"):
            return self.__sdk_schema
        raise NotImplementedError("SDK schema not defined")


class Service(ABC):
    """服务基类，所有服务应继承此类"""
    __service_schema: Dict[str, Any] = {}
    @property
    def schema(self) -> Dict[str, Any]:
        """返回服务的schema定义"""
        if hasattr(self, "__service_schema"):
            return self.__service_schema
        raise NotImplementedError("Service schema not defined")
    
    @abstractmethod
    def call(self, *args, **kwargs):
        """调用服务的方法，必须由子类实现"""
        raise NotImplementedError("Service call method not implemented")


class Agent(ABC):
    """Agent基类，所有Agent应继承此类"""
    __agent_schema: Dict[str, Any] = {}
    @property
    def schema(self) -> Dict[str, Any]:
        """返回Agent的schema定义"""
        if hasattr(self, "__agent_schema"):
            return self.__agent_schema
        raise NotImplementedError("Agent schema not defined")
    
    @abstractmethod
    def call(self, *args, **kwargs):
        """调用Agent的方法，必须由子类实现"""
        raise NotImplementedError("Agent call method not implemented")
    