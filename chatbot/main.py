import tkinter as tk
from tkinter import scrolledtext
import requests
import threading

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"

def chat_with_ai(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    return response.json()["response"]

def send_message(event=None):
    user_input = entry.get().strip()
    if not user_input:
        return

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"You: {user_input}\n\n")
    chat_box.config(state=tk.DISABLED)
    chat_box.see(tk.END)

    entry.delete(0, tk.END)

    def get_reply():
        try:
            reply = chat_with_ai(user_input)
        except Exception as e:
            reply = f"Error: {e}"

        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, f"Bot: {reply}\n\n")
        chat_box.config(state=tk.DISABLED)
        chat_box.see(tk.END)

    threading.Thread(target=get_reply, daemon=True).start()

# ---- GUI SETUP ----
root = tk.Tk()
root.title("Local AI Chatbot (Ollama)")
root.geometry("600x500")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(root, font=("Arial", 12))
entry.pack(padx=10, pady=(0, 10), fill=tk.X)
entry.bind("<Return>", send_message)

send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(pady=(0, 10))

root.mainloop()
