import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
import json
from schemas import ChatRequest, ChatMessage, ToolMessage
from core.model_api import openai_chat_non_stream
from tools.get_weather import tools, get_weather
from test import tianqi
import time
from check import check_output_format as ce
import ui

stream=True

# 运行一次 chat 请求
def run_chat(request: ChatRequest):
    try:
        if request.stream:
            reply_content = ""
            print("🤖:", end=" ")

            tool_call_final = None
            toolname = None
            toolid = None
            arguments_parts = []  # ✅ 用来拼接 arguments
            got_tool_info = False

            for chunk in openai_chat_non_stream(request):
                
                if chunk.get("is_tool_call"):
                    tool = chunk["tool"]
                    # 第一个 tool_call：记录 id 和 name
                    if not got_tool_info:
                        toolname = tool.get("name")
                        toolid = tool.get("id")
                        got_tool_info = True

                    # 每段 arguments 都拼进来
                    arguments_parts.append(tool.get("arguments", ""))
                    continue  # 工具块不输出文本

                # 普通文本块
                content_piece = chunk["content"]
                print(content_piece, end="", flush=True)
                time.sleep(0.05)
                reply_content += content_piece

            print()
            # ✅ 拼出完整 tool 调用
            if got_tool_info:
                tool_call_final = {
                    "id": toolid,
                    "name": toolname,
                    "arguments": "".join(arguments_parts)
                }
                

            return {
                "content": reply_content,
                "tool": tool_call_final
            }

        else:
            reply = next(openai_chat_non_stream(request))
            print("🤖:", reply["content"])
            return reply

    except Exception as e:
        print("❌ 出错了：", e)
        return None



# 如果模型调用工具，处理工具函数
def handle_tool_call(reply, messages):
    if not stream:
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
            stream=stream
        )
        return run_chat(new_request)
    else:
        tool_call=reply["tool"]
        function_name = tool_call["name"]
        function_args =json.loads(tool_call["arguments"])

        if "city" in function_args:
            function_args["city"] = function_args["city"].capitalize()
            function_args["adm"]=function_args["adm"].capitalize()

        tool_call_id = tool_call["id"]
        
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
            stream=stream
        )
        return run_chat(new_request)

# 主程序：支持多轮聊天
def main():
    app = QApplication(sys.argv)  # 创建 QApplication 实例
    # 设置全局字体，确保中文正常显示
    font = QFont("SimHei")
    app.setFont(font)


    # 初始化 UI
    chatui = ui.ChatUI()
    chatui.show()


    print("🤖 聊天助手已启动，输入 `exit` 退出\n")
    
    # 初始上下文（带 system prompt）
    messages = [
        ChatMessage(
            role="system",
            content=(
                "你是一个智能出行助手。\n"
                "用户会提出与天气和出行有关的问题。\n"
                "请根据你当前知道的信息回答；如果你不知道天气，请调用天气查询工具函数再回答。\n\n"

                "当你查到天气数据之后再输出时，请严格遵守以下结构：\n"
                "- 城市（string）\n"
                "- 天气（string）\n"
                "- 温度范围（string，格式如“22°C ~ 30°C”）\n"
                "- 出行建议（string）\n\n"
                #"- content(这一项最好包含天气和出行建议做一个整合)\n\n"

                "⚠️ 查到天气数据之后输出时请只输出一个 JSON 对象，不要加任何解释性语言。\n"
                "⚠️ 不要使用 markdown 格式（如 ```json），直接输出纯 JSON。\n"
                "⚠️ 所有字段都必须出现，不能缺省。"
            )
        )
    ]

    def handle_user_input(user_input):
        if user_input.strip().lower() in ["exit", "quit"]:
            print("👋 再见！")
            app.quit()
            return

        # 立即显示用户消息
        messages.append(ChatMessage(role="user", content=user_input))
        request = ChatRequest(
            model="deepseek-ai/DeepSeek-V3",
            messages=messages,
            tools=tools,
            stream=stream
        )

        # 获取完整回复
        reply = run_chat(request)
        if not reply:
            print("🤖 出现错误，请重试。")
            return

        # 处理工具调用
        if reply.get("tool"):
            reply = handle_tool_call(reply, messages)
        
        full_text = reply["content"]
        
        # 打字机效果实现
        current_text = ""
        def display_next_char():
            nonlocal current_text
            if len(current_text) < len(full_text):
                current_text += full_text[len(current_text)]
                chatui.display_message("🤖", current_text)  # 注意这里使用"🤖"作为sender
                QTimer.singleShot(50, display_next_char)  # 50毫秒显示一个字
            else:
                # 完成显示后添加到消息历史
                messages.append(ChatMessage(role="assistant", content=full_text))
        
        # 开始显示
        display_next_char()
    # 连接自定义信号到槽函数
    chatui.message_sent.connect(handle_user_input)

    sys.exit(app.exec_())  # 进入应用程序的事件循环


if __name__ == "__main__":
    main()