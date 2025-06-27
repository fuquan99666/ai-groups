import json
import re
from core.memory_manager import MemoryManager
from core.model_api import openai_chat_stream
from schemas import ChatRequest, ChatMessage, ToolMessage
from tools.base import tool_manager

class ConversationAgent:
    def __init__(self, memory: MemoryManager):
        self.memory = memory
        self.current_conv_id = None
    
    def process_input(self, user_input: str):
        """处理用户输入并生成响应"""
        # 首次输入检查
        if self.memory.current_conversation is None:
            self.memory.start_new_conversation(user_input)
        
        self.memory.add_message("user", user_input)
        # 添加用户消息
        request = ChatRequest(
            model="deepseek-ai/DeepSeek-V3",
            messages=self.memory.current_conversation.messages,
            tools=tool_manager.tools,
            stream=True
        )

        # 生成响应（这里接入LLM）
        reply_content = ""
        tool_results = []
        use_tool = False
        tool_name = ""
        tool_args = ""
        tool_id = ""
        for chunk in openai_chat_stream(request):
            # 普通内容
            if chunk.get("content"):
                reply_content += chunk["content"]
                yield chunk["content"]
            # 工具调用
            if chunk.get("is_tool_call"):
                tool_info = chunk["tool"]
                use_tool = True
                if tool_info["name"] is not None:
                    tool_name += tool_info["name"]
                if tool_info["arguments"] is not None:
                    tool_args += tool_info["arguments"]
                if tool_info["id"] is not None:
                    tool_id += tool_info["id"]
        if use_tool:
            if isinstance(tool_args, str):
                try:
                    json_str = re.sub(r"^```json\s*|\s*```$", "", tool_args.strip())
                    tool_args = json.loads(json_str)
                except Exception:
                    yield f"\n[TOOL ARGS ERROR:{tool_args}]"
            # 工具执行
            try:
                tool_result = tool_manager.execute(tool_name, tool_args)

                if tool_result is not None:
                    self.memory.add_tool_message("tool", tool_result, tool_id)
                # 构造新的请求，包含工具结果
                new_request = ChatRequest(
                    model="deepseek-ai/DeepSeek-V3",
                    messages=self.memory.current_conversation.messages,
                    tools=tool_manager.tools,
                    stream=True
                )
                final_reply = ""
                for chunk in openai_chat_stream(new_request):
                    if chunk.get("content"):
                        final_reply += chunk["content"]
                        yield chunk["content"]
                self.memory.add_message("assistant", final_reply)

            except Exception as e:
                yield f"\n[TOOL ERROR:{tool_name}]: {e}\n"
        
        # 添加AI回复
        self.memory.add_message("assistant", reply_content)
    
    def _generate_response(self, request: ChatRequest) -> str:
        """模拟AI响应生成（实际应替换为真实模型调用）"""
        # 这里可以添加基于记忆的逻辑
        reply_content = ""
        for chunk in openai_chat_stream(request):
            content_piece = chunk["content"]
            yield content_piece