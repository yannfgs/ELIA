import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit
)
from PyQt6.QtGui import QPixmap, QIcon, QFont
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
        assistant_response = self.query_openai_api(self.user_input)
        self.finished.emit(assistant_response)

    def query_openai_api(self, user_input):
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": user_input},
            ],
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "OpenAI-Organization": ORGANIZATION_ID,
        }

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions", headers=headers, json=data
            )
            response.raise_for_status()
            response_data = response.json()
            return response_data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Houve um erro ao tentar se comunicar com a API da OpenAI.\n{e}"


class EliaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicação ELIA - Inteligência Artificial da Elite Aço")
        self.setWindowIcon(QIcon("icon_path_here"))  # Substitua pelo caminho do ícone da sua aplicação

        # Setup the UI
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        self.setup_ui()

        self.central_widget.setLayout(self.layout)
        self.showMaximized()

    def setup_ui(self):
        # Logo
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap("logo_path_here")  # Substitua pelo caminho da imagem da sua logo
        self.logo_label.setPixmap(self.logo_pixmap)
        self.layout.addWidget(self.logo_label)

        # Área de texto para exibir a conversa
        self.text_conversation = QTextEdit()
        self.text_conversation.setFont(QFont("Arial", 10))
        self.text_conversation.setReadOnly(True)
        self.layout.addWidget(self.text_conversation)

        # Área para digitar a mensagem
        self.text_message = QLineEdit()
        self.text_message.setFont(QFont("Arial", 10))
        self.text_message.setPlaceholderText("Escreva sua mensagem aqui...")
        self.text_message.returnPressed.connect(self.process_input)

        # Botão de enviar
        self.send_button = QPushButton("Enviar")
        self.send_button.clicked.connect(self.process_input)

        # Layout para a área de entrada e botão
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.text_message)
        input_layout.addWidget(self.send_button)

        self.layout.addLayout(input_layout)

    def process_input(self):
        user_input = self.text_message.text().strip()
        if user_input:
            self.update_ui(f"Você: {user_input}")
            self.text_message.clear()

            self.worker = Worker(user_input)
            self.worker.finished.connect(self.update_ui)
            self.worker.start()

    def update_ui(self, message):
        self.text_conversation.append(message + "\n")


def main():
    app = QApplication(sys.argv)
    window = EliaApp()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()