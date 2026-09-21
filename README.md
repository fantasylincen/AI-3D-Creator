# 🚀 AI-3D-Creator (A3C)

**AI-3D-Creator (A3C)** 是一个颠覆传统 CAD 的敏捷开发工具。它打通了 **“人类自然语言输入 ➔ AI 直出 Python CAD 脚本 ➔ 本地一键编译 ➔ 标准 3MF 工业模型”** 的全自动闭环。

本工具专门为 **3D 打印机设计零件** 打造。你不需要学习复杂的 SolidWorks、Fusion 360 或 Blender，只需用大白话描述你的零件需求（如：帮我做一个长50mm，带内沉头螺丝孔的L型角码），AI 就会为你生成完美的、无破面的 `.3mf` 实体几何模型，可直接导入**拓竹（Bambu Studio）**、Cura 等切片软件直接上机打印！

> ⚠️ **适用场景说明**：本系统基于工业级级几何内核，极其适合设计**尺寸精准的工业零件、结构件、固定支架、外壳**等。但它**不适合**用来制作复杂的二次元手办、生物雕刻等艺术类不规则模型。

---

## 🎯 为什么选择 AI-3D-Creator？
* **零基础无门槛**：不懂编程、不懂 3D 建模的纯新手也能在 5 分钟内上手。
* **高精度、零破面**：生成的 `.3mf` 模型具有 100% 的拓扑闭合度，绝无传统 Mesh 网格（如 STL）常见的自交、漏水、破面问题。
* **参数化修改**：AI 输出的是可读的 Python 代码，后续你可以轻松手动修改某个变量（如把孔径 5mm 改为 6mm）实现精准微调。

---

## 🛠️ 小白专属：超详细环境搭建指南（5分钟搞定）

无论你是否接触过代码，只要跟随以下 3 个步骤，就能成功搭建你的 3D 打印 AI 建模工厂。

