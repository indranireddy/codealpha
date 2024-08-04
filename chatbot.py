import tkinter as tk
from tkinter import scrolledtext
from nltk.chat.util import Chat, reflections
import datetime

# Define pairs of patterns and responses.
pairs = [
    [
        r"hi|hello|hey|hola|hello",
        ["Hello!", "Hi there!", "Hi!"]
    ],
    [
        r"what can you do?|help|options",
        ["I can chat with you and answer basic questions! Ask me something else!", "I can help you with general queries. Try asking something!"]
    ],
    [
        r"how are you?|how do you do?",
        ["I'm fine, thanks! How can I help you today?", "I'm doing well. How about you?"]
    ],
     [
        r"What is python?",
        ["Python is a high-level, interpreted programming language known for its clear syntax and readability. It was created by Guido van Rossum and first released in 1991. Python is designed to be easy to understand and fun to use (the name comes from Monty Python so a lot of its beginner tutorials reference it with playfulness)."]
    ],
    [
        r".*",
        ["I'm not sure I understand. Can you rephrase that?", "Interesting... Tell me more!", "I'm here to help!"]
    ]
]

chatbot = Chat(pairs, reflections)

def send(event=None):  # Allow for pressing "Enter" key
    user_input = user_entry.get()
    if not user_input.strip():
        return
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_entry.delete(0, tk.END)
    chat_area.configure(state='normal')
    chat_area.insert(tk.END, f"{timestamp} - You: {user_input}\n", 'user')
    response = chatbot.respond(user_input)
    if response is None:
        response = "Sorry, I don't understand that. Could you try asking something else?"
    chat_area.insert(tk.END, f"{timestamp} - Bot: {response}\n\n", 'bot')
    chat_area.configure(state='disabled')
    chat_area.yview(tk.END)

def clear_chat():
    chat_area.configure(state='normal')
    chat_area.delete('1.0', tk.END)
    chat_area.configure(state='disabled')

# Create the main window
root = tk.Tk()
root.title("Chatbot")
root.geometry("400x500")

# Set custom font and color tags
custom_font = ('Arial', 12)
chat_area = scrolledtext.ScrolledText(root, font=custom_font, wrap=tk.WORD, height=20, width=50, state='disabled')
chat_area.pack(padx=10, pady=10)
chat_area.tag_config('user', foreground='blue')
chat_area.tag_config('bot', foreground='green')

# Create a frame for user input
input_frame = tk.Frame(root)
user_entry = tk.Entry(input_frame, font=custom_font, width=30)
user_entry.bind("<Return>", send)
send_button = tk.Button(input_frame, text="Send", font=custom_font, command=send)
clear_button = tk.Button(input_frame, text="Clear", font=custom_font, command=clear_chat)

user_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
send_button.pack(side=tk.RIGHT, padx=(5, 10))
clear_button.pack(side=tk.RIGHT)
input_frame.pack(fill=tk.BOTH, padx=10, pady=5)

# Start the GUI event loop
root.mainloop()
