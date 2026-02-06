import pandas as pd
import os
import json
from datetime import datetime
from tkinter import *
from tkinter import scrolledtext, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import openai
from dotenv import load_dotenv

# Configuration
os.makedirs("generated_code", exist_ok=True)
# Ensure your API key is set in your environment variables or paste it here
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY5"))

class DataAgentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nexus Data Agent")
        self.root.geometry("900x700")
        self.df = None
        self.file_path = None

        # --- UI Setup ---
        # Fixed the 'dashed' error here by using 'ridge'
        self.drop_label = Label(root, text="Drag & Drop CSV Here", bg="#f1f5f9", 
                               fg="#64748b", height=5, relief="ridge", bd=2)
        self.drop_label.pack(fill=X, padx=20, pady=20)
        
        # Register for Drag and Drop
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.handle_drop)

        self.stats_area = scrolledtext.ScrolledText(root, height=8, bg="#ffffff", font=("Consolas", 10))
        self.stats_area.pack(fill=X, padx=20, pady=5)
        self.stats_area.insert(END, "Data Summary will appear here after uploading a CSV...")

        self.chat_history = scrolledtext.ScrolledText(root, height=15, bg="#0f172a", fg="#f8fafc", font=("Segoe UI", 10))
        self.chat_history.pack(fill=BOTH, expand=True, padx=20, pady=10)

        self.input_frame = Frame(root)
        self.input_frame.pack(fill=X, padx=20, pady=10)
        
        self.user_input = Entry(self.input_frame, font=("Segoe UI", 11))
        self.user_input.pack(side=LEFT, fill=X, expand=True, ipady=4)
        self.user_input.bind("<Return>", lambda e: self.process_query())

        self.send_btn = Button(self.input_frame, text="Generate Plot", command=self.process_query, bg="#3b82f6", fg="white", padx=15)
        self.send_btn.pack(side=RIGHT, padx=5)

    def handle_drop(self, event):
        file_path = event.data.strip('{}')
        if file_path.lower().endswith('.csv'):
            self.file_path = file_path
            try:
                self.df = pd.read_csv(file_path)
                self.show_stats()
                self.chat_history.insert(END, f"\n[System]: Loaded {os.path.basename(file_path)} successfully.\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read CSV: {e}")
        else:
            messagebox.showerror("Error", "Please drop a valid CSV file.")

    def show_stats(self):
        summary = f"--- DATASET OVERVIEW ---\n"
        summary += f"Rows: {self.df.shape[0]} | Columns: {self.df.shape[1]}\n\n"
        summary += f"COLUMN TYPES:\n{self.df.dtypes.to_string()}\n\n"
        summary += f"STATISTICS:\n{self.df.describe().to_string()}"
        self.stats_area.delete(1.0, END)
        self.stats_area.insert(END, summary)

    def process_query(self):
        query = self.user_input.get()
        if not query: return
        if self.df is None:
            messagebox.showwarning("Warning", "Please upload a CSV file first!")
            return
        
        self.chat_history.insert(END, f"\nUser: {query}\n")
        self.user_input.delete(0, END)
        self.root.update_idletasks()

        # Data summary for LLM context
        data_summary = {
            "columns": list(self.df.columns),
            "sample": self.df.head(10).to_dict(orient='records'),
            "stats": self.df.describe().to_dict()
        }

        # Prompt focusing on the 12-column Grid Solution
        prompt = f"""
        Act as a React/Chart.js developer. Create a dashboard for this data:
        Columns: {data_summary['columns']}
        Sample: {json.dumps(data_summary['sample'])}
        
        Request: {query}
        
        Layout Requirements:
        1. Use a 12-column grid (`grid grid-cols-12`).
        2. Assign `col-span-12`, `col-span-8`, or `col-span-4` to charts based on their complexity.
        3. Use Tailwind CSS and Chart.js.
        4. Return ONLY the full HTML code, starting with <!DOCTYPE html>.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "system", "content": "You are a data visualization assistant."},
                          {"role": "user", "content": prompt}]
            )
            
            raw_html = response.choices[0].message.content
            # Clean up potential markdown formatting
            if "```html" in raw_html:
                raw_html = raw_html.split("```html")[1].split("```")[0]
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_code/dashboard_{timestamp}.html"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(raw_html)

            self.chat_history.insert(END, f"Agent: Dashboard generated successfully!\nLocation: {os.path.abspath(filename)}\n", "success")
        except Exception as e:
            self.chat_history.insert(END, f"Agent Error: {str(e)}\n")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = DataAgentApp(root)
    root.mainloop()