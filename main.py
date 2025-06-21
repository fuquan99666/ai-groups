import json
from schemas import ChatRequest, ChatMessage, ToolMessage
from core.model_api import openai_chat_non_stream
from tools.get_weather import tools, get_weather
from test import tianqi

# 运行一次 chat 请求
def run_chat(request: ChatRequest):
    try:
        reply = next(openai_chat_non_stream(request))
        return reply
    except Exception as e:
        print("出错了：", e)
        return None


# 如果模型调用工具，处理工具函数
def handle_tool_call(reply, messages):
    tool_call = reply.get("tool")
    if not tool_call:
        return reply  # 没有调用工具，直接返回原始回复

    # 解析工具调用
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    if "city" in function_args:
        function_args["city"] = function_args["city"].capitalize()
        function_args["adm"]=function_args["adm"].capitalize()

    tool_call_id = tool_call.id
    
    func_map = {
        "get_weather": tianqi
    }
    # 调用实际函数
    result = func_map[function_name](**function_args)

    # 添加 ToolMessage 到上下文中
    messages.append(ToolMessage(role="tool", tool_call_id=tool_call_id, content=str(result)))

    # 再次发起请求
    new_request = ChatRequest(
        model="deepseek-ai/DeepSeek-V3",
        messages=messages,
        tools=tools,
        stream=False
    )
    return run_chat(new_request)


# 主程序：支持多轮聊天
def main():
    print("🤖 聊天助手已启动，输入 `exit` 退出\n")
    
    # 初始上下文（带 system prompt）
    messages = [
        ChatMessage(role="system", content=(
            "你是一个助理。如果你知道答案就直接回答；"
            "如果你无法回答时，再调用工具函数来获取信息。"
        ))
    ]

    while True:
        user_input = input("你：")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("👋 再见！")
            break

        # 添加用户消息
        messages.append(ChatMessage(role="user", content=user_input))

        # 发起请求
        request = ChatRequest(
            model="deepseek-ai/DeepSeek-V3",
            messages=messages,
            tools=tools,
            stream=False
        )

        reply = run_chat(request)

        if not reply:
            print("🤖 出现错误，请重试。")
            continue

        # 如果调用了工具
        if reply.get("tool"):
            reply = handle_tool_call(reply, messages)

        # 添加最终回复到消息列表中
        messages.append(ChatMessage(role="assistant", content=reply["content"]))
        print("🤖", reply["content"])


if __name__ == "__main__":
    main()
