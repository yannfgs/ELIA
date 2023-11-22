import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests

# Substitua 'sua_chave_api_aqui' com sua chave de API real da OpenAI
API_KEY = "vgBwZU9MeRPukewGxEpiT3BlbkFJ3glWxR8VEEmHt7tDtKyX"


class EliaApp:
    def __init__(self, master):
        self.master = master
        master.title("Aplicação ELIA - Inteligência Artificial da Elite Aço")

        # Label e área de texto para a mensagem do usuário
        self.label_message = tk.Label(master, text="Digite sua mensagem para a ELIA:")
        self.label_message.pack()

        self.text_message = tk.Entry(master, width=50)
        self.text_message.pack()

        # Botão para enviar mensagem
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
    data = {
        "inputs": prompt.strip(),
    }

    headers = {"Authorization": "Bearer " + API_KEY}

    assistant_id = "asst_9ME2sTydFVlaMbHADWoI0nu9"  # ID do seu assistente personalizado

    try:
        url = f"https://api.openai.com/v1/assistants/{assistant_id}/generate"
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Vai gerar uma exceção para respostas HTTP com erro
        response_data = response.json()

        self.text_response.delete(1.0, tk.END)  # Limpa a área de texto de resposta
        self.text_response.insert(
            tk.END, response_data["choices"][0]["message"]["content"]
        )
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", e)


def main():
    root = tk.Tk()
    app = EliaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
