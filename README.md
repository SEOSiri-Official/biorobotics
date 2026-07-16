# SEOSiri Bio-Robotics Core Engine

[![seosiri-biorobotics MCP server](https://glama.ai/mcp/servers/SEOSiri-Official/biorobotics/badges/card.svg)](https://glama.ai/mcp/servers/SEOSiri-Official/biorobotics)

An open-source, stateless Model Context Protocol (MCP) framework bridging the gap between biological datasets, physiological biosignals, and physical robotic actuation systems.

## 💖 Sponsorship & Open Source Attribution

This project is developed and maintained by **[SEOSiri-Official](https://github.com/SEOSiri-Official)** (Official website: [seosiri.com](https://seosiri.com)).

To fund ongoing engineering research or scale the core physical kinematics engine, consider supporting the team via the [SEOSiri Sponsors Page](https://github.com/sponsors/SEOSiri-Official).

## Architecture Overview

This framework acts as a stateless broker. Biological inputs (fetched dynamically from standard web APIs like UniProt or fallback reference data) and physiological biosignals (such as surface electromyography, or EMG) are digested, normalized via mathematical boundaries, and translated into explicit Cartesian physical coordinates represented strictly in International System (SI) units (meters). These coordinates are subsequently mapped to standardized G-code strings for physical motion planning or robotic prosthetic actuation.

```
[Raw Input: Bio-Data / EMG] → [Stateless MCP Server] → [Deterministic Math Core] → [G-code Serial Stream]
```

## Tools

This server exposes six MCP tools:

| Tool | Description |
|---|---|
| `fetch_genomic_data` | Queries live sequence parameters from the UniProt REST API, with a local fallback for offline or rate-limited conditions. |
| `resolve_biotech_spatial_intent` | Translates assay parameters (concentration, plate scale) into immutable spatial metrics in SI base units. |
| `map_plate_coordinate` | Translates alphanumeric well IDs (e.g. `A1`–`H12`) into exact millimeter offsets, per SLAS/SBS 96-well plate standards. |
| `calculate_pipetting_speed` | Calibrates G-code feedrate and pressure delay from reagent viscosity and target volume. |
| `calculate_dna_melting_temp` | Calculates GC-content and melting temperature (Tm) of a DNA sequence for thermal deck configuration. |
| `translate_emg_to_actuation` | Translates EMG muscle signals (µV) into safe joint angles and G-code velocity profiles, with a built-in safety envelope check. |

## Quickstart (CLI Orchestrator)

This project utilizes a local-first Python runtime to bypass IDE proxy lags and regional API restrictions, offering a stable and deterministic execution channel.

1. **Install Package in Editable Mode:**
```bash
   pip install -e .
```

2. **Execute the Decoupled Orchestrator (Live UniProt Fetch):**
```bash
   # Queries live reference protein GFP (P42212)
   python src/run_experiment.py P42212
```

3. **Execute Using Fallback Database:**
```bash
   # Fallback reference run for BRCA1
   python src/run_experiment.py BRCA1
```

4. **Verify the CI/CD Pipeline:**
```bash
   pytest tests/test_stability.py
```

## 🔌 How to Connect to Claude Desktop or Cursor IDE

You can connect this server to your local AI clients using one of two standard methods.

### Method 1: Direct Execution from GitHub (Zero-Setup, Recommended)

If you have `uv` installed, you can run the server directly from our public repository without cloning it locally.

Open your `claude_desktop_config.json` (Windows: `%APPDATA%\Claude\claude_desktop_config.json` | macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`) and add this configuration:

```json
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
```

### Method 2: Local Execution (If Cloned)

If you have cloned this repository to your local drive (e.g., `D:/my-century-biorobotics-core`), configure your client to point to your local entry file:

```json
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
```

## Verified Live Test Results

All six tools have been independently tested against the running server via Glama.ai's browser-based MCP Inspector, with output matching each tool's closed-form mathematical model exactly:

| Tool | Input | Verified Output |
|---|---|---|
| `fetch_genomic_data` | `P42212` (GFP) | 238-residue sequence, `source: UniProt_Live_API`, `status: DATA_RETRIEVED` |
| `resolve_biotech_spatial_intent` | concentration=22.8, plate_scale_mm=100.0 | `x_axis_delta: 0.022413` m |
| `map_plate_coordinate` | well=`B5`, plate_format=96 | `x: 36, y: 9` mm |
| `calculate_pipetting_speed` | viscosity_cp=5.0, volume_ul=50.0 | `recommended_gcode_feedrate: 300`, `pressure_delay_seconds: 2.5` |
| `translate_emg_to_actuation` | emg_uV=350, joint=`elbow_servo` | `calculated_angle_degrees: 63`, `gcode_command: "G1 X63.0 F1500.0"`, `safety_envelope: NOMINAL` |

## Technical Specifications

- **Communication protocol:** Model Context Protocol JSON-RPC over stdio
- **Actuation protocol:** Cartesian G-code, per the [NIST RS274/NGC interpreter specification](https://www.nist.gov/publications/nist-rs274ngc-interpreter-version-3)
- **Coordinate space:** SI units (meters), with millimeter-scale conversions for plate-level operations
- **Verification:** automated unit testing via [pytest](https://docs.pytest.org/)
- **Containerization:** Dockerfile included for isolated runtime environments
- **Directory sync:** `glama.json` drives the automatic Glama.ai listing sync
- **Language:** Python
- **Compatible platforms:** Linux, macOS, Windows

## Requirements

- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv) (optional, for zero-setup remote execution) or `pip`
- An MCP-compatible client (Claude Desktop, Cursor IDE, or Glama's browser-based Inspector)

## Contributing

Issues and pull requests are welcome. This is a small, modular, readable Python codebase with clear separation of concerns (`core_math.py`, `hardware_gateway.py`, `main_mcp_server.py`) — a reasonable reference implementation if you're building your own MCP server for a physical-hardware use case.

## Roadmap

- **Closed-loop telemetry:** parsing real-time coordinate position queries from serial ports to verify physical arrival
- **Capacitive liquid-level detection (LLD):** halting probe movement immediately on contact with a liquid surface, to prevent pipette tip damage

## ⚠️ Safety Note

`translate_emg_to_actuation` is a translation and safety-check layer suitable for research and prototyping — it is not a certified medical or prosthetic control system. Any clinical or assistive deployment requires independent regulatory validation beyond the scope of this project.

## License

Distributed under the MIT License. See [LICENSE](https://github.com/SEOSiri-Official/biorobotics/blob/main/LICENSE) for more information.

## Links

- **Repository:** [github.com/SEOSiri-Official/biorobotics](https://github.com/SEOSiri-Official/biorobotics)
- **MCP Directory Listing:** [glama.ai/mcp/servers/SEOSiri-Official/biorobotics](https://glama.ai/mcp/servers/SEOSiri-Official/biorobotics)
- **Technical Article:** [seosiri.com/2026/07/seosiri-bio-robotics-core-engine.html](https://www.seosiri.com/2026/07/seosiri-bio-robotics-core-engine.html)