# webui/routes.py
from flask import Blueprint, jsonify, render_template, request
from easyagent.webui.utils.monitor import SystemMonitor

web_bp = Blueprint("webui", __name__)


@web_bp.route("/")
def index():
    """首页路由"""
    return render_template("dashboard.html")


@web_bp.route("/dashboard")
def control_panel():
    """控制面板页面"""
    return render_template("dashboard.html")


@web_bp.route("/api/health")
def health_check():
    """健康检查"""
    return jsonify({"status": "ok", "service": "EasyAgent"})


@web_bp.route("/api/agent/status")
def get_agent_status():
    """获取所有Agent运行状态"""
    return jsonify(SystemMonitor.get_agents_status())


@web_bp.route("/api/agent/create", methods=["POST"])
def create_agent():
    """创建新Agent"""
    data = request.get_json() or {}

    agent_id = data.get("agent_id", "agent_" + str(SystemMonitor.get_next_id()))
    agent_type = data.get("type", "ChatAgent")
    model_name = data.get("model_name", "gpt-4")

    agent_info = {
        "id": agent_id,
        "type": agent_type,
        "model_name": model_name,
        "status": "active",
        "created_at": SystemMonitor.get_current_timestamp(),
    }

    SystemMonitor.register_agent(agent_id, agent_info)

    return jsonify(
        {"success": True, "agent_id": agent_id, "message": f"Agent {agent_id} 创建成功"}
    )


@web_bp.route("/api/agent/<agent_id>", methods=["DELETE"])
def delete_agent(agent_id):
    """删除Agent"""
    success = SystemMonitor.unregister_agent(agent_id)

    if success:
        return jsonify({"success": True, "message": f"Agent {agent_id} 已删除"})
    else:
        return jsonify({"success": False, "error": f"Agent {agent_id} 不存在"}), 404


@web_bp.route("/api/agent/<agent_id>/chat", methods=["POST"])
def chat_with_agent(agent_id):
    """与Agent聊天"""
    data = request.get_json() or {}
    message = data.get("message", "")

    agent_info = SystemMonitor.get_agent(agent_id)
    if not agent_info:
        return jsonify({"success": False, "error": f"Agent {agent_id} 不存在"}), 404

    return jsonify(
        {
            "success": True,
            "agent_id": agent_id,
            "message": message,
            "response": "这是一个模拟响应，实际使用需要配置API Key",
        }
    )


@web_bp.route("/api/model/info")
def get_model_info():
    """获取当前模型信息"""
    return jsonify(SystemMonitor.get_model_info())


@web_bp.route("/api/model/update", methods=["POST"])
def update_model_params():
    """更新模型参数"""
    data = request.get_json() or {}

    model_name = data.get("model_name")
    temperature = data.get("temperature")
    max_tokens = data.get("max_tokens")

    updates = {}
    if model_name:
        updates["model_name"] = model_name
    if temperature is not None:
        updates["temperature"] = temperature
    if max_tokens is not None:
        updates["max_tokens"] = max_tokens

    SystemMonitor.update_model_params(updates)

    return jsonify({"success": True, "message": "模型参数已更新", "updates": updates})


@web_bp.route("/api/tool/list")
def list_tools():
    """列出所有可用工具"""
    return jsonify(SystemMonitor.get_available_tools())


@web_bp.route("/api/tool/register", methods=["POST"])
def register_tool():
    """注册新工具"""
    data = request.get_json() or {}

    tool_name = data.get("name")
    tool_description = data.get("description")

    if not tool_name:
        return jsonify({"success": False, "error": "工具名称不能为空"}), 400

    success = SystemMonitor.register_tool(tool_name, tool_description)

    if success:
        return jsonify({"success": True, "message": f"工具 {tool_name} 注册成功"})
    else:
        return jsonify({"success": False, "error": f"工具 {tool_name} 已存在"}), 400


@web_bp.route("/api/system/metrics")
def get_system_metrics():
    """获取系统指标"""
    return jsonify(SystemMonitor.get_system_metrics())
