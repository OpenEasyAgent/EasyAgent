from easyagent.core.base import Message

from typing import Literal

class TextMessage(Message):
    """
    文本消息类
    """
    
    __message_schema = {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "文本内容"
            }
        },
        "required": ["text"]
    }
    
    def __init__(self, text: str, source: str = "system") -> None:
        """
        初始化文本消息
        :param text: 文本内容
        :param source: 消息来源
        """
        super().__init__(source=source)
        self.text = text

    def __add__(self, other: "TextMessage") -> "TextMessage":
        """
        重载加法运算符
        :param other: 另一个文本消息对象
        :return: 新的文本消息对象
        
        将两个文本消息的内容连接在一起，并返回一个新的文本消息对象
        souce属性为自身的source属性
        """
        return TextMessage(self.text + other.text, source=self.source)
    
    def __iadd__(self, other: "TextMessage") -> "TextMessage":
        """
        重载加法赋值运算符
        :param other: 另一个文本消息对象
        :return: 自身对象
        
        将另一个文本消息的内容连接到自身的文本消息中，并返回自身对象
        source属性为自身的source属性
        """
        self.text += other.text
        return self
    
    def __len__(self) -> int:
        """
        重载len函数
        :return: 文本长度
        """
        return len(self.text)
    
    def __getitem__(self, item: slice) -> str:
        """
        重载索引运算符
        :param item: 索引
        :return: 索引位置的字符
        
        返回文本消息中指定索引位置的字符
        """
        return self.text[item]
    
    def __contains__(self, item: str) -> bool:
        """
        重载in运算符
        :param item: 字符
        :return: 是否包含
        
        判断文本消息中是否包含指定字符
        """
        return item in self.text
    
    def __eq__(self, other: object) -> bool:
        """
        重载等于运算符
        :param other: 另一个文本消息对象
        :return: 是否相等
        
        判断两个文本消息的内容和来源是否相等
        如果内容和来源都相等，则返回True，否则返回False
        """
        if not isinstance(other, TextMessage):
            return NotImplemented
        return self.text == other.text and self.source == other.source

    def __ne__(self, other: object) -> bool:
        """
        重载不等于运算符
        :param other: 另一个文本消息对象
        :return: 是否不相等
        
        判断两个文本消息的内容和来源是否不相等
        如果内容和来源都不相等，则返回True，否则返回False
        """
        return not self.__eq__(other)
    
    def __str__(self) -> str:
        """
        返回文本消息的字符串表示
        :return: 文本内容
        """
        return self.text
    
    def __repr__(self) -> str:
        """
        返回文本消息的详细字符串表示
        :return: 文本消息对象的字符串表示
        """
        return f"<TextMessage: {self.text}, source: {self.source}>"