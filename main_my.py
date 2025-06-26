import sys

from core.conversation_agent import ConversationAgent
from core.memory_manager import MemoryManager
from resources import resources
from ui.CLI import CLIInterface
from ui.chat_window import ChatUI
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setFont(QFont("SimHei"))
        
        # 初始化组件
        self.chat_ui = ChatUI()
        self.cli = CLIInterface()
        
        # 建立通信桥梁
        self._setup_connections()

    def _setup_connections(self):
        """连接信号与槽函数"""
        # CLI输出 -> ChatUI
        self.cli.set_output_callback(self.chat_ui.append_output_signal.emit)
        
        # ChatUI输入 -> CLI（通过信号）
        self.chat_ui.message_sent.connect(self.cli.receive_input)
    
    # def _handle_message_sent_command(self, message: str):
    #     """处理来自ChatUI的发送命令"""
    #     if command.lower() == "exit":
    #         self.cli._print("👋 再见！", "系统")
    #         self.app.quit()
    #     else:
    #         # 模拟CLI处理命令
    #         self.cli._handle_command(*self.cli._parse_command(command))
    
    def run(self):
        """启动应用"""
        self.chat_ui.show()
        
        # 启动CLI（在单独的线程中运行，避免阻塞GUI）
        import threading
        cli_thread = threading.Thread(target=self.cli.run, daemon=True)
        cli_thread.start()
        
        sys.exit(self.app.exec_())
if __name__ == '__main__':
    MainApp().run()
        
