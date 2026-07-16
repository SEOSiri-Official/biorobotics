# SEOSiri Bio-Robotics Core Engine

[![seosiri-biorobotics MCP server](https://glama.ai/mcp/servers/SEOSiri-Official/biorobotics/badges/card.svg)](https://glama.ai/mcp/servers/SEOSiri-Official/biorobotics)

An open-source, stateless Model Context Protocol (MCP) framework bridging the gap between biological datasets, physiological biosignals, and physical robotic actuation systems.

## 💖 Sponsorship & Open Source Attribution
This project is developed and maintained by **[SEOSiri-Official](https://github.com/SEOSiri-Official)** (Official website: [seosiri.com](https://seosiri.com)). 
To fund ongoing engineering research or scale the core physical kinematics engine, consider supporting the team via the [SEOSiri Sponsors Page](https://github.com/sponsors/SEOSiri-Official).

## Architecture Overview
This framework acts as a stateless broker. Biological inputs (fetched dynamically from standard web APIs like UniProt or fallback reference data) and physiological biosignals (such as surface electromyography, or EMG) are digested, normalized via mathematical boundaries, and translated into explicit Cartesian physical coordinates represented strictly in International System (SI) units (meters). These coordinates are subsequently mapped to standardized G-code strings for physical motion planning or robotic prosthetic actuation.

## Quickstart (CLI Orchestrator)
This project utilizes a local-first Python runtime to bypass IDE proxy lags and regional API restrictions, offering a stable and deterministic execution channel.

1. **Install Package in Editable Mode:**
   ```bash
   pip install -e .

2.  Execute the Decoupled Orchestrator (Live UniProt Fetch):

    # Queries live reference protein GFP (P42212)
    python src/run_experiment.py P42212

3.  Execute using Fallback Database:

    # Fallback reference run for BRCA1
    python src/run_experiment.py BRCA1

4.  Verify the CI/CD Pipeline:

    pytest tests/test_stability.py

🔌 How to Connect to Claude Desktop or Cursor IDE

You can connect this server to your local AI clients using one of two standard
methods.

Method 1: Direct Execution from GitHub (Zero-Setup, Recommended)

If you have uv installed, you can run the server directly from our public
repository without cloning it locally.

Open your claude_desktop_config.json (Windows:
%APPDATA%\Claude\claude_desktop_config.json | macOS: ~/Library/Application
Support/Claude/claude_desktop_config.json) and add this configuration:

{
  "mcpServers": {
    "seosiri-biorobotics": {
      "command": "uv",
      "args": [
        "run",
        "--github",
        "SEOSiri-Official/biorobotics",
        "src/main_mcp_server.py"
      ]
    }
  }
}

Method 2: Local Execution (If Cloned)

If you have cloned this repository to your local drive (e.g.,
D:/my-century-biorobotics-core), configure your client to point to your local
entry file:

{
  "mcpServers": {
    "seosiri-biorobotics": {
      "command": "python",
      "args": [
        "D:/my-century-biorobotics-core/src/main_mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "D:/my-century-biorobotics-core"
      }
    }
  }
}

License

Distributed under the MIT License. See LICENSE for more information.

