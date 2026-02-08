import requests

def chat_with_ai(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)
    return response.json()["response"]

if __name__ == "__main__":
    print("Local AI Chatbot (Ollama) — type exit to quit")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        reply = chat_with_ai(user_input)
        print("Bot:", reply)
