from openai import OpenAI
from typing import Dict, Any, Callable
from tools.python_execute import PythonExecutor
from tools.get_weather import get_weather_func
from tools.pku_course import fetch_pku_course_updates

class ToolManager:
    def __init__(self):
        self._tools = {}      # 工具函数字典
        self._schemas = []    # OpenAI格式的工具描述
    
    def register(self, name: str, description: str, parameters: Dict[str, Any]) -> Callable:
        """装饰器注册工具"""
        def decorator(func: Callable):
            self._tools[name] = func
            self._schemas.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": {
                        "type": "object",
                        "properties": parameters,
                        "required": list(parameters.keys())
                    }
                }
            })
            return func
        return decorator
    
    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """执行工具并返回结果字符串"""
        if tool_name not in self._tools:
            return f"Error: Tool {tool_name} not found"
        return str(self._tools[tool_name](**arguments))
    
    @property
    def tools(self) -> list:
        """获取OpenAI格式的工具列表"""
        return self._schemas
    
tool_manager = ToolManager()
# 1. 注册计算器工具
@tool_manager.register(
    name="calculator",
    description="Evaluate math expressions",
    parameters={
        "expression": {"type": "string", "description": "Math expression like '2+3*5'"}
    }
)
def calculate(expression: str) -> float:
    import math
    return eval(expression, {"math": math})

# 2. 注册天气查询工具（模拟实现）
@tool_manager.register(
    name="get_weather",
    description="Get current weather for a location (专业天气查询)",
    parameters={
        "location": {"type": "string", "description": "City name like 'Hangzhou'"}
    }
)
def get_weather(location: str) -> str:
    return get_weather_func(location)

# 3. 注册python代码执行工具
@tool_manager.register(
    name="python_execute",
    description="安全执行简单的Python代码，仅支持基础数学和部分内置函数",
    parameters={
        "code": {"type": "string", "description": "要执行的Python代码"}
    }
)
def python_execute(code: str) -> str:
    import asyncio
    executor = PythonExecutor()
    return asyncio.run(executor.execute(code))

@tool_manager.register(
    name="pku_course",
    description="获取北京大学选课系统的课程更新信息，包括作业DDL、公告等。需要提供用户名和密码。",
    parameters={
    }
)
def pku_course() -> str:
    """
    查询北大选课系统的课程更新（如DDL、公告等）。
    """
    return fetch_pku_course_updates()