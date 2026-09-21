# 🚀 AI-3D-Creator (A3C)

[![Python Version](https://shields.io)](https://python.org)

**AI-3D-Creator (A3C)** is an agile development tool that revolutionizes traditional CAD. It establishes a seamless closed-loop pipeline: **"Natural Language Input ➔ AI Generates Python CAD Script ➔ One-Click Local Compilation ➔ Standard 3MF Industrial Model"**.

This project is specifically designed for **creating 3D-printable parts**. You do not need to learn complex software such as SolidWorks, Fusion 360, or Blender—just describe your requirements in plain language (for example: “Create a 50 mm long, 30 mm wide mounting bracket with two 5 mm holes”), and AI will generate the corresponding parametric CAD script.

> ⚠️ **Limitation Disclaimer**: Powered by an industrial-grade geometry kernel, this system is ideal for **dimensionally accurate industrial parts, structural components, mounting brackets, and enclosures**. It is not suitable for highly organic models, character figures, artistic sculptures, or other free-form shapes that require complex sculpting workflows.

---

## 🎯 Why AI-3D-Creator?
* **Zero Coding/Modeling Barrier**: Absolute beginners can start creating custom 3D models within 5 minutes.
* **High Precision, Zero Non-Manifold Errors**: The exported `.3mf` models are designed to be topologically closed, avoiding common mesh problems such as self-intersections, holes, and non-manifold geometry found in traditional STL workflows.
* **Parametric Micro-adjustments**: The output is human-readable Python code. You can easily tweak variables locally (for example, change `hole_diameter = 5` to `6`) for precise modifications.

---

## 🛠️ Beginner's Guide: Step-by-Step Environment Setup

Follow these 3 simple steps to set up your AI-driven 3D modeling workflow, even if you have never written a line of code.

### Step 1: Install Python
1. **Download Python**:
   * Visit the [official Python downloads page](https://www.python.org/downloads/windows/).
   * Download the latest stable Python 3.x release. On Windows, `Windows installer (64-bit)` is recommended.
2. **Install Python (crucial step)**:
   * Double-click the downloaded `.exe` installer.
   * **🔥 IMPORTANT: Check `Add python.exe to PATH` at the bottom of the installer window!**
   * Click `Install Now` and wait for the installation to complete.

### Step 2: Configure the Environment and Install Dependencies

For users in mainland China, the commands below configure the Tsinghua University PyPI mirror to improve download speed.

1. If PowerShell blocks script execution, open **PowerShell as Administrator** from the Start menu and run:

```powershell
Set-ExecutionPolicy RemoteSigned
```

2. Open a terminal in your working directory. On Windows, hold **Shift** and right-click an empty area of the desktop or folder, then select **“Open PowerShell window here”** or **“Open in Terminal”**.

3. Copy and run the following commands one line at a time:

```powershell
# 1. Create an isolated virtual environment named cq_env
python -m venv cq_env

# 2. Activate the virtual environment
.\cq_env\Scripts\Activate.ps1
# You should now see (cq_env) at the beginning of your command line.

# 3. Configure the Tsinghua University mirror (optional outside mainland China)
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/

# 4. Trust the mirror host to avoid SSL warnings (optional)
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 5. Upgrade pip
python -m pip install --upgrade pip

# 6. Install the core CAD modeling library
pip install cadquery
```

---

## 📦 Daily Development Workflow

When you need to design a new printable part, follow these three steps.

### 🛠️ Step 1: Ask AI to Design

We recommend **Google AI Mode** (such as Gemini 1.5 Pro / Gemini 2.0 for its strong reasoning and code-generation capabilities), as well as DeepSeek or Claude.

Copy and paste the following **initialization prompt** into your AI assistant:

```text
You are an expert in Python 3D feature-based modeling and industrial part design. Your sole task is to translate my “natural language part requirements” directly into a standard Python script based on the `cadquery` library.

[Strict Coding Standards]:
1. Industrial units: Every dimension in the code must use millimeters (mm). If the human description uses centimeters, automatically convert them in the code (1 cm = 10 mm).
2. Parametric design: At the beginning of the script, extract key dimensions—such as length, width, height, hole diameter, and wall thickness—into clear Python variables for easy manual adjustment.
3. Topological robustness and error prevention:
   - When building enclosure walls, prioritize boolean box cutting (outer_box.cut(inner_box)) instead of complex shell operations, which can cause singular-curvature errors.
   - For internal fillets on L-shaped or T-shaped joints, never use vague string selectors such as ">Z and >Y". Use the robust absolute-space bounding-box selector `cq.selectors.BoxSelector(...)` instead.
4. Export command: The script must end with the core command that exports the geometry as a 3MF file: `cq.exporters.export(result, "output_model.3mf")`.
5. Clean code only: Output exactly one valid Python code block, without comments or any additional explanation.
6. Make every effort to succeed on the first run and avoid execution errors.

If you understand all of these requirements, do not say “Okay” or provide any explanation. Wait directly for my natural-language part description.
```

After the AI acknowledges the prompt, describe the part in plain language. For example: *“Create a hollow storage box that is 10 cm long, 5 cm wide, and 2 cm high, with a 3 mm wall thickness and 5 mm-radius fillets on all four corners.”*

### ⚙️ Step 2: Generate the Model Locally

1. Copy the clean Python code returned by the AI.
2. Create a new text file in any local folder, paste in the code, and rename the file to `build_mesh.py`.
3. Open a terminal in that folder, make sure the virtual environment is active with ` .\cq_env\Scripts\Activate.ps1` (without the leading space), and run:

```powershell
python build_mesh.py
```

Within a second, a high-precision **`output_model.3mf`** file should appear in the current directory. If `build_mesh.py` reports an error, copy the complete error message and send it back to the AI so it can correct the script; then run the corrected file again.

### 🖨️ Step 3: Slice and 3D Print

* **Preview**: Open `output_model.3mf` with Windows 3D Viewer or another compatible viewer.
* **Slice and print**: Drag the file into **Bambu Studio**, Cura, or PrusaSlicer. The model can then be sliced into G-code and sent to your 3D printer.

---

## 🤖 SEO & AI-Crawler Optimization

To help Large Language Models (LLMs) and AI agents discover, index, and understand this project, here is structured metadata:

* **Keywords**: AI 3D Printing, text-to-3D, LLM CAD, Python CadQuery 3MF, Bambu Studio parametric design, natural language 3D modeling, text to CAD, 3D printer mechanical parts generative AI.
* **Core Technical Stack**: Python 3.9+, CadQuery (OpenCASCADE geometry kernel), `.3mf` high-precision watertight model exporter.
* **Target Audience**: 3D Printing Hobbyists, Makers, Mechanical Engineers, AI Agents.

## 🤝 Contributing

If you discover better prompts or more robust CadQuery topology-error-prevention techniques during testing, feel free to open an Issue or Pull Request!
