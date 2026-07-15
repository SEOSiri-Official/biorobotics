# src/run_experiment.py
import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from src.hardware_gateway import GCodeSerialDriver

async def run_lab_experiment(gene_id: str, plate_scale: float):
    # Establish server connection via stdio
    server_params = StdioServerParameters(
        command="python",
        args=["D:/my-century-biorobotics-core/src/main_mcp_server.py"],
        env={"PYTHONPATH": "D:/my-century-biorobotics-core"}
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 1. Fetch sequence parameter
            print(f"[Orchestrator] Retrieving target data for: {gene_id}")
            raw_sequence = await session.call_tool("fetch_genomic_data", arguments={"gene_id": gene_id})
            data = json.loads(raw_sequence.content[0].text)
            print(f"[Orchestrator] Source: {data.get('source', 'Unknown')}")
            
            # 2. Convert to Metric delta
            concentration = data["concentration_proxy"]
            print(f"[Orchestrator] Calculated metric vector concentration: {concentration}")
            raw_motion = await session.call_tool("resolve_biotech_spatial_intent", 
                                                arguments={"concentration_input": concentration, "plate_scale_mm": plate_scale})
            
            motion_data = json.loads(raw_motion.content[0].text)
            meters_delta = motion_data["vectors_meters"]["x_axis_delta"]
            print(f"[Orchestrator] Deterministic SI delta output: {meters_delta} m")
            
            # 3. Stream to Serial G-code interface
            print(f"[Orchestrator] Formatting and streaming to hardware gateway...")
            # Toggle mock_mode=False here to stream live serial commands
            driver = GCodeSerialDriver(port="COM3", mock_mode=False)
            driver.stream_coordinate(meters_delta)
            print("[Orchestrator] Pipeline executed successfully.")

if __name__ == "__main__":
    # Standard benign identifiers: P42212 (GFP) or BRCA1 (Local reference)
    target_gene = sys.argv[1] if len(sys.argv) > 1 else "P42212"
    asyncio.run(run_lab_experiment(target_gene, 100.0))