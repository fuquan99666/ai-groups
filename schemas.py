from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 500
    tool_name: Optional[str] = None  # 外部工具标识
