# First refactored code; Simple UI

import sys
import requests
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QWidget,
)
from PyQt6.QtGui import (
    QTextCursor,
    QTextCharFormat,
    QFont,
    QPixmap,
    QIcon,  # Adicionado a importação correta aqui
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize

# Substitua pela sua chave de API e Organization ID reais da OpenAI
API_KEY = "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"
ORGANIZATION_ID = "org-4GGvTGan5YuCScHmLKDtIGt8"


class Worker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input

    def run(self):
        try:
            response = self.query_openai_api(self.user_input)
            self.finished.emit(response)
        except Exception as e:
            self.finished.emit(f"Erro ao se comunicar com a API da OpenAI: {e}")

    def query_openai_api(self, user_input):
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_input}],
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "OpenAI-Organization": ORGANIZATION_ID,
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=data
        )
        response.raise_for_status()
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]


class EliaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicação ELIA - Inteligência Artificial da Elite Aço")
        self.setWindowIcon(
            QIcon("img/icon_usuario.png")
        )  # Insert the path to your app icon

        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Logo setup
        self.logo = QLabel()
        self.logo_pixmap = QPixmap(
            "img/logo_ELITEACO_500px.png"
        )  # Insert the path to your logo image
        self.logo.setPixmap(
            self.logo_pixmap.scaled(QSize(400, 100), Qt.AspectRatioMode.KeepAspectRatio)
        )
        self.layout.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Text area for conversation history
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet(
            "QTextEdit { padding: 10px; }"
        )  # Add internal padding
        self.layout.addWidget(self.chat_history)

        # Input area setup
        self.input_area = QLineEdit()
        self.input_area.returnPressed.connect(
            self.send_message
        )  # Envia a mensagem ao pressionar Enter
        self.layout.addWidget(self.input_area)
        self.send_button = QPushButton("Enviar")
        self.layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_message)

        # Processing Label
        self.processing_label = QLabel()
        self.layout.addWidget(self.processing_label)

        # Window central widget setup
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def send_message(self):
        user_message = self.input_area.text()
        if user_message:
            self.append_message_to_chat("Você", user_message)
            self.input_area.clear()
            self.processing_label.setText("Processando...")
            self.worker = Worker(user_message)
            self.worker.finished.connect(self.handle_response)
            self.worker.start()

    def handle_response(self, message):
        self.processing_label.clear()
        self.append_message_to_chat("Assistente", message)

    def append_message_to_chat(self, sender, message):
        if sender == "Assistente":
            self.processing_label.clear()  # Clear processing text when we receive the response
        self.chat_history.moveCursor(QTextCursor.MoveOperation.End)

        # Apply bold format to sender's name
        char_format = QTextCharFormat()
        char_format.setFontWeight(QFont.Weight.Bold)
        self.chat_history.setCurrentCharFormat(char_format)
        self.chat_history.insertPlainText(f"{sender}:\n")

        # Apply normal format to message
        char_format.setFontWeight(QFont.Weight.Normal)
        self.chat_history.setCurrentCharFormat(char_format)
        self.chat_history.insertPlainText(f"{message}\n\n")

        self.chat_history.ensureCursorVisible()


# Run the app
def main():
    app = QApplication(sys.argv)
    elia_app = EliaApp()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
