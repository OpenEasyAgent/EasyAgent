#!/usr/bin/env python
# run_web.py
"""EasyAgent Web 控制台启动脚本"""

import os
import sys

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from easyagent.webui.routes import web_bp
from easyagent.webui.utils.monitor import SystemMonitor


def create_app():
    """创建并配置 Flask 应用"""
    app = Flask(
        __name__,
        template_folder="easyagent/webui/templates",
        static_folder="easyagent/webui/static",
    )

    app.register_blueprint(web_bp)

    # 注册默认工具
    _register_default_tools()

    return app


def _register_default_tools():
    """注册默认工具"""
    default_tools = [
        {"name": "search_engine", "description": "搜索引擎工具"},
        {"name": "calculator", "description": "计算器工具"},
        {"name": "weather", "description": "天气查询工具"},
    ]

    for tool in default_tools:
        SystemMonitor.register_tool(tool["name"], tool["description"])


def main():
    """主函数"""
    app = create_app()

    print("=" * 50)
    print("EasyAgent Web 控制台")
    print("=" * 50)
    print("启动地址: http://localhost:4090")
    print("按 Ctrl+C 停止服务")
    print("=" * 50)

    app.run(host="0.0.0.0", port=4090, debug=True)


if __name__ == "__main__":
    main()
