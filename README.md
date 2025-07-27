# ARP Spoofing Tool

A Python-based tool for performing ARP spoofing attacks on local networks.

## Description

This tool allows you to perform ARP cache poisoning attacks, enabling various man-in-the-middle (MITM) scenarios. It works by sending forged ARP replies to the target machine and the gateway, redirecting traffic through your machine.

## Features

- ARP cache poisoning for targeted devices
- Configurable packet interval timing
- Verbose output mode for debugging
- Automatic IP forwarding enable/disable

## Requirements

- Python 3
- root/administrator privileges
- npcap

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/0xAbolfazl/ARP-Spoofer.git
   cd ARP-Spoofer
2. Install dependencies:
    ```bash
    pip install -r requirements.txt

## Usage

### Running the Tool
1. **Main Interface**:  
   Run `main.py` to launch the interactive menu where you can choose between Graphical or Command Line versions:
   ```bash
   python main.py
2. **Direct Execution**:
    1. Command Line Version (CLI):
        - Execute cli.py directly with two options:
            1. Interactive Mode: Run without arguments and provide inputs when prompted
            ```bash
            python cli.py
            ```
            2. Argument Mode: Provide all parameters directly via command line
            ```bash
            python cli.py -t <target_ip> -g <gateway_ip> -i <interface> -s <delay>
    2. Graphical Version (GUI):
        Simply run gui.py to launch the graphical interface:
        ```bash
        python gui.py

### Command Line Options (CLI Version)

| Option               | Description                          | Default Value   |
|----------------------|--------------------------------------|-----------------|
| `-t` or `--target`   | Target IP address to spoof           | **Required**    |
| `-g` or `--gateway`  | Gateway/Router IP address            | **Required**    |
| `-i` or `--interface`| Network interface to use             | **Required**    |
| `-s` or `--speed`    | Delay between packets (in seconds)   | `2`             |

## Warning
- ⚠️ This tool is for educational and authorized testing purposes only.
- ⚠️ Unauthorized ARP spoofing may be illegal in your jurisdiction.
- ⚠️ Use only on networks you own or have permission to test.