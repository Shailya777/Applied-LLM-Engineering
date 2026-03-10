# Applied LLM Engineering & Agentic AI

This repository documents my progression from traditional Machine Learning and NLP into modern Generative AI, specifically focusing on building production-ready Large Language Model (LLM) applications. 

The primary objective of this project is to master the applied integration of LLMs, Retrieval-Augmented Generation (RAG), and autonomous AI Agents, bridging my existing data stack with cutting-edge AI orchestration frameworks.

## 🛠️ Tech Stack & Tools
**Modern AI Stack:**
* **Orchestration:** LangChain, LangGraph
* **Models:** OpenAI API, Local Open-Source LLMs (via Ollama)
* **Architecture:** RAG (Retrieval-Augmented Generation), Agentic AI
* **Data Storage:** Vector Databases

**Foundational Data Stack:**
* Python, Pandas, Exploratory Data Analysis (EDA)
* Machine Learning & Deep Learning architectures
* Relational Databases (MySQL)

## 📂 Repository Structure
*(Note: I will update this section as the modules are completed)*
* `/setup` - Documentation on the custom Windows/Conda architecture used to run local LLMs via WSL.
* `/module_1_basics` - Foundational API connections and prompt templates.
* *(Upcoming)* `/rag_systems` - Document retrieval and vector search implementations.
* *(Upcoming)* `/ai_agents` - Autonomous agents executing multi-step reasoning tasks.

## ⚙️ Environment Architecture
To maintain maximum stability and avoid cross-OS file system lag, this project utilizes a custom hybrid architecture:
* Code execution and version control are handled natively on Windows via PyCharm and a Conda virtual environment.
* Local open-source LLMs are executed via Ollama inside Windows Subsystem for Linux (WSL) to fully leverage local NVIDIA RTX GPU acceleration, communicating with the Windows IDE over localhost. 
* [View the full setup documentation here](./setup/setup_windows_conda.md)

---
*Created by [Shailya](https://github.com/Shailya777)*
