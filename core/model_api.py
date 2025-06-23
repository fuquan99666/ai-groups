import httpx
import logging

from openai import OpenAI
from schemas import ChatMessage, ChatRequest
from config import MODEL_CONFIG

# 同步版本
def openai_chat_non_stream(request: ChatRequest):

    model_config = MODEL_CONFIG.get(request.model)
    if not model_config:
        raise ValueError(f"未找到模型 {request.model} 的配置")
    
    # 动态创建客户端
    client = OpenAI(
        api_key=model_config["api_key"],
        base_url=model_config["base_url"]
    )

    # 构造请求参数（Pydantic模型转字典）▼
    params = {
        "model": request.model,
        "messages": [m.model_dump() for m in request.messages],
        "temperature": request.temperature,
        "top_p": request.top_p,
        "max_tokens": request.max_tokens,
        "stream": request.stream,  # 根据请求传递stream参数
        "tools": request.tools
    }
    if request.stream:
        response = client.chat.completions.create(**params)
        for chunk in response:
            for char_msg in parse_openai_chunk(chunk):
                yield char_msg
    else:
        response = client.chat.completions.create(**params)
        yield format_non_stream_response(response)


# 新增非流式响应适配器
def format_non_stream_response(response) -> dict:
    """将非流式响应转换为流式结构模拟输出"""
    msg = response.choices[0].message
    # 也许应该return一个ChatMessage
    return {
        "content": msg.content,
        "role": msg.role,
        "tool": msg.tool_calls[0] if msg.tool_calls else None
    }

# 更新chunk解析方法（兼容对象直接处理）

def parse_openai_chunk(chunk) -> list:
    """解析 OpenAI SDK 返回的 chunk 对象，支持内容和工具调用"""
    if not chunk.choices:
        return []

    choice = chunk.choices[0]
    delta = choice.delta
    content = delta.content or ""
    role = delta.role or "assistant"
    finish_reason = choice.finish_reason

    results = []

    # 普通内容逐字符处理
    for ch in content:
        results.append({
            "content": ch,
            "role": role,
            "finish_reason": finish_reason,
            "delta": {"content": ch},
            "chunk": chunk.model_dump()
        })

    # 工具调用部分（注意：是 delta.tool_calls）
    if hasattr(delta, "tool_calls") and delta.tool_calls:
        
        for tool in delta.tool_calls:
            
            results.append({
                "content": "",
                "role": role,
                "tool": {
                    "id": tool.id,
                    "name": tool.function.name,
                    "arguments": tool.function.arguments or ""
                },
                "is_tool_call": True,
                "finish_reason": finish_reason,
                "delta": delta.model_dump(),
                "chunk": chunk.model_dump()
            })

    return results

