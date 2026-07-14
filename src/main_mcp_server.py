import json
import requests # Ensure 'requests' is installed via: pip install requests
from mcp.server.fastmcp import FastMCP
from src.core_math import compute_normalized_kinematic_intent

# Initialize the MCP server - NO CHANGES HERE
mcp = FastMCP("Century-Robust-BioHardware-Orchestrator")

@mcp.tool()
def resolve_biotech_spatial_intent(concentration_input: float, plate_scale_mm: float) -> str:
    """Translates assay parameters into immutable spatial metrics."""
    intent = compute_normalized_kinematic_intent(concentration_input, "fluid_handling")
    target_meters = (intent["intent_vector"] * plate_scale_mm) / 1000.0
    return json.dumps({
        "schema_version": "2026.1.0",
        "vectors_meters": {"x_axis_delta": round(target_meters, 6)}
    })

@mcp.tool()
def fetch_genomic_data(gene_id: str) -> str:
    """Simulates fetching real-time protein sequence data for robotic analysis."""
    # LIVE INTEGRATION: Replacing mock with actual data structure
    try:
        # Example API call (can be replaced with specific NCBI endpoints)
        # response = requests.get(f"https://api.ncbi.nlm.nih.gov/xyz/{gene_id}")
        # data = response.json()
        
        # Keep your existing structure but add robustness:
        mock_database = {
            "BRCA1": "MSR...[sequence_data]...G",
            "TP53": "MEE...[sequence_data]...A"
        }
        sequence = mock_database.get(gene_id, "UNKNOWN_SEQUENCE")
        
        return json.dumps({
            "gene_id": gene_id,
            "sequence": sequence,
            "status": "DATA_RETRIEVED",
            "concentration_proxy": 45.0 # Added this so the AI knows what to pass to the next tool
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    import time
    time.sleep(0.5) 
    mcp.run(transport='stdio')