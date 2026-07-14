# src/main_mcp_server.py
import json
import requests
from mcp.server.fastmcp import FastMCP
from src.core_math import compute_normalized_kinematic_intent

mcp = FastMCP("Century-Robust-BioHardware-Orchestrator")

@mcp.tool()
def fetch_genomic_data(gene_id: str) -> str:
    """
    Queries live open-access sequence parameters from the UniProt REST API.
    Gracefully falls back to mock sequences if the API is offline or restricted.
    """
    # Standard, non-hazardous accession numbers: P42212 (GFP), P01308 (Insulin)
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

@mcp.tool()
def resolve_biotech_spatial_intent(concentration_input: float, plate_scale_mm: float) -> str:
    """Translates assay parameters into immutable spatial metrics using SI base units (meters)."""
    intent = compute_normalized_kinematic_intent(concentration_input, "fluid_handling")
    target_meters = (intent["intent_vector"] * plate_scale_mm) / 1000.0
    return json.dumps({
        "schema_version": "2026.1.0",
        "vectors_meters": {"x_axis_delta": round(target_meters, 6)}
    })

if __name__ == "__main__":
    import time
    time.sleep(0.5)
    mcp.run(transport='stdio')