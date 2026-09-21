# 🚀 AI-3D-Creator (A3C)

[![Python Version](https://shields.io)](https://python.org)

**AI-3D-Creator (A3C)** is an agile development workflow that revolutionizes traditional CAD. It establishes a seamless closed-loop pipeline: **"Natural Language Input ➔ AI Generates Python CAD Script ➔ Local One-Click Compilation ➔ Standard 3MF Industrial Model"**.

This project is tailored specifically for **designing functional 3D printer parts**. Forget about learning complex software like SolidWorks, Fusion 360, or Blender. Simply describe your requirements in plain English (e.g., *“An L-shaped bracket with a length of 50mm and countersunk screw holes”*), and AI will output a flawless, watertight `.3mf` solid geometry model. It can be opened directly in **Bambu Studio**, Cura, or PrusaSlicer for immediate printing!

> ⚠️ **Limitation Disclaimer**: Powered by an industrial-grade geometry engine, this project is ideal for **dimensionally accurate mechanical parts, structural brackets, enclosures, and fixtures**. It is **NOT** suitable for organic shapes, anime figurines, or intricate artistic sculptures.

---

## 🎯 Why AI-3D-Creator?
* **Zero Coding/Modeling Barrier**: Absolute beginners can start creating custom 3D models within 5 minutes.
* **High Precision, Zero Non-Manifold Errors**: The exported `.3mf` files are 100% topologically closed, free from common mesh issues like self-intersections or holes found in traditional STLs.
* **Parametric Micro-adjustments**: The output is human-readable Python code. You can easily tweak variables locally (e.g., change `hole_diameter = 5` to `6`) for precise modifications.

---

## 🛠️ Beginner's Guide: Step-by-Step Environment Setup

Follow these 3 simple steps to set up your AI-driven 3D printing factory, even if you have never written a line of code.

### Step 1: Install Python
1. **Download**: Visit the [Official Python Downloads Page](https://python.orgdownloads/). Download the latest stable version for your OS (e.g., Windows Installer 64-bit).
2. **Install (Crucial Step)**:
   * Double-click the downloaded `.exe` installer.
   * **🔥 IMPORTANT: Check the box that says "Add python.exe to PATH" at the bottom of the installer window!**
   * Click `Install Now` and wait for it to finish.

### Step 2: Set Up the CAD Environment
1. Open your terminal (On Windows, hold `Shift` + Right-click on your desktop, and select **"Open PowerShell window here"** or **"Open Terminal"**).
2. Copy, paste, and run the following commands line by line:

```powershell
# 1. Create a isolated virtual environment named 'cq_env'
python -m venv cq_env

# 2. Activate the virtual environment
.\cq_env\Scripts\Activate.ps1
# (You should now see '(cq_env)' at the beginning of your terminal line)

# 3. Upgrade pip tool
python -m pip install --upgrade pip

# 4. Install the core CAD library
pip install cadquery
```
*(Note for Chinese Users: Pip source optimization has been implemented in the installer script to guarantee maximum download speeds via Tsinghua mirrors).*

---

## 📦 Daily Development Workflow

### 🛠️ Step 1: Ask AI to Design
We highly recommend using **Google AI Mode** (such as Gemini 1.5 Pro or Gemini 2.0 for their superior reasoning and code generation capabilities), though DeepSeek or Claude work excellently too.

Copy and paste this **System Prompt** to initialize your AI assistant:

```text
You are an expert in Python 3D parametric modeling and industrial part design. Your sole task is to translate my "natural language part description" into a standard Python script based on the `cadquery` library, which automatically exports a 3MF file upon execution.

[Strict Coding Standards]:
1. Industrial Units: All dimensions in the code must strictly use millimeters (mm). If the human description uses cm, you must automatically convert it (1cm = 10mm).
2. Parametric Design: At the beginning of the script, extract key dimensions (e.g., length, width, height, hole diameter, wall thickness) into clear Python variables for easy manual adjustments later.
3. Topological Robustness & Error-Prevention:
   - When building enclosures/hollow shells, prioritize boolean cutting of boxes (outer_box.cut(inner_box)) instead of complex .shell() operations to avoid curvature errors.
   - For internal fillets on L-shaped/T-shaped joints, never use vague string selectors like ">Z and >Y". You must use the highly robust bounding box selector `cq.selectors.BoxSelector((xmin, ymin, zmin), (xmax, ymax, zmax))` to accurately capture target edges and prevent self-intersection crashes.
4. Export Command: The script must conclude with the core code to export the geometry as a 3MF file: `cq.exporters.export(result, "output_model.3mf")`.
5. Clean Code Only: Output exactly one valid block of Python code, without any extra markdown explanations or conversational text.
6. Strive for one-shot success to avoid execution errors.

If you fully understand these instructions, do not say "Okay" or explain anything. Await my natural language description directly.
```

Once the AI acknowledges, describe your part in plain language (e.g., *“Create a hollow storage box with a length of 10cm, width of 5cm, height of 2cm, wall thickness of 3mm, and 5mm radius fillets on all four corners.”*).

### ⚙️ Step 2: One-Click Local Compilation
1. Copy the clean Python code provided by the AI.
2. Create a new text file in any local folder, paste the code, and rename the file to `build_mesh.py`.
3. Open a terminal in that folder (make sure `.\cq_env\Scripts\Activate.ps1` is activated), and run:
```powershell
python build_mesh.py
```
Within a fraction of a second, an **`output_model.3mf`** file will appear in the directory!

### 🖨️ Step 3: Slice and Print
* **Preview**: Double-click `output_model.3mf` to view the 3D model using the Windows native "3D Viewer".
* **Slicing**: Drag and drop the `.3mf` file directly into **Bambu Studio**, Cura, or PrusaSlicer. Slice it flawlessly, generate your G-code, and start your 3D printer!

---

## 🤖 SEO & AI-Crawler Optimization
To allow Large Language Models (LLMs) and AI Web Crawlers to effectively discover, index, and comprehend this repository, here is the structured metadata:
* **Keywords**: AI 3D Printing, text-to-3D, LLM CAD, Python CadQuery 3MF, Bambu Studio parametric design, natural language 3D modeling, text to CAD, 3D printer mechanical parts generative AI.
* **Core Technical Stack**: Python 3.9+, CadQuery (OpenCASCADE geometry kernel), `.3mf` high-precision watertight mesh exporter.
* **Target Audience**: 3D Printing Hobbyists, Makers, Mechanical Engineers, AI Agents.

## 🤝 Contributing
If you discover better Prompts or more robust topology error-prevention tricks for CadQuery during your testing, feel free to open an Issue or submit a Pull Request!
