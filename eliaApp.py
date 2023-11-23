import tkinter as tk
from tkinter import messagebox, scrolledtext, PhotoImage, font
import requests
import threading
import time
import os
import sys

# Substitua pela sua chave de API e Organization ID reais da OpenAI
API_KEY = "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"
ORGANIZATION_ID = "org-4GGvTGan5YuCScHmLKDtIGt8"

# Função para obter o caminho correto dos recursos
def resource_path(relative_path):
    """ Get absolute path to resource, works for development and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class EliaApp:
    def __init__(self, master):
        self.master = master
        master.title("Aplicação ELIA - Inteligência Artificial da Elite Aço")

        # Define a fonte Poppins
        self.custom_font = font.Font(family="Poppins", size=10)

        # Carregar e exibir a logo
        logo_path = resource_path("img/logo_ELITEACO_150px.png")
        self.logo_image = PhotoImage(file=logo_path)
        self.logo_label = tk.Label(master, image=self.logo_image)
        self.logo_label.pack()

        # Label e entrada de texto para a mensagem do usuário
        self.label_message = tk.Label(
            master, text="Digite sua mensagem para o assistente:", font=self.custom_font
        )
        self.label_message.pack()

        self.text_message = tk.Entry(master, width=50, font=self.custom_font)
        self.text_message.pack()
        self.text_message.bind("<Return>", self.send_message)  # Bind da tecla Enter

        # Botão para enviar a mensagem
        self.button_send = tk.Button(
            master,
            text="Enviar Mensagem",
            command=lambda: self.send_message(),
            font=self.custom_font,
        )
        self.button_send.pack()

        # Área de texto com barra de rolagem para a resposta
        self.label_response = tk.Label(
            master, text="Resposta do assistente:", font=self.custom_font
        )
        self.label_response.pack()

        self.text_response = scrolledtext.ScrolledText(
            master, height=15, width=50, wrap=tk.WORD, font=self.custom_font
        )
        self.text_response.pack()

        # Histórico da conversa
        self.conversation_history = []

        # Variável para controlar a animação de espera
        self.waiting_animation_active = False

    def send_message(self, event=None):
        user_input = self.text_message.get()
        if not user_input.strip():  # Evita enviar mensagens vazias
            return
        self.text_message.delete(0, tk.END)  # Limpa o campo de entrada após enviar
        self.conversation_history.append(f"Você: {user_input}")

        # Inicia a animação de espera
        self.waiting_animation_active = True
        threading.Thread(target=self.waiting_animation, daemon=True).start()

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um assistente útil. Responda somente em Português (Brasil)",
                },
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
            assistant_response = response_data["choices"][0]["message"]["content"]
            self.conversation_history.append(f"Assistente: {assistant_response}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", str(e))
        finally:
            self.waiting_animation_active = False  # Desativa a animação de espera

            # Atualizar a área de texto com o histórico completo
            self.text_response.delete(1.0, tk.END)
            for message in self.conversation_history:
                if "Você:" in message or "Assistente:" in message:
                    self.text_response.insert(tk.END, message + "\n\n", "bold")
                else:
                    self.text_response.insert(tk.END, message + "\n\n")
            self.text_response.tag_configure(
                "bold", font=self.custom_font.copy(weight="bold")
            )

    def waiting_animation(self):
        animation_frames = [".", "..", "..."]
        i = 0
        while self.waiting_animation_active:
            if not self.waiting_animation_active:
                break
            frame = animation_frames[i % len(animation_frames)]
            self.label_response.config(text=f"Resposta do assistente{frame}")
            i += 1
            time.sleep(0.5)  # Pausa entre as animações

        # Limpa o texto quando a animação de espera termina
        if not self.waiting_animation_active:
            self.label_response.config(text="Resposta do assistente:")


def main():
    root = tk.Tk()
    app = EliaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
