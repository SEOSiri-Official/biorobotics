# SEOSiri Bio-Robotics Core Engine
An open-source, stateless Model Context Protocol (MCP) framework bridging the gap between biological datasets and physical robotic actuation systems.

## 💖 Sponsorship & Open Source Attribution
This project is developed and maintained by **[SEOSiri-Official](https://github.com/SEOSiri-Official)** (Official website: [seosiri.com](https://seosiri.com)). 
To fund ongoing engineering research or scale the core physical kinematics engine, consider supporting the team via the [SEOSiri Sponsors Page](https://github.com/sponsors/SEOSiri-Official).

## Architecture Overview
This framework acts as a stateless broker. Biological inputs (fetched dynamically from standard web APIs or fallback reference data) are digested, normalized via mathematical boundaries, and translated into explicit Cartesian physical coordinates represented strictly in International System (SI) units (meters). These coordinates are subsequently mapped to standardized G-code strings for physical motion planning.

## Quickstart (CLI Orchestrator)
This project utilizes a local-first Python runtime to bypass IDE proxy lags and regional API restrictions, offering a stable and deterministic execution channel.

1. **Install Package in Editable Mode:**
   ```bash
   pip install -e .