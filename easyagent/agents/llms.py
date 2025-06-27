from easyagent.core.base import Agent
from easyagent.messages.text import TextMessage

from openai import OpenAI

class LLM(Agent):
    """
    LLM（大语言模型）基类，所有LLM应继承此类
    """

    __agent_schema = {
        "type": "object",
        "properties": {
            "model_name": {
                "type": "string",
                "description": "模型名称"
            },
            "api_key": {
                "type": "string",
                "description": "API密钥"
            }
        },
        "required": ["model_name", "api_key"]
    }

    def __init__(self, model_name: str, api_key: str) -> None:
        """
        初始化LLM
        :param model_name: 模型名称
        :param api_key: API密钥
        """
        super().__init__()
        self.model_name = model_name
        self.api_key = api_key

    def call(self, prompt: TextMessage) -> TextMessage:
        """
        调用LLM生成文本
        :param prompt: 输入的文本消息
        :return: 生成的文本消息
        """
        raise NotImplementedError("LLM call method not implemented")

class OpenAILLM(LLM):
    """
    OpenAI LLM实现
    """
    __agent_schema = {
        "type": "object",
        "properties": {
            "model_name": {
                "type": "string",
                "description": "OpenAI模型名称"
            },
            "api_key": {
                "type": "string",
                "description": "OpenAI API密钥"
            },
            "temperature": {
                "type": "number",
                "description": "生成文本的温度参数",
                "default": 0.7
            },
            "max_tokens": {
                "type": "integer",
                "description": "生成文本的最大token数",
                "default": 150
            },
            "top_p": {
                "type": "number",
                "description": "生成文本的top_p参数",
                "default": 1.0
            },
            "frequency_penalty": {
                "type": "number",
                "description": "生成文本的频率惩罚参数",
                "default": 0.0
            },
            "presence_penalty": {
                "type": "number",
                "description": "生成文本的存在惩罚参数",
                "default": 0.0
            },
            "stop": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "生成文本的停止符号"
            },
        },
        "required": ["model_name", "api_key"],
    }
    
    def __init__(self,
                    model_name: str,
                    api_key: str,
                    temperature: float = 0.7,
                    max_tokens: int = 150,
                    top_p: float = 1.0,
                    frequency_penalty: float = 0.0,
                    presence_penalty: float = 0.0,
                    stop: list | None = None) -> None:
        """

        Args:
            model_name (str): _description_
            api_key (str): _description_
            temperature (float, optional): _description_. Defaults to 0.7.
            max_tokens (int, optional): _description_. Defaults to 150.
            top_p (float, optional): _description_. Defaults to 1.0.
            frequency_penalty (float, optional): _description_. Defaults to 0.0.
            presence_penalty (float, optional): _description_. Defaults to 0.0.
            stop (list | None, optional): _description_. Defaults to None.
        
        """
        
        super().__init__(model_name, api_key)
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = stop if stop is not None else []
        
        self.client = OpenAI(api_key=self.api_key)
        
    def call(self, prompt: TextMessage) -> TextMessage:
        """
        调用OpenAI LLM生成文本
        :param prompt: 输入的文本消息
        :return: 生成的文本消息
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt.text}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            stop=self.stop
        )
        
        content = response.choices[0].message.content
        generated_text = content.strip() if content is not None else ""
        return TextMessage(generated_text, source=self.model_name)

