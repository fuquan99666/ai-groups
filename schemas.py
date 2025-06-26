from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, List, Callable, Optional

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

    def model_dump(self):
        return {"role": self.role, "content": self.content}

class ToolMessage(ChatMessage):
    tool_call_id: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str
    stream: bool
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 500
    tools: Optional[List[Dict]] = Field(
        default=None,
        description="【可选】工具定义列表，当使用功能调用时需要传递"
    )

# --------------
# 待修改
# --------------

class ToolParameter(BaseModel):
    """工具参数定义规范"""
    name: str
    # type: str = Field(..., regex="string|number|integer|boolean")
    description: str
    enum: Optional[List[str]] = None  # 可选值约束

class FunctionDefinition(BaseModel):
    """函数工具定义规范"""
    name: str
    description: str
    parameters: Dict[str, ToolParameter]
    required_params: List[str]
    execute: Callable  # 实际执行函数

class Tool(BaseModel):
    """工具元数据规范"""
    type: str = "function"
    function: FunctionDefinition

class IOInterface:
    """输入输出接口抽象类"""
    @classmethod
    def input(cls, prompt: str = "") -> str:
        """获取用户输入的抽象方法"""
        raise NotImplementedError
    
    @classmethod
    def output(cls, message: str) -> None:
        """输出内容的抽象方法"""
        raise NotImplementedError

class StandardIO(IOInterface):
    """标准控制台输入输出"""
    @classmethod
    def input(cls, prompt: str = "") -> str:
        return input(prompt)
    
    @classmethod
    def output(cls, message: str) -> None:
        print(message)