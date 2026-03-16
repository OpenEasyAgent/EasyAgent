import pytest
from easyagent.webui.utils.monitor import SystemMonitor
from easyagent.messages.text import TextMessage


class TestSystemMonitor:
    """SystemMonitor 测试类"""

    def test_get_system_status(self):
        """测试获取系统状态"""
        status = SystemMonitor.get_system_status()

        assert "cpu" in status
        assert "memory" in status

    def test_get_system_metrics(self):
        """测试获取系统指标"""
        metrics = SystemMonitor.get_system_metrics()

        assert "cpu" in metrics
        assert "memory" in metrics
        assert "disk" in metrics
        assert "timestamp" in metrics

    def test_get_agents_status(self):
        """测试获取 Agent 状态"""
        status = SystemMonitor.get_agents_status()

        assert isinstance(status, list)

    def test_register_agent(self):
        """测试注册 Agent"""
        agent_id = "test_agent_123"
        agent_info = {
            "id": agent_id,
            "type": "ChatAgent",
            "model_name": "gpt-4",
            "status": "active",
        }

        SystemMonitor.register_agent(agent_id, agent_info)

        agent = SystemMonitor.get_agent(agent_id)
        assert agent is not None
        assert agent["id"] == agent_id

    def test_unregister_agent(self):
        """测试注销 Agent"""
        agent_id = "test_agent_456"
        agent_info = {"id": agent_id, "type": "ChatAgent"}

        SystemMonitor.register_agent(agent_id, agent_info)

        success = SystemMonitor.unregister_agent(agent_id)
        assert success is True

        agent = SystemMonitor.get_agent(agent_id)
        assert agent is None

    def test_unregister_nonexistent_agent(self):
        """测试注销不存在的 Agent"""
        success = SystemMonitor.unregister_agent("nonexistent_agent")
        assert success is False

    def test_model_info(self):
        """测试模型信息"""
        info = SystemMonitor.get_model_info()

        assert "model_name" in info
        assert "temperature" in info
        assert "max_tokens" in info

    def test_update_model_params(self):
        """测试更新模型参数"""
        SystemMonitor.update_model_params({"temperature": 0.9, "max_tokens": 200})

        new_info = SystemMonitor.get_model_info()
        assert new_info["temperature"] == 0.9
        assert new_info["max_tokens"] == 200

    def test_get_available_tools(self):
        """测试获取可用工具"""
        tools = SystemMonitor.get_available_tools()

        assert isinstance(tools, list)

    def test_register_tool(self):
        """测试注册工具"""
        tool_name = "test_tool"

        success = SystemMonitor.register_tool(tool_name, "Test tool description")
        assert success is True

        success = SystemMonitor.register_tool(tool_name, "Another description")
        assert success is False

    def test_get_current_timestamp(self):
        """测试获取时间戳"""
        timestamp = SystemMonitor.get_current_timestamp()

        assert isinstance(timestamp, str)
        assert len(timestamp) > 0
