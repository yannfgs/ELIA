import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests

# Substitua pela sua chave de API real da OpenAI
API_KEY = 'vgBwZU9MeRPukewGxEpiT3BlbkFJ3glWxR8VEEmHt7tDtKyX'

class EliaApp:
    def __init__(self, master):
        self.master = master
        master.title("Aplicação ELIA - ChatGPT com OpenAI")

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
        prompt = self.text_message.get()
        data = {
            'model': 'gpt-3.5-turbo',  # Escolha o modelo adequado para o seu caso
            'messages': [
                {"role": "system", "content": "Você é um assistente útil."},
                {"role": "user", "content": prompt.strip()}
            ]
        }

        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            self.text_response.delete(1.0, tk.END)
            if 'choices' in response_data:
                self.text_response.insert(tk.END, response_data['choices'][0]['message']['content'])
            else:
                self.text_response.insert(tk.END, "Erro na resposta da API.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", str(e))

def main():
    root = tk.Tk()
    app = EliaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()