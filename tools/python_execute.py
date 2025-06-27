import ast
import io
import contextlib
from textwrap import dedent
import math
import random
import datetime

class SecurityError(Exception):
    """自定义安全异常"""
    pass

class PythonExecutor:
    def __init__(self):
        self.allowed_modules = {"math", "datetime", "random"}
        # 允许的安全内置函数
        self.safe_builtins = {
            "print": print,
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "pow": pow,
            "len": len,
            "range": range,
        }

    def _sanitize_code(self, code: str) -> str:
        """安全检查：禁止危险操作"""
        tree = ast.parse(dedent(code))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                raise SecurityError("不允许导入模块")
            if isinstance(node, ast.ImportFrom):
                if node.module not in self.allowed_modules:
                    raise SecurityError(f"禁止导入模块: {node.module}")
            # 禁止exec、eval、open等危险函数
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in {"exec", "eval", "open", "compile", "input", "__import__"}:
                    raise SecurityError(f"禁止使用危险函数: {node.func.id}")
        return code

    async def execute(self, code: str) -> str:
        output = io.StringIO()
        try:
            sanitized_code = self._sanitize_code(code)
            # 允许安全内置和部分安全模块
            safe_globals = {
                "__builtins__": self.safe_builtins,
                "math": math,
                "random": random,
                "datetime": datetime,
            }
            with contextlib.redirect_stdout(output):
                exec(sanitized_code, safe_globals)
            return output.getvalue()
        except Exception as e:
            return f"EXECUTION ERROR: {type(e).__name__} - {str(e)}"
