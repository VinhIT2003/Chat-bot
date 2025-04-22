from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QTextCursor
import sys


import os
from bardapi import Bard

# Cấu hình API Key (cần thay thế bằng API key của bạn)
os.environ['_BARD_API_KEY'] = "AIzaSyB671PCzDywRaGgwwqH4GggGISouIzr0b8"

# Khởi tạo Bard
bard = Bard()



class ChatBotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chatbot - Giao diện ChatGPT")
        self.setGeometry(100, 100, 900, 500)

        # Bố cục chính (Gồm sidebar và khung chat)
        main_layout = QHBoxLayout(self)

        # 📌 Sidebar (Danh sách hội thoại)
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("""
            background-color: #f0f0f0;
            font-size: 14px;
            border-right: 2px solid #ccc;
        """)
        self.sidebar.itemClicked.connect(self.load_conversation)
        main_layout.addWidget(self.sidebar)

        # 📌 Layout khung chat (bên phải)
        chat_layout = QVBoxLayout()

        # 🔵 Tiêu đề Chat
        self.title = QLabel("ChatGPT")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 5px;")
        chat_layout.addWidget(self.title)

        # 📌 Khung hiển thị tin nhắn
        self.chat_display = QTextBrowser()
        self.chat_display.setStyleSheet("""
            font-size: 14px;
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
        """)
        chat_layout.addWidget(self.chat_display)

        # 📌 Ô nhập tin nhắn
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Nhập tin nhắn...")
        self.user_input.setStyleSheet("""
            font-size: 14px;
            padding: 8px;
            border-radius: 5px;
            border: 1px solid #ccc;
        """)
        self.user_input.returnPressed.connect(self.send_message)
        chat_layout.addWidget(self.user_input)

        # 📌 Hàng nút bấm (Gửi & Làm mới)
        button_layout = QHBoxLayout()

        # ✅ Nút gửi tin nhắn
        send_button = QPushButton("Gửi")
        send_button.setStyleSheet("""
            background-color: #0078D7;
            color: white;
            font-size: 14px;
            padding: 8px;
            border-radius: 5px;
        """)
        send_button.clicked.connect(self.send_message)
        button_layout.addWidget(send_button)

        # ✅ Nút làm mới
        refresh_button = QPushButton("Làm mới")
        refresh_button.setStyleSheet("""
            background-color: #FF5733;
            color: white;
            font-size: 14px;
            padding: 8px;
            border-radius: 5px;
        """)
        refresh_button.clicked.connect(self.new_conversation)
        button_layout.addWidget(refresh_button)

        chat_layout.addLayout(button_layout)
        main_layout.addLayout(chat_layout)
        self.setLayout(main_layout)

        # 📝 Danh sách lịch sử trò chuyện
        self.conversations = {}
        self.current_chat_id = None

    def send_message(self):
        user_text = self.user_input.text().strip()
        if user_text:
            if self.current_chat_id is None:
                self.current_chat_id = f"Cuộc trò chuyện {len(self.conversations) + 1}"
                self.sidebar.addItem(self.current_chat_id)
                self.conversations[self.current_chat_id] = []

            self.append_message(f"<b style='color:blue'>Bạn:</b> {user_text}")
            bot_reply = self.get_bot_response(user_text)
            self.append_message(f"<b style='color:green'>Bot:</b> {bot_reply}")

            # Lưu tin nhắn vào lịch sử hội thoại
            self.conversations[self.current_chat_id].append((user_text, bot_reply))
            self.user_input.clear()

    def get_bot_response(self, message):
        message = message.strip()
    
        try:
            # Gửi câu hỏi đến Bard
            response = bard.get_answer(message)
            
            # Kiểm tra phản hồi từ Bard
            if 'content' in response:
                return response['content']
            else:
                return "🤖 Xin lỗi, tôi chưa có câu trả lời cho câu hỏi này!"
        
        except Exception as e:
            return f"⚠️ Có lỗi xảy ra: {e}"
    
    
    def append_message(self, message):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertHtml(message + "<br><br>")
        self.chat_display.setTextCursor(cursor)
        self.chat_display.ensureCursorVisible()

    def load_conversation(self, item):
        self.current_chat_id = item.text()
        self.chat_display.clear()
        for user_text, bot_reply in self.conversations[self.current_chat_id]:
            self.append_message(f"<b style='color:blue'>Bạn:</b> {user_text}")
            self.append_message(f"<b style='color:green'>Bot:</b> {bot_reply}")

    def new_conversation(self):
        """Làm mới hội thoại, xóa nội dung hiện tại và tạo cuộc trò chuyện mới."""
        self.chat_display.clear()
        self.current_chat_id = f"Cuộc trò chuyện {len(self.conversations) + 1}"
        self.sidebar.addItem(self.current_chat_id)
        self.conversations[self.current_chat_id] = []

# Chạy ứng dụng
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatBotApp()
    window.show()
    sys.exit(app.exec_())