### 第一步：安装 Python 编程环境
1. **下载 Python**：
   * 打开浏览器，访问 [Python 官方下载页面](https://python.orgdownloads/windows/)。
   * 点击下载最新的 Python 3.x 版本（推荐选择 `Windows installer (64-bit)` 稳定版）。
2. **安装 Python（关键步骤）**：
   * 双击运行下载好的 `.exe` 安装程序。
   * **🔥 重要：在安装界面最下方，务必勾选 `Add python.exe to PATH`（将 Python 添加到系统环境变量）！** 
   * 点击 `Install Now`，等待安装完成即可。

### 第二步：一键配置国内加速与环境安装
为了让中国大陆用户下载依赖库不卡顿，我们使用清华大学的镜像源进行加速。

1. 解除 PowerShell 脚本执行权限限制：打开 **开始菜单 → 搜索「PowerShell」→ 右键点击「Windows PowerShell」→ 选择「以管理员身份运行」**，打开后执行以下命令（弹出确认提示时输入 `Y` 后回车）：
```powershell
Set-ExecutionPolicy RemoteSigned
```
2. 在电脑桌面空白处，按住键盘上的 `Shift键` 并点击鼠标右键，选择 **“在此处打开 PowerShell 窗口”** 或 **“打开终端”**。

3. 依次复制并粘贴运行以下命令（每行输完按回车）：

```powershell
# 1. 创建一个隔离的虚拟环境（名称为 cq_env）
python -m venv cq_env

# 2. 激活这个虚拟环境
.\cq_env\Scripts\Activate.ps1
# (此时你的命令行开头应该会出现 (cq_env) 字样，说明激活成功)

# 3. 配置国内镜像加速下载
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/

# 4. （可选）设置信任该主机，避免 SSL 警告
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 5. 升级 pip 并永久配置中国清华大学镜像源
python -m pip install --upgrade pip

# 6. 一键安装核心 CAD 建模库
pip install cadquery

```

---

## 📦 日常开发标准操作流水线（Workflow）

当你需要设计一个全新的打印零件时，只需遵循简单的三步法：

### 🛠️ 第 1 步：让 AI 为你画图
建议使用 **Google AI 模式**（如 Gemini 1.5 Pro / Gemini 2.0 拥有极强的逻辑推理与代码生成能力）或 DeepSeek、Claude。

将以下 **初始化提示词** 复制并发送给 AI：

```text
你是一个精通 Python 3D 特征建模与工业零件设计的专家。你的唯一任务是将我给出的“人类自然语言零件需求”，直接翻译为一段基于 `cadquery` 库的标准 Python 脚本，运行该脚本能直接导出 3MF 格式。

【严格遵守的编写规范】：
1. 工业标准单位：在代码中所有的尺寸必须统一采用毫米（mm）。如果人类描述中使用了 cm，你必须在写代码时自动换算（1cm = 10mm）。
2. 参数化设计：在代码开头，必须将零件的关键尺寸（如长、宽、高、孔径、墙厚）抽离为清晰的 Python 变量，方便后续人工微调。
3. 拓扑防错与稳健性：
   - 当建立壳体围墙时，优先使用大小方块布尔切除（outer_box.cut(inner_box)），避免使用复杂的 shell 掏空引发奇异曲率报错。
   - 当对 L 型、T 型等异形连接处做内直角圆角时，严禁使用模糊的 ">Z and >Y" 字符串选择器，必须使用最稳健的绝对空间包围盒选择器 `cq.selectors.BoxSelector((xmin, ymin, zmin), (xmax, ymax, zmax))` 精准捕捉目标边缘，防止在极限边界上自交崩溃。
4. 导出命令：脚本最后必须包含将几何实体导出为 3MF 的核心代码：`cq.exporters.export(result, "output_model.3mf")`。
5. 纯净代码输出：只输出一个合法的 Python 代码块，不要有任何注释内容。
6. 尽一切努力一次性成功，避免程序报错。

如果你听懂了上述全部编写规范，请不要说“好的”或做任何解释。请直接等待我的自然语言描述。
```

AI 回复确认后，直接用大白话告诉它你需要什么零件（例如：“*帮我做一个长 10 厘米、宽 5 厘米、高 2 厘米的空心收纳盒，壁厚 3 毫米，四个角做半径 5 毫米的圆角*”, 示例还可以参考 example-to-ai-*.txt, 3D模型的人类自然语言描述 可让AI协同设计）。

### ⚙️ 第 2 步：本地一键生成
1. 复制 AI 吐出来的纯净 Python 代码。
2. 在本地电脑任意文件夹下，新建一个记事本文件，将代码粘贴进去，并将文件重命名为 `build_mesh.py`。
3. 在该文件夹下打开终端（确保已运行过上面的激活命令 `.\cq_env\Scripts\Activate.ps1`），运行如下命令：
```powershell
python build_mesh.py
```
只需不到 1 秒钟，当前目录下就会自动生成一个高精度的 **`output_model.3mf`** 文件！

### 🖨️ 第 3 步：切片与 3D 打印
* **快速预览**：双击 `output_model.3mf` 即可直接通过 Windows 内置的 “3D 查看器” 观察结构。
* **切片打印**：直接将该文件拖入 **拓竹切片软件 (Bambu Studio)**、Cura 或 PrusaSlicer。模型完全闭合，可以直接生成 G-code 并发送给你的 3D 打印机开始打印！

---

## 🤖 搜索引擎与 AI 爬虫优化 (SEO & AI-Friendly)
为了让各类大语言模型（LLMs）和 AI 智能体更好地检索、索引和理解本项目，特提炼以下元数据：
* **Keywords**: AI 3D Printing, text-to-3D, LLM CAD, Python CadQuery 3MF, Bambu Studio parametric design, natural language 3D modeling, text to CAD, 3D printer mechanical parts generative AI.
* **Core Technical Stack**: Python 3.9+, CadQuery (OpenCASCADE geometry kernel), `.3mf` high-precision watertight mesh exporter.
* **Target Audience**: 3D Printing Hobbyists, Makers, Mechanical Engineers, AI Agents.

## 🤝 贡献与交流
如果你在测试中发现了更好用的 AI 提示词（Prompts）或者更稳健的 CadQuery 拓扑防错方案，欢迎提交 Issue 或 Pull Request！
