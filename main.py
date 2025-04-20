import asyncio
import json

from schemas import ChatRequest, ChatMessage, ToolMessage
from core.model_api import openai_chat_non_stream
from tools.get_weather import tools, get_weather

# 示例1：通过ChatRequest传递参数
request = ChatRequest(
    model="deepseek-ai/DeepSeek-V3",
    messages=[
        ChatMessage(role="system", content="You are a helpful assistant"),
        ChatMessage(role="user", content="Hello")
    ],
    stream=False
)

response_chunk = next(openai_chat_non_stream(request))
print(response_chunk['content'])  
# 输出：Hello! How can I assist you today?

# 实例2：查询天气功能调用
messages = [ChatMessage(role="user", content="上海天气怎么样")]
request = ChatRequest(
    model="deepseek-ai/DeepSeek-V3",
    messages=messages,
    tools=tools,
    stream=False
)
reply = next(openai_chat_non_stream(request))
# print(reply)
# messages.append(reply)

function_args = json.loads(reply["tool"].function.arguments)
function_name = reply["tool"].function.name
tool_call_id = reply["tool"].id

func_list = {
    "get_weather": get_weather
}

result = func_list[function_name](**function_args)
messages.append(ToolMessage(role="tool", tool_call_id=tool_call_id, content=str(result)))
request = ChatRequest(
    model="deepseek-ai/DeepSeek-V3",
    messages=messages,
    tools=tools,
    stream=False
)

reply = next(openai_chat_non_stream(request))
print(reply["content"])

