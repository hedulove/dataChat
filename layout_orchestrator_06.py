import os
import json
import re
from datetime import datetime
from tkinter import *
from tkinter import scrolledtext, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import openai
from dotenv import load_dotenv

# --- API CONFIGURATION ---
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY5"))
os.makedirs("assembled_dashboards", exist_ok=True)

class DashboardAssembler:
    def __init__(self, root):
        self.root = root
        self.root.title("Nexus Dashboard Assembler - FIXED")
        self.root.geometry("900x850")
        self.component_files = []
        self.master_template_path = None

        # --- UI SETUP ---
        self.comp_label = Label(root, text="1. Drag & Drop Chart HTMLs here", 
                               bg="#eff6ff", fg="#1e40af", height=4, relief="ridge", bd=2)
        self.comp_label.pack(fill=X, padx=20, pady=10)
        self.comp_label.drop_target_register(DND_FILES)
        self.comp_label.dnd_bind('<<Drop>>', self.handle_comp_drop)

        self.master_label = Label(root, text="2. Drag & Drop master_react.html", 
                                 bg="#f0fdf4", fg="#166534", height=3, relief="ridge", bd=2)
        self.master_label.pack(fill=X, padx=20, pady=10)
        self.master_label.drop_target_register(DND_FILES)
        self.master_label.dnd_bind('<<Drop>>', self.handle_master_drop)

        self.file_list = scrolledtext.ScrolledText(root, height=6, bg="#ffffff", font=("Consolas", 9))
        self.file_list.pack(fill=X, padx=20, pady=5)

        Label(root, text="Additional Layout Instructions:", fg="#475569").pack(anchor=W, padx=20)
        self.instructions = Text(root, height=4, font=("Segoe UI", 10))
        self.instructions.pack(fill=X, padx=20, pady=5)

        self.log = scrolledtext.ScrolledText(root, height=10, bg="#0f172a", fg="#f8fafc")
        self.log.pack(fill=BOTH, expand=True, padx=20, pady=10)

        self.assemble_btn = Button(root, text="ASSEMBLE REACT DASHBOARD", 
                                   command=self.assemble_dashboard, bg="#3b82f6", fg="white", 
                                   font=("Segoe UI", 10, "bold"), pady=10)
        self.assemble_btn.pack(fill=X, padx=20, pady=10)

    def handle_comp_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for f in files:
            path = f.strip('{}')
            if path not in self.component_files: self.component_files.append(path)
        self.update_ui()

    def handle_master_drop(self, event):
        self.master_template_path = event.data.strip('{}')
        self.update_ui()

    def update_ui(self):
        self.file_list.delete(1.0, END)
        master = os.path.basename(self.master_template_path) if self.master_template_path else "NONE"
        self.file_list.insert(END, f"MASTER: {master}\nCOMPONENTS:\n" + "\n".join([os.path.basename(f) for f in self.component_files]))

    def extract_react_logic(self, html_content):
        match = re.search(r'<script type="text/babel">(.*?)</script>', html_content, re.DOTALL)
        if match:
            logic = match.group(1)
            logic = re.sub(r'const root = ReactDOM\.createRoot.*', '', logic, flags=re.DOTALL)
            logic = re.sub(r'import .* from .*;', '', logic)
            return logic.strip()
        return html_content.strip()

    def assemble_dashboard(self):
        if not self.master_template_path or not self.component_files:
            messagebox.showwarning("Error", "Please provide the template and components.")
            return

        self.log.insert(END, f"\n[{datetime.now().strftime('%H:%M:%S')}] Starting Assembly...\n")
        
        try:
            components_data = []
            for path in self.component_files:
                with open(path, 'r', encoding='utf-8') as f:
                    logic = self.extract_react_logic(f.read())
                    components_data.append({"filename": os.path.basename(path), "logic": logic})

            user_instr = self.instructions.get(1.0, END).strip()
            
            # --- IMPROVED PROMPT TO FIX NESTED GRID AND CHART SIZE ISSUES ---
            prompt = f"""You are a React Expert working with browser-side Babel.

CRITICAL RULES:
1. NO 'import' or 'require' statements
2. Use React.useRef and React.useEffect (not destructured)
3. NO document.getElementById
4. NO NESTED GRIDS - each card must be a direct child
5. ALL charts need: responsive: true, maintainAspectRatio: false

SOURCE COMPONENTS:
{json.dumps(components_data, indent=2)}

COMPONENT PATTERN (copy this exactly):
const ComponentName = () => {{
    const canvasRef = React.useRef(null);
    React.useEffect(() => {{
        const ctx = canvasRef.current.getContext('2d');
        const chart = new Chart(ctx, {{
            type: 'bar',  // or line, pie, doughnut, etc
            data: {{ labels: [...], datasets: [...] }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: true }} }}
            }}
        }});
        return () => chart.destroy();
    }}, []);
    return <canvas ref={{canvasRef}} />;
}};

LAYOUT STRUCTURE (NO wrapper divs around cards):
<div className="col-span-12 lg:col-span-6 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
    <h3 className="font-bold text-lg mb-4 text-slate-800">Chart Title</h3>
    <div className="h-80 w-full relative"><ComponentName /></div>
</div>

SIZING OPTIONS:
- Half width: "col-span-12 lg:col-span-6"
- Full width: "col-span-12"
- 2/3 width: "col-span-12 lg:col-span-8"

CRITICAL: Return ONLY the card divs (no wrapper). They go directly into the existing grid.

User layout preferences: {user_instr if user_instr else "Use intelligent 2-column layout"}

Return JSON with:
{{
    "functions": "all React component definitions",
    "grid_jsx": "card divs only, no wrapper grid"
}}"""

            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )

            res_data = json.loads(response.choices[0].message.content)

            with open(self.master_template_path, 'r', encoding='utf-8') as f:
                master_content = f.read()

            # Replace injection markers
            final_content = master_content.replace("/* COMPONENTS_GO_HERE */", res_data['functions'])
            final_content = final_content.replace("{/* GRID_CONTENT_GOES_HERE */}", res_data['grid_jsx'])

            # Save result
            out_path = f"assembled_dashboards/dashboard_fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(final_content)

            self.log.insert(END, f"✓ Success! Dashboard created:\n{out_path}\n")
            self.log.insert(END, f"\n✓ Charts will be properly sized (h-80 = 320px height)\n")
            self.log.insert(END, f"✓ No nested grids - clean layout\n")
            
        except Exception as e:
            self.log.insert(END, f"✗ Error: {str(e)}\n")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = DashboardAssembler(root)
    root.mainloop()
