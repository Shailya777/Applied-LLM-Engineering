# Windows Environment Setup: Applied LLM Engineering

This guide details the exact environment architecture used for the `Applied-LLM-Engineering` repository. 

This setup intentionally deviates from the course's macOS-centric instructions (which use Cursor and `uv`). Instead, it is designed specifically for **Windows** users to provide a completely free, highly stable environment using **Anaconda**, **PyCharm**, and standard **pip**.

## 1. Core Architecture Decisions

Before running any commands, here is exactly why this environment is structured this way:

* **IDE (PyCharm over Cursor):** We use PyCharm installed natively on Windows. This bypasses cross-OS file system lag and avoids the PyCharm Professional paywall required for remote WSL interpreters. The free Unified version of PyCharm provides full, native support for Jupyter Notebooks (`.ipynb`), which is essential for this course.
* **Package Management (Conda + pip over `uv`):** While `uv` is exceptionally fast, it is an unnecessary learning curve for this sprint. We use a Conda virtual environment combined with standard `pip` installs via `requirements.txt` to maintain maximum compatibility with standard Data Science and Machine Learning workflows.
* **AI Execution (Localhost via WSL):** Later in the course, local LLMs (via Ollama) will be installed inside WSL (Windows Subsystem for Linux) to perfectly utilize the NVIDIA RTX GPU. PyCharm (on Windows) will communicate seamlessly with those models over the shared `localhost` network.

---

## 2. Step-by-Step Setup Guide

### Phase A: Install Prerequisites
Ensure the following tools are installed natively on your Windows machine:
1. **Anaconda Distribution** (for managing Python environments).
2. **PyCharm (Unified Version)** (ignore the 30-day Pro trial; core features and Jupyter support remain permanently free).
3. **Git for Windows** (for version control).

### Phase B: Repository Initialization (The Hybrid Method)
To ensure all daily code commits register to your own GitHub profile while still utilizing the instructor's setup:
1. Create a new, empty public repository on GitHub named `Applied-LLM-Engineering`.
2. Clone this new repository to a native Windows directory using PyCharm (e.g., `Documents\Applied-LLM-Engineering`).
3. Download the original course repository as a `.zip` file. Extract it to a separate `Reference_Materials` folder to use as a side-by-side reference and a source for dragging over necessary utility files.

### Phase C: Build the Virtual Environment
Open the standard **Anaconda Prompt** from the Windows Start Menu and run:
```bash
# Create the environment with Python 3.10 for maximum AI library stability
conda create -n applied_llm_engineering python=3.10 -y

# Verify creation
conda activate applied_llm_engineering
```

### Phase D: Link the Environment to PyCharm
1. Open the `Applied-LLM-Engineering` project in PyCharm.
2. Click the interpreter status in the bottom right corner (it may say "No Interpreter").
3. Select **Add New Interpreter** -> **Add Local Interpreter**.
4. Select **Conda Environment** on the left menu.
5. Choose **Use existing environment**.
6. Select `applied_llm_engineering` from the dropdown list and click **OK**. Allow PyCharm a moment to index the packages.

### Phase E: Install Dependencies
1. From your extracted course reference folder, copy **only** the `requirements.txt` file and paste it into the root of your `Applied-LLM-Engineering` PyCharm project. (You can ignore `environment.yml`, `pyproject.toml`, and `uv.lock`).
2. Open the **Terminal** tab at the bottom of PyCharm.
3. *Crucial Check:* Ensure `(applied_llm_engineering)` appears at the start of the terminal prompt.
4. Run the standard pip installation:
```bash
pip install -r requirements.txt
```

Once the installation completes, the environment is 100% synced with the course architecture and ready for development.