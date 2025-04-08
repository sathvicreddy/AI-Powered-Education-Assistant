import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
import threading

# Replace with your actual API key
API_KEY = "AIzaSyBb6wQPHvcuvN4wQd_sRGGxp1yqhb59qhA"
MODEL_NAME = "gemini-1.5-flash"

INSTRUCTIONS = """You are an AI-powered personalized education assistant. ... (rest of the instructions)"""

# Configure Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name=MODEL_NAME)

class ChatbotUI:
    def __init__(self, master):
        self.master = master
        master.title("AI Education Assistant")
        master.geometry("600x600")
        master.configure(bg="#1e1e1e")

        self.chat_history = []

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            master,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#2e2e2e",
            fg="white",
            insertbackground="white",
            font=("Consolas", 11),
            borderwidth=0
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # User input area
        self.user_input_frame = tk.Frame(master, bg="#1e1e1e")
        self.user_input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.user_entry = tk.Entry(
            self.user_input_frame,
            bg="#2e2e2e",
            fg="white",
            insertbackground="white",
            font=("Consolas", 11),
            borderwidth=1,
            relief="flat"
        )
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.user_input_frame,
            text="Send",
            command=self.send_message,
            bg="#007acc",
            fg="white",
            font=("Consolas", 10, "bold"),
            activebackground="#005f99",
            relief="flat",
            padx=10,
            pady=2
        )
        self.send_button.pack(side=tk.RIGHT)

        # Initial messages
        self.display_message("AI Assistant", "Hello! How can I help you learn today?")
        self.chat_history.append({"role": "user", "parts": [f"You are a helpful AI education assistant. {INSTRUCTIONS}"]})
        self.chat_history.append({"role": "model", "parts": ["Understood. How can I help you today?"]})

    def display_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

    def send_message(self, event=None):
        user_query = self.user_entry.get().strip()
        if not user_query:
            return
        self.user_entry.delete(0, tk.END)

        if user_query.lower() in ["quit", "exit", "bye"]:
            self.display_message("You", user_query)
            self.display_message("AI Assistant", "Goodbye and happy learning!")
            self.master.destroy()
            return

        self.display_message("You", user_query)
        self.get_ai_response(user_query)

    def get_ai_response(self, user_input):
        self.user_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        threading.Thread(target=self._get_and_display_response, args=(user_input,)).start()

    def _get_and_display_response(self, user_input):
        try:
            generation_config = {
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 50,
                "max_output_tokens": 512,
            }
            convo = model.start_chat(history=self.chat_history)
            response = convo.send_message(user_input)
            ai_response = response.text
            self.chat_history.append({"role": "user", "parts": [user_input]})
            self.chat_history.append({"role": "model", "parts": [ai_response]})
            self.display_message("AI Assistant", ai_response)
        except Exception as e:
            self.display_message("Error", f"An error occurred: {e}")
        finally:
            self.user_entry.config(state=tk.NORMAL)
            self.send_button.config(state=tk.NORMAL)
            self.user_entry.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_ui = ChatbotUI(root)
    root.mainloop()
