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
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um assistente útil. Responda sempre em Português (Brasil).",
                },
                {"role": "user", "content": user_input},
            ],
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

        # Carregar ícones
        self.user_icon = QPixmap("img/icon_usuario.png")
        self.assistant_icon = QPixmap("img/icon_assistente.png")

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

        # Defina o tamanho da fonte para algo maior, por exemplo, 12 ou 14
        self.chat_history.setFont(QFont("Arial", 12))

        # Mensagem de boas-vindas
        self.append_message_to_chat("Assistente", "Olá, bem-vindo(a) ao atendimento da Elite Aço! Como posso ajudar?")
        
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
        
# Defina o tamanho inicial da janela para ser menor que o máximo
        self.setGeometry(300, 300, 800, 600)  # Ajuste as dimensões conforme necessário
        
    def send_message(self):
        user_message = self.input_area.text()
        if user_message:
            self.append_message_to_chat("Você", user_message)
            self.input_area.clear()
            self.processing_label.setText("Processando...")
            self.worker = Worker(user_message)
            self.worker.finished.connect(self.handle_response)  # Conexão correta
            self.worker.start()

    def handle_response(self, message):
        self.processing_label.clear()
        self.append_message_to_chat("Assistente", message)

    def append_message_to_chat(self, sender, message):
        self.chat_history.moveCursor(QTextCursor.MoveOperation.End)
        icon_path = (
            "img/icon_usuario.png" if sender == "Você" else "img/icon_assistente.png"
        )
        self.chat_history.insertHtml(
            f"<img src='{icon_path}' width='15' height='15'> <b>{sender}:</b><br>"
        )
        self.chat_history.insertPlainText(f"{message}\n\n")
        self.chat_history.ensureCursorVisible()


# Run the app
def main():
    app = QApplication(sys.argv)
    elia_app = EliaApp()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
