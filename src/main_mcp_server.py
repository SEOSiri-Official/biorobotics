import json
from mcp.server.fastmcp import FastMCP
from src.core_math import compute_normalized_kinematic_intent

mcp = FastMCP("Century-Robust-BioHardware-Orchestrator")

@mcp.tool()
def resolve_biotech_spatial_intent(concentration_input: float, plate_scale_mm: float) -> str:
    intent = compute_normalized_kinematic_intent(concentration_input, "fluid_handling")
    target_meters = (intent["intent_vector"] * plate_scale_mm) / 1000.0
    return json.dumps({
        "schema_version": "2026.1.0",
        "vectors_meters": {"x_axis_delta": round(target_meters, 6)}
    })

if __name__ == "__main__":
    mcp.run(transport='stdio')