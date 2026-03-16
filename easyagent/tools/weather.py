from easyagent.core.base import Tool
from easyagent.messages.text import TextMessage
from typing import Dict, Any, Optional
import requests
import json


class WeatherAPI(Tool):
    """天气查询工具"""

    __tool_schema: Dict[str, Any] = {
        "type": "function",
        "function": {
            "name": "weather",
            "description": "查询指定城市的天气信息，包括温度、湿度、风力、空气质量等",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，例如: 北京、上海、London",
                    },
                    "units": {
                        "type": "string",
                        "description": "温度单位，可选值: metric(摄氏度), imperial(华氏度), standard(开尔文)",
                        "enum": ["metric", "imperial", "standard"],
                        "default": "metric",
                    },
                },
                "required": ["city"],
            },
        },
    }

    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.api_key = api_key

    @property
    def schema(self) -> Dict[str, Any]:
        return self.__tool_schema

    def call(self, city: str, units: str = "metric") -> TextMessage:
        """查询城市天气

        Args:
            city: 城市名称
            units: 温度单位，可选值: metric(摄氏度), imperial(华氏度), standard(开尔文)

        Returns:
            天气信息文本消息
        """
        if not self.api_key:
            return self._simulated_weather(city, units)

        try:
            weather_data = self._fetch_weather(city, units)
            return self._format_weather(weather_data, city)
        except Exception as e:
            return TextMessage(f"天气查询出错: {str(e)}", source="tool")

    def _fetch_weather(self, city: str, units: str) -> Dict[str, Any]:
        """从API获取天气数据"""
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": self.api_key, "units": units}
        response = requests.get(url, params=params)
        if response.status_code == 404:
            raise ValueError(f"未找到城市: {city}")
        if response.status_code != 200:
            raise ValueError(f"API请求失败: {response.status_code}")
        return response.json()

    def _simulated_weather(self, city: str, units: str) -> TextMessage:
        """模拟天气数据（当没有API密钥时使用）"""
        unit_str = {"metric": "°C", "imperial": "°F", "standard": "K"}.get(units, "°C")

        weather_info = f"""【{city}】天气预报（模拟数据）

🌡️ 温度: 22{unit_str}
💧 湿度: 65%
🌤️ 天气: 多云
🌬️ 风力: 3级，东南风
👁️ 能见度: 10公里
�气压: 1013 hPa

备注: 此为模拟数据，实际使用请配置 API Key
获取免费 API Key: https://openweathermap.org/api"""

        return TextMessage(weather_info, source="tool")

    def _format_weather(self, data: Dict[str, Any], city: str) -> TextMessage:
        """格式化天气数据"""
        main = data.get("main", {})
        weather = data.get("weather", [{}])[0]
        wind = data.get("wind", {})

        temp = main.get("temp")
        feels_like = main.get("feels_like")
        humidity = main.get("humidity")
        pressure = main.get("pressure")
        description = weather.get("description", "未知")
        wind_speed = wind.get("speed", "未知")

        unit_str = "°C"

        weather_info = f"""【{city}】天气预报

🌡️ 温度: {temp}{unit_str} (体感: {feels_like}{unit_str})
💧 湿度: {humidity}%
🌤️ 天气: {description}
🌬️ 风力: {wind_speed} m/s
�气压: {pressure} hPa"""

        return TextMessage(weather_info, source="tool")
