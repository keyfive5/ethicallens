import tkinter as tk
from tkinter import scrolledtext, font
from tkinter import ttk
import os
import threading
from tkinter import messagebox
try:
    from dotenv import load_dotenv
    import openai
except ImportError:
    load_dotenv = None
    openai = None

class EthicalLensApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EthicalLens – Unbiased Moral Analysis")
        self.root.geometry("650x550")
        self.root.configure(bg="#f5f6fa")

        # Set modern font
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Segoe UI", size=11)
        self.root.option_add("*Font", self.default_font)

        # Notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # --- EthicalLens Tab ---
        self.main_frame = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.main_frame, text="EthicalLens")

        # Frame for input
        self.input_frame = tk.Frame(self.main_frame, bg="#f5f6fa")
        self.input_frame.pack(pady=(20, 10), padx=20, fill=tk.X)

        self.input_label = tk.Label(self.input_frame, text="Enter a moral dilemma:", bg="#f5f6fa", anchor="w")
        self.input_label.pack(anchor="w")

        self.input_text = tk.Text(self.input_frame, height=5, width=70, bd=2, relief="groove", font=("Segoe UI", 11))
        self.input_text.pack(pady=(5, 0), fill=tk.X)

        # Evaluate button
        self.button_frame = tk.Frame(self.main_frame, bg="#f5f6fa")
        self.button_frame.pack(pady=(5, 10))
        self.evaluate_button = ttk.Button(self.button_frame, text="Evaluate", command=self.evaluate)
        self.evaluate_button.pack()

        # Frame for output
        self.output_frame = tk.Frame(self.main_frame, bg="#f5f6fa")
        self.output_frame.pack(pady=(5, 10), padx=20, fill=tk.BOTH, expand=True)

        self.output_label = tk.Label(self.output_frame, text="Ethical Analysis:", bg="#f5f6fa", anchor="w")
        self.output_label.pack(anchor="w")

        self.output_area = scrolledtext.ScrolledText(
            self.output_frame, height=15, width=70, state='disabled', wrap=tk.WORD,
            font=("Segoe UI", 11), bd=2, relief="groove", bg="#f8f9fa"
        )
        self.output_area.pack(pady=(5, 0), fill=tk.BOTH, expand=True)

        # Copy All Analyses button
        self.copy_button = ttk.Button(self.output_frame, text="Copy All Analyses", command=self.copy_output)
        self.copy_button.pack(pady=(8, 0), anchor="e")
        self.copy_button.config(state='disabled')

        # --- Updates Tab ---
        self.updates_frame = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.updates_frame, text="Updates")

        self.updates_label = tk.Label(self.updates_frame, text="Project Updates", bg="#f5f6fa", font=("Segoe UI", 13, "bold"))
        self.updates_label.pack(pady=(20, 5), anchor="w", padx=20)

        self.updates_text = scrolledtext.ScrolledText(
            self.updates_frame, height=20, width=70, state='normal', wrap=tk.WORD,
            font=("Segoe UI", 11), bd=2, relief="groove", bg="#f8f9fa"
        )
        self.updates_text.pack(padx=20, pady=(0, 20), fill=tk.BOTH, expand=True)
        self.updates_text.insert(tk.END, "June 17, 2025\n-------------------\n- Created initial Tkinter GUI skeleton for EthicalLens.\n- Added input box, Evaluate button, and scrollable output area.\n- Improved aesthetics: modern font, padding, and color scheme.\n- Scaffolded backend logic for ethical lens analysis.\n- Added this Updates tab to track project progress.\n")
        self.updates_text.config(state='disabled')

        if load_dotenv:
            load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if openai and self.api_key:
            openai.api_key = self.api_key

    def evaluate(self):
        dilemma = self.input_text.get("1.0", tk.END).strip()
        if not dilemma:
            self.display_output("Please enter a moral dilemma above.")
            return
        if not openai or not self.api_key:
            self.display_output("OpenAI API or dotenv not installed, or API key missing. Please install requirements and set your API key in a .env file.")
            return
        self.display_output("Evaluating... Please wait.")
        threading.Thread(target=self.fetch_analyses, args=(dilemma,), daemon=True).start()

    def fetch_analyses(self, dilemma):
        lenses = [
            ("Utilitarianism", "You are a moral philosopher evaluating the following situation from a Utilitarian perspective. Provide a short, unbiased analysis without judgment."),
            ("Deontology", "You are a moral philosopher evaluating the following situation from a Deontological perspective. Provide a short, unbiased analysis without judgment."),
            ("Virtue Ethics", "You are a moral philosopher evaluating the following situation from a Virtue Ethics perspective. Provide a short, unbiased analysis without judgment."),
            ("Islamic Ethics", "You are a moral philosopher evaluating the following situation from an Islamic Ethics perspective. Provide a short, unbiased analysis without judgment.")
        ]
        output = ""
        try:
            for lens, prompt in lenses:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": dilemma}
                    ],
                    max_tokens=120,
                    temperature=0.2
                )
                analysis = response.choices[0].message.content.strip()
                output += f"{lens}: {analysis}\n\n"
            output += "This is a neutral, comparative ethical reflection. No synthesis is made."
        except Exception as e:
            output = f"Error: {str(e)}"
        self.display_output(output)

    def display_output(self, text):
        self.output_area.config(state='normal')
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, text)
        self.output_area.config(state='disabled')
        # Enable copy button if there is output
        if text.strip():
            self.copy_button.config(state='normal')
        else:
            self.copy_button.config(state='disabled')

    def copy_output(self):
        output = self.output_area.get(1.0, tk.END).strip()
        if output:
            self.root.clipboard_clear()
            self.root.clipboard_append(output)
            self.root.update()  # Keeps clipboard after app closes

if __name__ == "__main__":
    root = tk.Tk()
    app = EthicalLensApp(root)
    root.mainloop() 