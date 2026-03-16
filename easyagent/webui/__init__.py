from flask import Flask
from easyagent.webui.routes import web_bp


def create_app(config=None):
    """创建Flask应用

    Args:
        config: 配置字典

    Returns:
        Flask应用实例
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")

    if config:
        app.config.update(config)

    app.register_blueprint(web_bp)

    return app


def run_app(host="0.0.0.0", port=5000, debug=True):
    """运行Flask应用

    Args:
        host: 主机地址
        port: 端口号
        debug: 调试模式
    """
    app = create_app()
    app.run(host=host, port=port, debug=debug)
