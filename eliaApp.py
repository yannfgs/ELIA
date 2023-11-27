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
    """Get absolute path to resource, works for development and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class EliaApp:
    def __init__(self, master):
        self.master = master
        master.title("Aplicação ELIA - Inteligência Artificial da Elite Aço")
        master.state("zoomed")

        # Define a fonte Poppins
        self.custom_font = font.Font(family="Poppins", size=11)
        self.bold_font = font.Font(family="Poppins", size=11, weight="bold")

        # Carregar e exibir a logo
        logo_path = resource_path("img/logo_ELITEACO_500px.png")
        self.logo_image = PhotoImage(file=logo_path)
        self.logo_label = tk.Label(master, image=self.logo_image)
        self.logo_label.pack()

        # Carregar ícones para o usuário e o assistente
        self.user_icon = PhotoImage(file=resource_path("img\icon_usuario.png"))
        self.assistant_icon = PhotoImage(file=resource_path("img\icon_assistente.png"))

        # Configurar o layout da aplicação
        self.setup_layout(master)

        # Histórico da conversa
        self.conversation_history = []

        # Variável para controlar a animação de espera
        self.waiting_animation_active = False
        self.waiting_animation_label = tk.Label(master, text="", font=self.custom_font)
        self.waiting_animation_label.pack()

    def setup_layout(self, master):
        # Frame para área de resposta
        response_frame = tk.Frame(master)
        response_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Área de texto com barra de rolagem para a resposta
        self.text_response = scrolledtext.ScrolledText(
            response_frame,
            wrap=tk.WORD,
            font=self.custom_font,
            state="disabled",
            padx=10,
            pady=10,
        )
        self.text_response.pack(expand=True, fill="both")

        # Frame para área de entrada
        input_frame = tk.Frame(master)
        input_frame.pack(fill="x", padx=10, pady=10)

        # Área de entrada de texto com barra de rolagem
        self.text_message = tk.Text(
            input_frame, height=3, font=self.custom_font, padx=10, pady=10
        )  # Margens internas ajustadas
        self.text_message.pack(side="left", fill="x", expand=True)
        self.text_message.bind("<Return>", self.send_message)

        # Placeholder para a área de entrada de texto
        self.placeholder_text = "Escreva sua mensagem aqui"
        self.text_message.insert("1.0", self.placeholder_text)
        self.text_message.bind("<FocusIn>", self.clear_placeholder)
        self.text_message.bind("<FocusOut>", self.add_placeholder)
        self.text_message.config(fg="grey")

        # Botão para enviar a mensagem
        self.button_send = tk.Button(
            input_frame, text="Enviar", command=self.send_message, font=self.custom_font
        )
        self.button_send.pack(side="left", padx=10)

    def clear_placeholder(self, event=None):
        """Limpa o texto de placeholder quando a caixa de texto é focada."""
        current_text = self.text_message.get("1.0", tk.END)
        if current_text.strip() == self.placeholder_text:
            self.text_message.delete("1.0", tk.END)
            self.text_message.config(fg="black")

    def add_placeholder(self, event=None):
        """Adiciona o texto de placeholder se a caixa de texto estiver vazia quando desfocada."""
        if not self.text_message.get("1.0", tk.END).strip():
            self.text_message.insert("1.0", self.placeholder_text)
            self.text_message.config(fg="grey")

    def send_message(self, event=None):
        user_input = self.text_message.get("1.0", tk.END).strip()
        if (
            user_input and not user_input.isspace()
        ):  # Verifica se a entrada não é apenas espaço em branco
            self.append_to_chat(
                user_input, "Você"
            )  # Adiciona a mensagem do usuário ao histórico
            self.initiate_waiting_animation()
            threading.Thread(
                target=self.query_openai_api, args=(user_input,), daemon=True
            ).start()

            self.text_message.delete(
                "1.0", tk.END
            )  # Limpa o campo de entrada após enviar
            self.text_message.insert(
                "1.0", ""
            )  # Insere uma string vazia para manter o cursor na primeira linha
            self.text_message.mark_set(
                tk.INSERT, "1.0"
            )  # Reposiciona o cursor na primeira linha
            self.text_message.see(
                tk.INSERT
            )  # Garante que a visão esteja focada no cursor
            self.text_message.focus_set()  # Foca na área de texto de entrada

        # Se a função foi chamada por um evento de tecla, impede a inserção de nova linha
        if event:
            return "break"

    def append_to_chat(self, message, sender):
        self.text_response.config(state="normal")
        # Determinar qual ícone usar baseado no remetente da mensagem
        icon_to_use = self.user_icon if sender == "Você" else self.assistant_icon

        # Inserir o ícone no chat
        self.text_response.image_create(tk.END, image=icon_to_use)
        self.text_response.insert(tk.END, f" {sender}\n", "bold")

        # Inserir a mensagem no chat e adicionar uma linha em branco após a mensagem para espaçamento
        self.text_response.insert(tk.END, f"{message}\n\n")
        self.text_response.config(state="disabled")
        self.text_response.see(tk.END)
        self.text_response.tag_configure("bold", font=self.bold_font)
        if sender:  # Se existe um remetente, formatar e adicionar o nome em negrito
            sender_formatted = (
                f"{sender}:\n"  # Quebra de linha após o nome do remetente
            )
            self.text_response.insert(tk.END, sender_formatted, "bold")
        self.text_response.insert(
            tk.END, f"{message}\n"
        )  # Uma única quebra de linha após a mensagem
        if (
            sender
        ):  # Adiciona uma quebra de linha extra apenas se for o final de uma interação
            self.text_response.insert(tk.END, "\n")  # Espaçamento entre interações
        self.text_response.config(state="disabled")
        self.text_response.see(tk.END)
        # Configuração das tags
        self.text_response.tag_configure("bold", font=self.bold_font)

    def query_openai_api(self, user_input):
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um assistente útil. Sempre responda em Português do Brasil",
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
            response.raise_for_status()  # Vai gerar um erro se a chamada falhar
            response_data = response.json()
            assistant_response = response_data["choices"][0]["message"]["content"]
            self.master.after(
                0, self.append_to_chat, assistant_response, "ELIA - IA da Elite Aço"
            )
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", str(e))
            assistant_response = (
                "Houve um erro ao tentar se comunicar com a API da OpenAI."
            )
        finally:
            self.master.after(0, self.stop_waiting_animation)

    def initiate_waiting_animation(self):
        self.waiting_animation_active = True
        self.waiting_animation_label.config(text="Processando...")
        threading.Thread(target=self.waiting_animation, daemon=True).start()

    def stop_waiting_animation(self):
        self.waiting_animation_active = False
        self.waiting_animation_label.config(text="")

    def waiting_animation(self):
        while self.waiting_animation_active:
            time.sleep(0.5)


def main():
    root = tk.Tk()
    app = EliaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
