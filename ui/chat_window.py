import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor

# 简化后的聊天核心功能（模拟流式输出）
def simulate_stream_response(message: str):
    """模拟流式返回的生成器"""
    words = [
        "你好！",
        "我是简单的聊天助手",
        "当前功能只展示流式对话效果",
        "输入'清空'可以重置对话",
        f"你最后说的是：{message}",
    ]
    for word in words:
        time.sleep(0.3)  # 模拟网络延迟
        yield word + " "


class ChatThread(QThread):
    """聊天线程（处理流式输出）"""
    text_received = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        try:
            for chunk in simulate_stream_response(self.message):
                self.text_received.emit(chunk)
        except Exception as e:
            print("Error:", e)
        finally:
            self.finished.emit()


class SimpleChatUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("简单聊天")
        self.setGeometry(300, 300, 500, 600)
        self.init_ui()

    def init_ui(self):
        # 主窗口
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # 聊天记录区域
        self.chat_log = QTextEdit()
        self.chat_log.setReadOnly(True)
        self.chat_log.setFont(QFont("Arial", 12))
        layout.addWidget(self.chat_log)

        # 输入区域
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("请输入消息...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        self.send_button = QPushButton("发送")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addWidget(input_widget)

        # 连接状态显示
        self.status_label = QLabel("准备就绪")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # 初始化聊天
        self.append_message("系统", "简单聊天助手已启动，开始对话吧！")

    def append_message(self, sender, message):
        """添加消息到聊天区"""
        cursor = self.chat_log.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(f"{sender}: {message}\n")
        self.chat_log.setTextCursor(cursor)

    def send_message(self):
        """发送消息"""
        message = self.input_field.text().strip()
        if not message:
            return

        if message == "清空":
            self.chat_log.clear()
            self.append_message("系统", "对话已清空")
            self.input_field.clear()
            return

        # 显示用户消息
        self.append_message("你", message)
        self.input_field.clear()
        self.status_label.setText("正在回复...")

        # 禁用输入
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)

        # 启动线程处理回复
        self.chat_thread = ChatThread(message)
        self.chat_thread.text_received.connect(lambda text: self.append_message("助手", text))
        self.chat_thread.finished.connect(self.on_reply_finished)
        self.chat_thread.start()

    def on_reply_finished(self):
        """回复完成后的处理"""
        self.status_label.setText("准备就绪")
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_field.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleChatUI()
    window.show()
    sys.exit(app.exec_())
