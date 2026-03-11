# Troubleshooting: WSL to Windows Localhost Routing

When running local LLMs (like Ollama) inside Windows Subsystem for Linux (WSL) and executing Python code natively on Windows (via PyCharm), you will likely encounter a `ConnectionRefusedError` or `RemoteDisconnected` error when targeting `http://localhost:11434`.

This guide documents the "Split-Brain Networking" issue between Windows and Linux and provides the permanent architectural fix used in this repository.

## The Problem: Two Different `localhosts`

By default, the Ollama engine installs with strict security settings. It binds exclusively to the internal Linux loopback address (`127.0.0.1`). 

When your Windows Python script knocks on the door at `localhost:11434`, two things fail:
1. **The Firewall Block:** Ollama actively refuses connections that don't originate from inside the Linux environment itself.
2. **The IPv6 Trap:** Windows often attempts to route `localhost` traffic through IPv6 (`::1`), which WSL fails to hand off properly to the IPv4 Linux backend, causing the connection to instantly drop.

## The Solution: Direct IP Routing & Open Hosting

To bypass this, we must configure the Ollama background service to listen to outside traffic (from the Windows side of the machine) and force our Python scripts to target the actual, physical IP address of the WSL virtual machine, bypassing the unreliable `localhost` alias entirely.

### Step 1: Open the Ollama Firewall (Run Once)
We must override Ollama's default system service to listen on `0.0.0.0` (all network interfaces). Run these commands in your WSL terminal:

```bash
# 1. Create a systemd override directory
sudo mkdir -p /etc/systemd/system/ollama.service.d

# 2. Inject the OLLAMA_HOST environment variable
echo '[Service]' | sudo tee /etc/systemd/system/ollama.service.d/override.conf
echo 'Environment="OLLAMA_HOST=0.0.0.0"' | sudo tee -a /etc/systemd/system/ollama.service.d/override.conf

# 3. Reload the daemon and restart the background service
sudo systemctl daemon-reload
sudo systemctl restart ollama
```
*Note: Because this modifies the background service, you only ever have to do this once per machine.*

### Step 2: Retrieve the Dynamic WSL IP Address (Run Daily)
WSL dynamically assigns a new internal IP address to the Linux subsystem every time you reboot your computer. Before running your Python code for the day, you must retrieve today's IP.

In your WSL terminal, run:
```bash
hostname -I
```
*(Copy the first IP address returned, e.g., `172.25.100.5`)*

### Step 3: Update the Python Architecture
In your Windows IDE, replace any standard `localhost` API calls with the direct WSL IP address.

**Incorrect (Relies on Windows Routing):**
```python
url = "http://localhost:11434/api/generate"
```

**Correct (Direct VM Targeting):**
```python
# Replace with today's dynamic WSL IP
url = "[http://172.](http://172.)x.x.x:11434/api/generate"
```

By explicitly defining the host environment (`0.0.0.0`) and targeting the exact IP address, the Windows IDE can seamlessly leverage the GPU-accelerated Linux environment without connection drops.