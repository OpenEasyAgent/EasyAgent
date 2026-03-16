from easyagent.messages.text import TextMessage
from typing import List, Dict, Any


def text_list_to_openai_messages(
    text_list: TextMessage | List[TextMessage],
) -> List[Dict[str, Any]]:
    """
    将文本消息列表转换为OpenAI消息格式
    :param text_list: 文本消息或文本消息列表
    :return: OpenAI消息格式的字典列表
    """
    if isinstance(text_list, TextMessage):
        text_list = [
            text_list,
        ]

    messages = []

    for msg in text_list:
        if msg.source == "user":
            messages.append({"role": "user", "content": msg.text})
        elif msg.source == "assistant":
            messages.append({"role": "assistant", "content": msg.text})
        elif msg.source == "system":
            messages.append({"role": "system", "content": msg.text})
        elif msg.source == "developer":
            messages.append({"role": "developer", "content": msg.text})
        else:
            messages.append({"role": "system", "content": msg.text})
    return messages
