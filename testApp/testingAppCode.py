import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QWidget, QHBoxLayout
)
from PyQt6.QtGui import (
    QFont, QPixmap, QIcon, QMovie, QTextCursor  # Aqui foi adicionado QTextCursor
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
        self.setWindowIcon(QIcon("img/icon_usuario.png"))  # Verifique o caminho do ícone

        # Inicializar os atributos que serão usados em outros métodos
        self.chat_history = QTextEdit()
        self.processing_label = QLabel()
        self.input_area = QLineEdit()
        self.send_button = QPushButton("Enviar")
        self.current_worker = None  # Inicializa um atributo para armazenar o worker atual

        # Carregar ícones
        self.user_icon = QPixmap("img/icon_usuario.png")  # Verifique o caminho do ícone
        self.assistant_icon = QPixmap("img/icon_assistente.png")  # Verifique o caminho do ícone

        self.init_ui()

        # Define o tamanho e posição iniciais da janela
        self.setGeometry(300, 300, 800, 600)

    def init_ui(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            QLabel, QPushButton {
                font-family: 'Arial';
                font-size: 15px;
            }
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #D3D3D3;
                font-size: 15px;
                padding: 10px;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 10px;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #005FA3;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #D3D3D3;
                border-radius: 5px;
            }
        """)
        
        # Configuração do layout principal
        self.layout = QVBoxLayout()

        # Configuração da logo
        self.logo = QLabel()
        self.logo_pixmap = QPixmap("img/logo_ELITEACO_500px.png")  # Verifique o caminho da imagem
        self.logo.setPixmap(self.logo_pixmap.scaled(QSize(400, 100), Qt.AspectRatioMode.KeepAspectRatio))
        self.layout.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Configuração da área de histórico de conversas
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("QTextEdit { padding: 10px; }")  # Adicionar padding interno
        self.chat_history.setFont(QFont("Arial", 12))  # Configurar o tamanho da fonte
        self.layout.addWidget(self.chat_history)

        # Mensagem de boas-vindas
        self.append_message_to_chat("Assistente", "Olá, bem-vindo(a) ao atendimento da Elite Aço! Como posso ajudar?")

        # Configuração da área de entrada de texto
        self.input_area.returnPressed.connect(self.send_message)
        self.layout.addWidget(self.input_area)

        # Configuração do botão de envio
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        # Configuração do label de processamento
        self.layout.addWidget(self.processing_label)

        # Configuração do widget central da janela
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        
        # Definição de layout para área de entrada e botão de envio
        input_layout = QHBoxLayout()
        self.input_area.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_area)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        # Integração do novo layout na interface
        self.layout.addLayout(input_layout)

        # Adicione o layout de entrada ao layout principal
        self.layout.addLayout(input_layout)

        # GIF de carregamento para feedback visual durante a chamada da API
        self.loading_movie = QMovie("path/to/loading.gif")
        self.processing_label.setMovie(self.loading_movie)
        self.layout.addWidget(self.processing_label)

    def send_message(self):
        user_message = self.input_area.text()
        if user_message:
            self.append_message_to_chat("Você", user_message)
            self.input_area.clear()
            self.processing_label.movie().start()
            self.processing_label.setText("Processando...")
            self.worker = Worker(user_message)
            self.worker.finished.connect(self.handle_response)  # Conexão correta
            self.worker.start()
            self.loading_movie.start()
            # Iniciar um novo Worker a cada mensagem enviada
            self.start_worker(user_message)
            
    def start_worker(self, user_input):
        if self.current_worker is not None:
            # Desconecta o sinal finished do worker anterior (se houver)
            self.current_worker.finished.disconnect()
            self.current_worker = Worker(user_input)
            self.current_worker.finished.connect(self.handle_response)
            self.current_worker.start()

    def handle_response(self, message):
        # Parar o GIF de carregamento e limpar a label uma única vez
        self.loading_movie.stop()
        self.processing_label.clear()
        self.append_message_to_chat("Assistente", message)
        # Importante: desvincular o slot do sinal depois de processar a resposta para evitar chamadas múltiplas
        self.current_worker.finished.disconnect()

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


# Rodar a aplicação
def main():
    app = QApplication(sys.argv)
    elia_app = EliaApp()
    elia_app.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()