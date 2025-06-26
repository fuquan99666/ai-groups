import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                            QFrame, QScrollBar)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import (QFont, QTextCursor, QTextCharFormat, QTextFormat, 
                        QColor, QLinearGradient, QPalette, QPainter, 
                        QBrush, QPainterPath)
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionFrame

class RoundedTextEdit(QTextEdit):
    """自定义圆角文本编辑框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.NoFrame)
        
    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 创建圆角路径
        path = QPainterPath()
        path.addRoundedRect(self.viewport().rect(), 10, 10)
        
        # 设置背景渐变
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0, QColor(240, 240, 245))
        grad.setColorAt(1, QColor(255, 255, 255))
        
        painter.fillPath(path, grad)
        painter.setPen(QColor(200, 200, 210))
        painter.drawPath(path)
        
        super().paintEvent(event)

class ModernLineEdit(QLineEdit):
    """现代风格的输入框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #d1d5db;
                border-radius: 12px;
                padding: 8px 12px;
                background: white;
                font-size: 18px;
                selection-background-color: #60a5fa;
            }
            QLineEdit:focus {
                border-color: #60a5fa;
            }
        """)

class GradientButton(QPushButton):
    """渐变色按钮"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:0.5 #6366f1, stop:1 #8b5cf6);
                color: white;
                border-radius: 12px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:0.5 #4f46e5, stop:1 #7c3aed);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1d4ed8, stop:0.5 #4338ca, stop:1 #6d28d9);
            }
        """)

class ChatUI(QMainWindow):
    message_sent = pyqtSignal(str)
    append_output_signal = pyqtSignal(str, str, str)  # text, sender, end
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.append_output_signal.connect(self.append_output)

    def initUI(self):
        # 设置窗口属性
        self.setWindowTitle('AI聊天助手')
        self.setGeometry(200, 100, 1100, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f9fafb;
            }
        """)
        
        # 主部件和布局
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #f9fafb;")
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # 聊天显示区域
        chat_frame = QFrame()
        chat_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            }
        """)
        chat_layout = QVBoxLayout(chat_frame)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        
        self.chat_display = QTextEdit()
        self.chat_display.setMarkdown("")
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                border: none;
                border-radius: 12px;
                padding: 16px;
                font-family: "PingFang SC", "Microsoft YaHei";
                font-size: 20px;
                color: #374151;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f5f9;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #d1d5db;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        self.chat_display.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # 设置聊天泡泡样式
        self.initMessageStyles()
        
        chat_layout.addWidget(self.chat_display)
        main_layout.addWidget(chat_frame, 1)
        
        # 输入区域
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
                padding: 8px;
            }
        """)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(4, 4, 4, 4)
        input_layout.setSpacing(10)
        
        self.message_input = ModernLineEdit()
        self.message_input.setPlaceholderText("输入消息...")
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input, 5)
        
        self.send_button = GradientButton("发送")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button, 1)
        
        main_layout.addWidget(input_frame)
        
    def initMessageStyles(self):
        """初始化消息样式"""
        # 系统消息样式
        system_format = QTextCharFormat()
        system_format.setForeground(QColor("#6b7280"))
        system_format.setFontWeight(QFont.Medium)
        self.chat_display.document().setDefaultStyleSheet("""
            .system-message {
                color: #6b7280;
                font-weight: 500;
                margin-bottom: 8px;
            }
            .user-message {
                color: #111827;
                font-weight: 500;
                background-color: #e0e7ff;
                border-radius: 12px;
                padding: 8px 12px;
                margin: 4px 60px 4px 4px;
                border: 1px solid #dbeafe;
                display: inline-block;
            }
            .ai-message {
                color: #111827;
                font-weight: 500;
                background-color: #f3f4f6;
                border-radius: 12px;
                padding: 8px 12px;
                margin: 4px 4px 4px 60px;
                border: 1px solid #e5e7eb;
                display: inline-block;
            }
        """)
        
    def send_message(self):
        """处理发送消息"""
        message = self.message_input.text().strip()
        if message:
            self.append_output(message, "你")
            self.message_input.clear()
            self.message_sent.emit(message)

    def append_output(self, text: str, sender: str = "系统", end: str = "\n"):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # 只有 end == '\n' 时才加发送者标签
        if sender == "系统":
            cursor.insertHtml(f"<b><font color='#888888'>[系统]:</font></b> ")
        elif sender == "AI":
            cursor.insertHtml(f"<b><font color='#0000FF'>[AI]:</font></b> ")
        else:
            if sender != "":
                cursor.insertHtml(f"<b><font color='#008000'>[{sender}]:</b> ")
        cursor.insertText(text + end)

        self.chat_display.ensureCursorVisible()
        
        # 自动滚动到底部（优化版）
        scroll_bar = self.chat_display.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())
        QApplication.processEvents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置全局字体
    font = QFont("PingFang SC", 10)
    app.setFont(font)
    chat_ui = ChatUI()
    chat_ui.show()
    sys.exit(app.exec_())
