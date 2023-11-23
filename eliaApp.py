import tkinter as tk
from tkinter import messagebox, scrolledtext, PhotoImage
import requests

# Substitua pela sua chave de API e Organization ID reais da OpenAI
API_KEY = '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'
ORGANIZATION_ID = 'org-4GGvTGan5YuCScHmLKDtIGt8'

class EliaApp:
    def __init__(self, master):
        self.master = master
        master.title("Aplicação ELIA - Inteligência Artificial da Elite Aço")

        # Carregar e exibir a logo
        self.logo_image = PhotoImage(file='img\logo_ELITEACO_150px.png')  # Substitua pelo caminho correto da sua logo
        self.logo_label = tk.Label(master, image=self.logo_image)
        self.logo_label.pack()

        # Label e entrada de texto para a mensagem do usuário
        self.label_message = tk.Label(master, text="Digite sua mensagem para o assistente:")
        self.label_message.pack()

        self.text_message = tk.Entry(master, width=50)
        self.text_message.pack()

        # Botão para enviar a mensagem
        self.button_send = tk.Button(master, text="Enviar Mensagem", command=self.send_message)
        self.button_send.pack()

        # Área de texto com barra de rolagem para a resposta
        self.label_response = tk.Label(master, text="Resposta do assistente:")
        self.label_response.pack()

        self.text_response = scrolledtext.ScrolledText(master, height=15, width=50)
        self.text_response.pack()

    def send_message(self):
        user_input = self.text_message.get()
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {"role": "system", "content": "Você é um assistente útil. Sempre responda na língua Portuguesa do Brasil"},
                {"role": "user", "content": user_input}
            ]
        }

        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
            'OpenAI-Organization': ORGANIZATION_ID
        }

        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            response.raise_for_status()  # Isso vai gerar uma exceção se a requisição falhar
            response_data = response.json()
            self.text_response.delete(1.0, tk.END)
            self.text_response.insert(tk.END, response_data['choices'][0]['message']['content'])
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", str(e))

def main():
    root = tk.Tk()
    app = EliaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
