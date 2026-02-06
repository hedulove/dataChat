# dataChat
Chatbot AI agent to generate plots and insights from data 

# Nexus Data Agent & Dashboard Assembler

A dual-tool suite designed to transform raw CSV data into interactive, professional React-based dashboards using LLM-powered code generation. This project automates the transition from data exploration to high-fidelity visualization using **Python**, **Tkinter**, and the **OpenAI API**.

---

## ## Features

* **Nexus Data Agent**:
* Drag-and-drop CSV interface.
* Automatic data profiling (statistics and column types).
* Natural language to dashboard generation (React + Chart.js + Tailwind CSS).


* **Dashboard Assembler**:
* Merges multiple generated chart components into a unified master dashboard.
* Enforces a clean **12-column responsive grid**.
* Automates React logic extraction and injection.
* Ensures chart responsiveness and proper canvas scaling.



---

## ## Prerequisites

Before running the applications, ensure you have the following:

* **Python 3.8+**
* **OpenAI API Key**: Access to GPT-4 Turbo or similar models.
* **Tkinter**: Usually included with Python (Linux users may need `sudo apt-get install python3-tk`).

---

## ## Installation

1. **Clone the Repository**:
```bash
git clone https://github.com/yourusername/nexus-data-agent.git
cd nexus-data-agent

```


2. **Install Dependencies**:
This project requires specialized libraries for Drag-and-Drop functionality and OpenAI integration.
```bash
pip install pandas openai python-dotenv tkinterdnd2

```


3. **Configure Environment Variables**:
Create a `.env` file in the root directory and add your OpenAI API key:
```env
OPENAI_API_KEY5=your_api_key_here

```



---

## ## Usage Guide

### 1. Generating Charts (`genChart_01.py`)

This tool creates individual dashboard components based on your data.

* Run the script: `python genChart_01.py`
* **Drag & Drop** a CSV file into the designated area.
* Type a query (e.g., *"Show me a bar chart of sales by region and a pie chart of category distribution"*) and click **Generate Plot**.
* The generated HTML files will be saved in the `generated_code/` folder.

### 2. Assembling the Dashboard (`layout_orchestrator_06.py`)

This tool stitches components together into a final, production-ready React layout.

* Run the script: `python layout_orchestrator_06.py`
* **Step 1**: Drag the HTML files generated in the previous step into the blue area.
* **Step 2**: Drag your `master_react.html` template into the green area.
* Add any specific layout instructions (e.g., *"Put the sales chart at the top full-width"*) and click **Assemble**.
* The final result will be in the `assembled_dashboards/` folder.

---

## ## Technical Architecture

| Component | Technology | Purpose |
| --- | --- | --- |
| **GUI Framework** | `Tkinter` / `TkinterDnD` | Cross-platform desktop interface with file handling. |
| **Data Processing** | `Pandas` | Summarizing CSV structure for LLM context. |
| **LLM Engine** | `OpenAI GPT-4 Turbo` | Translating data summaries into functional React code. |
| **Frontend Stack** | `Chart.js`, `Tailwind CSS`, `React` | Modern, responsive, and interactive visualizations. |

---

## ## File Structure

* `genChart_01.py`: The primary agent for data analysis and initial code generation.
* `layout_orchestrator_06.py`: The logic handler for component extraction and assembly.
* `generated_code/`: (Auto-generated) Stores individual chart HTML files.
* `assembled_dashboards/`: (Auto-generated) Stores the final unified dashboard.

---

## ## Troubleshooting

* **DND Error**: If the Drag & Drop fails, ensure you have installed `tkinterdnd2` correctly. On some systems, you may need to manually point to the Tcl/Tk binary.
* **API Limits**: Ensure your OpenAI account has sufficient credits for `gpt-4-turbo-preview` calls.
* **Layout Issues**: The Assembler expects a `master_react.html` with specific markers (`/* COMPONENTS_GO_HERE */` and `{/* GRID_CONTENT_GOES_HERE */}`).


---

## ## 👤 Developer

**Hector Duran** *Main Creator and Lead Architect*

---

## ## 📄 License

This project is licensed under the **MIT License**.

> **Summary**: You are free to use, copy, and modify this software for any purpose. The only requirement is that the original copyright notice and this permission notice must be included in all copies or substantial portions of the software.

---




