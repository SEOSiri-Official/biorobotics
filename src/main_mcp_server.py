# src/main_mcp_server.py
import os
import sys

# Force the project root directory into the Python path to resolve 'src' packages cleanly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import requests
from mcp.server.fastmcp import FastMCP
from src.core_math import compute_normalized_kinematic_intent

# Initialize the MCP server
mcp = FastMCP("Century-Robust-BioHardware-Orchestrator")

# =====================================================================
# TOOL 1: SPATIAL INTENT (Translations to SI metric delta coordinates)
# =====================================================================
@mcp.tool()
def resolve_biotech_spatial_intent(concentration_input: float, plate_scale_mm: float) -> str:
    """Translates assay parameters into immutable spatial metrics using SI base units (meters)."""
    intent = compute_normalized_kinematic_intent(concentration_input, "fluid_handling")
    target_meters = (intent["intent_vector"] * plate_scale_mm) / 1000.0
    return json.dumps({
        "schema_version": "2026.1.0",
        "vectors_meters": {"x_axis_delta": round(target_meters, 6)}
    })

# =====================================================================
# TOOL 2: GENOMIC DATA FETCH (NCBI / UniProt API Interface)
# =====================================================================
@mcp.tool()
def fetch_genomic_data(gene_id: str) -> str:
    """
    Queries live open-access sequence parameters from the UniProt REST API.
    Gracefully falls back to mock sequences if the API is offline or restricted.
    """
    url = f"https://rest.uniprot.org/uniprotkb/{gene_id}.json"
    
    fallback_database = {
        "BRCA1": {"sequence": "MSR...[sequence_data]...G", "concentration_proxy": 45.0},
        "TP53": {"sequence": "MEE...[sequence_data]...A", "concentration_proxy": 12.8}
    }
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            sequence = data.get("sequence", {}).get("value", "")
            length = len(sequence)
            
            # Map benign molecular complexity to a metric proxy concentration
            concentration = round(float(length) * 0.1, 2)
            return json.dumps({
                "gene_id": gene_id,
                "sequence": sequence[:40] + "...",
                "sequence_length": length,
                "concentration_proxy": concentration,
                "source": "UniProt_Live_API",
                "status": "DATA_RETRIEVED"
            })
    except Exception:
        pass # Fall through to local fallback database on timeout/network issue
    
    # Fallback to local static database on failure
    record = fallback_database.get(gene_id, {"sequence": "UNKNOWN", "concentration_proxy": 10.0})
    return json.dumps({
        "gene_id": gene_id,
        "sequence": record["sequence"],
        "concentration_proxy": record["concentration_proxy"],
        "source": "Local_Fallback_Database",
        "status": "DATA_RETRIEVED"
    })

# =====================================================================
# NEW TOOL 3: ALPHANUMERIC WELL-PLATE MAPPING (96-Well SLAS Standards)
# =====================================================================
@mcp.tool()
def map_plate_coordinate(well_id: str, plate_format: int = 96) -> str:
    """
    Translates standard alphanumeric well IDs (e.g., 'A1' to 'H12') into 
    exact Cartesian offsets (X, Y) in millimeters based on SLAS/SBS standards.
    """
    well_id = well_id.upper().strip()
    if not well_id or len(well_id) < 2:
        return json.dumps({"error": "Invalid well format. Use format like 'A1'."})
        
    row_char = well_id[0]
    col_str = well_id[1:]
    
    # 96-Well Plate standard: 8 rows (A-H), 12 columns (1-12) with 9.0mm spacing
    if plate_format == 96:
        spacing_mm = 9.0
        max_rows = 8
        max_cols = 12
    else:
        return json.dumps({"error": "Unsupported plate format. Use 96."})

    row_index = ord(row_char) - ord('A')
    try:
        col_index = int(col_str) - 1
    except ValueError:
        return json.dumps({"error": "Column must be an integer."})

    if row_index < 0 or row_index >= max_rows or col_index < 0 or col_index >= max_cols:
        return json.dumps({"error": f"Well ID out of bounds for {plate_format}-well plate."})

    # Calculate offset relative to A1 home position (0,0)
    x_offset = round(col_index * spacing_mm, 3)
    y_offset = round(row_index * spacing_mm, 3)

    return json.dumps({
        "well_id": well_id,
        "plate_format": plate_format,
        "offsets_mm": {
            "x": x_offset,
            "y": y_offset
        }
    })

# =====================================================================
# NEW TOOL 4: VISCOSITY CALIBRATION (G-Code feedrate & volume calculation)
# =====================================================================
@mcp.tool()
def calculate_pipetting_speed(reagent_viscosity_cp: float, target_volume_uL: float) -> str:
    """
    Calculates the optimal safe feedrate (G-code speed) and physical delay times 
    based on the fluid viscosity (in cP) to ensure precise volumes and prevent splashing.
    """
    base_feedrate = 1500.0 # mm/min
    clamped_viscosity = max(0.8, min(reagent_viscosity_cp, 100.0))
    
    # Scale feedrate inversely with viscosity
    safe_feedrate = round(base_feedrate / clamped_viscosity, 1)
    
    # Calculate required pause time (in seconds) to allow pressure stabilization
    aspiration_delay_sec = round((target_volume_uL * 0.01) * clamped_viscosity, 2)
    
    return json.dumps({
        "input_viscosity_cp": clamped_viscosity,
        "target_volume_uL": target_volume_uL,
        "recommended_gcode_feedrate": max(100.0, safe_feedrate), # Prevent stalling below 100
        "pressure_delay_seconds": max(0.5, aspiration_delay_sec)
    })

# =====================================================================
# THE ENTRY POINT (MUST ALWAYS REMAIN AT THE ABSOLUTE BOTTOM)
# =====================================================================
if __name__ == "__main__":
    import time
    time.sleep(0.5)
    mcp.run(transport='stdio')