import queue

from resources import resources
from core.memory_manager import MemoryManager
from core.conversation_agent import ConversationAgent
from typing import List, Dict, Optional

class CLIInterface:
    """命令行交互界面"""
    def __init__(self):
        self.running = True
        self.memory = MemoryManager()
        self.agent = ConversationAgent(self.memory)
        self.output_callback = None  # 输出回调函数
        self.input_queue = queue.Queue()  # 用于接收GUI输入
    
    def set_output_callback(self, callback):
        """设置输出回调函数（由MainApp注入）"""
        self.output_callback = callback

    def _print(self, text: str, sender: str = "系统", end: str = "\n"):
        """改用回调函数输出"""
        if self.output_callback:
            self.output_callback(text, sender, end)

    def receive_input(self, text: str):
        """接收来自GUI的输入，放入队列"""
        self.input_queue.put(text)

    def _print_banner(self):
        self._print(resources.get_text("banner"))
        self._print(resources.get_text("help"), sender="")

    def _parse_command(self, input_str: str) -> tuple:
        """解析用户输入的命令和参数"""
        parts = input_str.strip().split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        return (cmd, args)
    
    def _handle_command(self, cmd: str, args: str) -> Optional[str]:
        """处理所有命令"""
        # 退出命令
        if cmd in ("exit", "quit"):
            self.running = False
            return None
        
        # 帮助命令
        elif cmd == "help":
            return resources.get_text("help")
        
        # 新建对话
        elif cmd == "new":
            self.memory = MemoryManager()
            self.agent = ConversationAgent(self.memory)
            self._print("🔄 已创建新对话，输入quit退出：")
            return "__start_conversation__"
        
        # 历史记录
        elif cmd == "history":
            conversations = self.memory.list_conversations()
  
            if not conversations:
                return "📂 暂无历史对话"
            
            lines = ["\n历史对话："]
            for i, conv in enumerate(conversations, 1):
                lines.append(
                    f"{i}. [{conv['id']}] {conv['title']} ({conv['message_count']}条消息)"
                )
            return "\n".join(lines)
        
        # 加载对话
        elif cmd == "load":
            if not args:
                return "⚠️ 请指定对话ID"
            
            convo = self.memory.load_conversation(args)
            if not convo:
                return f"❌ 找不到对话: {args}"
            
            self._print(f"✅ 已加载对话: {convo.title}")
            self.agent = ConversationAgent(self.memory)
            return "__start_conversation__"
        
        # 删除对话
        elif cmd == "delete":
            if not args:
                return "⚠️ 请指定要删除的对话ID"
            
            if self.memory.delete_conversation(args):
                return f"🗑️ 已删除对话 {args}"
            else:
                return f"❌ 删除失败: 对话 {args} 不存在"
        
        # 未知命令
        return None

    def run(self):
        self._print_banner()

        while self.running:
            try:
                user_input = self.input_queue.get().strip()  # 阻塞直到有输入
                # user_input = input("\n> ").strip()
                if not user_input:
                    continue
                
                # 解析命令
                cmd, args = self._parse_command(user_input)
                
                # 处理命令
                cmd_result = self._handle_command(cmd, args)
                if cmd_result == "__start_conversation__":
                    while self.running:
                        # msg = input("\n你: ").strip()
                        msg = self.input_queue.get().strip()
                        if not msg:
                            continue
                        if msg.lower() in ("quit", "exit"):
                            self._print("👋 已退出对话模式。")
                            break
                        self._print("", sender="AI", end="")

                        for response in self.agent.process_input(msg):
                            self._print(response, sender="", end="")
                        self._print("", sender="")
                    continue
                elif cmd_result:
                    self._print(cmd_result)
                    continue
                
            except KeyboardInterrupt:
                self._print("\n👋 再见！")
                self.running = False
            except Exception as e:
                self._print(f"⚠️ 发生错误: {e}")

    