# webui/utils/monitor.py
import psutil
import time
from typing import Dict, Any, List, Optional
from datetime import datetime


class SystemMonitor:
    """系统监控工具"""

    _agents: Dict[str, Dict[str, Any]] = {}
    _tools: Dict[str, Dict[str, Any]] = {}
    _model_params: Dict[str, Any] = {
        "model_name": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 150,
    }
    _next_id: int = 1

    @staticmethod
    def get_system_status() -> Dict[str, Any]:
        """获取系统状态"""
        return {"cpu": psutil.cpu_percent(), "memory": psutil.virtual_memory().percent}

    @staticmethod
    def get_agents_status() -> List[Dict[str, Any]]:
        """获取所有Agent状态"""
        return list(SystemMonitor._agents.values())

    @staticmethod
    def get_agent(agent_id: str) -> Optional[Dict[str, Any]]:
        """获取指定Agent"""
        return SystemMonitor._agents.get(agent_id)

    @staticmethod
    def register_agent(agent_id: str, agent_info: Dict[str, Any]) -> None:
        """注册Agent"""
        SystemMonitor._agents[agent_id] = agent_info

    @staticmethod
    def unregister_agent(agent_id: str) -> bool:
        """注销Agent"""
        if agent_id in SystemMonitor._agents:
            del SystemMonitor._agents[agent_id]
            return True
        return False

    @staticmethod
    def get_next_id() -> int:
        """获取下一个ID"""
        SystemMonitor._next_id += 1
        return SystemMonitor._next_id

    @staticmethod
    def get_current_timestamp() -> str:
        """获取当前时间戳"""
        return datetime.now().isoformat()

    @staticmethod
    def get_model_info() -> Dict[str, Any]:
        """获取模型信息"""
        return SystemMonitor._model_params.copy()

    @staticmethod
    def update_model_params(params: Dict[str, Any]) -> None:
        """更新模型参数"""
        SystemMonitor._model_params.update(params)

    @staticmethod
    def get_available_tools() -> List[Dict[str, Any]]:
        """获取可用工具列表"""
        return list(SystemMonitor._tools.values())

    @staticmethod
    def register_tool(tool_name: str, tool_description: str = "") -> bool:
        """注册工具"""
        if tool_name in SystemMonitor._tools:
            return False
        SystemMonitor._tools[tool_name] = {
            "name": tool_name,
            "description": tool_description,
            "registered_at": SystemMonitor.get_current_timestamp(),
        }
        return True

    @staticmethod
    def get_system_metrics() -> Dict[str, Any]:
        """获取系统指标"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        return {
            "cpu": {"percent": cpu_percent, "count": psutil.cpu_count()},
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used,
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent,
            },
            "timestamp": SystemMonitor.get_current_timestamp(),
        }
