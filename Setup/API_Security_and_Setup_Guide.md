# API Security & `.env` Setup Guide

In modern AI engineering, protecting API keys (OpenAI, Gemini, Pinecone, etc.) is mandatory. Hardcoding keys directly into Python scripts and pushing them to a public GitHub repository will result in stolen credentials and immediate account bans.

We use a `.env` file as a local vault, combined with a `.gitignore` file, to keep keys secure.

## Step 1: Create the Vault (`.env`)
The `.env` file stores sensitive environment variables locally.

1. In the root directory of your PyCharm project, create a new file and name it exactly: `.env` 
   *(Note: There is nothing before the dot. It is just `.env`)*
2. Open the file and add your API keys in this format (no spaces around the `=` sign, and no quote marks around the key):
   ```text
   OPENAI_API_KEY=sk-your-actual-api-key-goes-here
   ```
3. Save and close the file.

## Step 2: Hide the Vault (`.gitignore`)
This is the most critical step. We must tell Git to completely ignore the `.env` file so it never gets pushed to GitHub.

1. In the root directory of your project, look for a file named `.gitignore`. 
   *(If it doesn't exist, create a new file named exactly `.gitignore`)*
2. Open `.gitignore` and add this exact line anywhere in the file:
   ```text
   .env
   ```
3. Save the file. In PyCharm, the `.env` file in your project explorer should now appear slightly grayed out or yellow, indicating Git is actively ignoring it.

## Step 3: Access the Keys in Python
Now that the key is secured locally, we use the `python-dotenv` library (which was installed via our `requirements.txt`) to pull the key into our scripts safely.

Whenever you start a new Jupyter Notebook or Python script, place this code at the very top:

```python
import os
from dotenv import load_dotenv

# This loads the vault
load_dotenv()

# This safely retrieves the key
api_key = os.getenv("OPENAI_API_KEY")
```
By using this method, your code functions perfectly on your local machine, but anyone looking at your public GitHub repository will only see the safe `os.getenv()` command, not your actual secret key.