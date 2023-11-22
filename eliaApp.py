# APLICAÇÃO ELITA - INTELIGÊNCIA ARTIFICIAL DA ELITE AÇO - API CHATGPT

import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests

# Substitua pela sua chave de API e Organization ID reais da OpenAI
API_KEY = "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"
ORGANIZATION_ID = "org-4GGvTGan5YuCScHmLKDtIGt8"


class EliaApp:
    def __init__(self, master):
        self.master = master
        master.title("Aplicação ELIA - ChatGPT Personalizado")

        # Label e entrada de texto para a mensagem do usuário
        self.label_message = tk.Label(master, text="Digite sua mensagem para a ELIA:")
        self.label_message.pack()

        self.text_message = tk.Entry(master, width=50)
        self.text_message.pack()

        # Botão para enviar a mensagem
        self.button_send = tk.Button(
            master, text="Enviar Mensagem", command=self.send_message
        )
        self.button_send.pack()

        # Área de texto com barra de rolagem para a resposta
        self.label_response = tk.Label(master, text="Resposta da ELIA:")
        self.label_response.pack()

        self.text_response = scrolledtext.ScrolledText(master, height=15, width=50)
        self.text_response.pack()

    def send_message(self):
        prompt = self.text_message.get()
        data = {"input": {"text": prompt.strip()}}

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "OpenAI-Organization": ORGANIZATION_ID,
        }

        assistant_id = (
            "asst_9ME2sTydFVlaMbHADWoI0nu9"  # ID do seu assistente personalizado
        )

        try:
            url = f"https://api.openai.com/v1/assistants/{assistant_id}/messages"
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            self.text_response.delete(1.0, tk.END)
            # Adapte a chave de acesso no JSON conforme a API do seu assistente responde.
            self.text_response.insert(tk.END, response_data["data"][0]["text"])
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", str(e))


def main():
    root = tk.Tk()
    app = EliaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
