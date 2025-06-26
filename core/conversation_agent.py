from core.memory_manager import MemoryManager
from core.model_api import openai_chat_non_stream
from schemas import ChatRequest, ChatMessage, ToolMessage
from tools.get_weather import tools

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
            tools=tools,
            stream=True
        )

        # 生成响应（这里接入LLM）
        reply_content = ""
        for chunk in self._generate_response(request):
            yield chunk
            reply_content += chunk
        
        # 添加AI回复
        self.memory.add_message("assistant", chunk)
    
    def _generate_response(self, request: ChatRequest) -> str:
        """模拟AI响应生成（实际应替换为真实模型调用）"""
        # 这里可以添加基于记忆的逻辑
        reply_content = ""
        for chunk in openai_chat_non_stream(request):
            content_piece = chunk["content"]
            yield content_piece
        