# Local LLM Architecture: WSL & Ollama Setup

This guide details how to configure local, open-source Large Language Models (LLMs) to run entirely offline. By deploying the models inside Windows Subsystem for Linux (WSL), they can directly utilize the local NVIDIA RTX 4080 GPU for maximum inference speed, while still allowing the main project code to be executed natively on Windows PyCharm.

## Step 1: Base WSL & GPU Configuration

Before installing any AI models, the WSL environment must be properly configured to interface with the NVIDIA GPU. 

The complete, step-by-step documentation for initializing this environment is already detailed in the core `Learning-Logs` repository. Ensure that setup is complete before proceeding.
* [Reference: WSL & GPU Integration Guide](https://github.com/Shailya777/Learning-Logs/blob/main/Deep_Learning_with_Tensorflow/Theory_01_README_GPU_SETUP.ipynb)

## Step 2: Install the Ollama Engine

Ollama is the serving engine for local LLMs. It must be installed directly **inside the WSL terminal** (not on standard Windows) to guarantee seamless GPU handoff.

1. Open your Ubuntu/WSL terminal.
2. Execute the official installation script:
   ```bash
   curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
   ```

## Step 3: Pull and Execute an LLM

With the engine installed, models can be downloaded and run via the command line. The baseline model for this project is `llama3.1:8b` (approx. 4.9GB).

1. In the WSL terminal, pull and run the model:
   ```bash
   ollama run llama3.1:8b
   ```
2. The model will download and allocate directly into the GPU's VRAM. Once a `>>>` prompt appears in the terminal, the model is active and ready to receive prompts.

**Useful Storage Management Commands:**
* List all currently installed models: `ollama list`
* Delete a model to free up storage space: `ollama rm <model_name>`

## Step 4: Verify Cross-OS Communication

Ollama automatically broadcasts its API on `localhost:11434`. To verify that the Windows environment (PyCharm) can successfully send requests to the Linux environment (WSL), run the following Python test script.

```python
import requests

# Target the localhost port broadcasting from WSL
url = "http://localhost:11434/api/generate"

# Construct the payload targeting the specific downloaded model
payload = {
    "model": "llama3.1:8b",
    "prompt": "In one short sentence, what is the best thing about learning Python?",
    "stream": False
}

# Execute the request and parse the AI's response
response = requests.post(url, json=payload)
print(response.json()["response"])
```

> **⚠️ Connection Error?**
> If you receive a `ConnectionRefusedError`, `WinError 10061`, or `RemoteDisconnected` error when running this script, Windows and WSL are experiencing a "Split-Brain Networking" routing issue. 
> 
> **Do not panic.** This is a highly common architecture quirk. Follow the exact fix documented here: 
> [Troubleshooting: WSL to Windows Localhost Routing](./setup_wsl_networking_fix.md)