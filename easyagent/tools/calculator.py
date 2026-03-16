from easyagent.core.base import Tool
from easyagent.messages.text import TextMessage
from typing import Dict, Any
import ast
import operator


class Calculator(Tool):
    """计算器工具，支持数学表达式计算"""

    __tool_schema: Dict[str, Any] = {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式的结果，支持加减乘除、幂运算、括号等",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，例如: 2+2, 10*5, (3+4)*2",
                    }
                },
                "required": ["expression"],
            },
        },
    }

    SAFE_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def __init__(self):
        super().__init__()

    @property
    def schema(self) -> Dict[str, Any]:
        return self.__tool_schema

    def call(self, expression: str) -> TextMessage:
        """计算数学表达式

        Args:
            expression: 数学表达式字符串

        Returns:
            计算结果文本消息
        """
        try:
            result = self._safe_eval(expression)
            return TextMessage(f"计算结果: {expression} = {result}", source="tool")
        except Exception as e:
            return TextMessage(f"计算错误: {str(e)}", source="tool")

    def _safe_eval(self, expr: str) -> float:
        """安全地计算数学表达式"""
        expr = expr.strip()

        try:
            result = ast.literal_eval(expr)
            if isinstance(result, (int, float)):
                return result
            raise ValueError("表达式结果不是数字")
        except (ValueError, SyntaxError):
            pass

        return self._eval_expression(expr)

    def _eval_expression(self, expr: str) -> float:
        """解析并计算表达式"""
        node = ast.parse(expr, mode="eval")
        return self._eval_node(node.body)

    def _eval_node(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("表达式结果不是数字")
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type in self.SAFE_OPERATORS:
                return self.SAFE_OPERATORS[op_type](left, right)
            raise ValueError(f"不支持的操作符: {op_type.__name__}")
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in self.SAFE_OPERATORS:
                return self.SAFE_OPERATORS[op_type](operand)
            raise ValueError(f"不支持的操作符: {op_type.__name__}")
        else:
            raise ValueError(f"不支持的表达式节点: {type(node).__name__}")
