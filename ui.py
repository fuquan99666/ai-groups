import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTextEdit, QLineEdit, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QTextCursor
import markdown

class ChatUI(QMainWindow):
    message_sent = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 设置窗口标题和尺寸
        self.setWindowTitle('AI聊天助手')
        self.setGeometry(300, 300, 800, 600)
        
        # 创建主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 创建聊天显示区域（支持滚动）
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setLineWrapMode(QTextEdit.WidgetWidth)
        self.chat_display.setFont(QFont("SimHei", 10))
        main_layout.addWidget(self.chat_display)
        
        # 创建输入区域
        input_layout = QHBoxLayout()
        
        self.message_input = QLineEdit()
        self.message_input.setFont(QFont("SimHei", 10))
        self.message_input.setPlaceholderText("输入消息，按Enter发送")
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input, 7)
        
        self.send_button = QPushButton("发送")
        self.send_button.setFont(QFont("SimHei", 10))
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button, 1)
        
        main_layout.addLayout(input_layout)
        
        # 初始化消息历史
        self.init_messages()
        
    def init_messages(self):
        # 显示欢迎消息
        self.display_message("系统", "聊天助手已启动，输入 `exit` 退出\n")
        
    def display_message(self, sender, message):
        """在聊天窗口中显示消息"""
        cursor = self.chat_display.textCursor()
        
        # 将Markdown转换为HTML
        html_message = markdown.markdown(message)
        
        if sender == "系统":
            self.chat_display.append(f"<b><font color='#888888'>🤖:</font></b> {html_message}")
        elif sender == "你":
            # 用户消息直接追加，不做特殊处理
            self.chat_display.append(f"<b><font color='#008000'>你:</font></b> {html_message}")
        else:
            # 只对AI回复使用打字机效果
            if "🤖:" in self.chat_display.toPlainText():
                # 找到最后一条AI回复并替换
                cursor.movePosition(QTextCursor.End)
                cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
                cursor.removeSelectedText()
                cursor.deletePreviousChar()  # 删除换行符
            
            # 添加更新后的AI回复
            self.chat_display.append(f"<b><font color='#0000FF'>🤖:</font></b> {html_message}")
        
        # 自动滚动到底部
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
    
    def send_message(self):
        """处理发送消息"""
        message = self.message_input.text().strip()
        if message:
            # 显示用户消息
            self.chat_display.append(f"<b><font color='#008000'>你:</font></b> {message}")
            self.display_message("你", message)
            
            # 清空输入框
            self.message_input.clear()

            # 发送消息信号
            self.message_sent.emit(message)
            # # 模拟AI回复（实际应用中这里应该调用你的AI接口）
            # if message.lower() == "exit":
            #     self.display_message("🤖", "再见！")
            #     # 实际应用中可以在这里添加退出逻辑
            # else:
            #     # 模拟AI生成回复
            #     self.display_message("AI", f"你发送了: {message}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置全局字体，确保中文正常显示
    font = QFont("SimHei")
    app.setFont(font)
    chat_ui = ChatUI()
    chat_ui.show()
    sys.exit(app.exec_())  
