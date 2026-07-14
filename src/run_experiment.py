import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_lab_experiment(gene_id, scale):
    server_params = StdioServerParameters(
        command="python", # Uses system python
        args=["D:/my-century-biorobotics-core/src/main_mcp_server.py"],
        env={"PYTHONPATH": "D:/my-century-biorobotics-core"}
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Step 1: Fetch
            print(f"[Lab] Fetching data for: {gene_id}")
            result = await session.call_tool("fetch_genomic_data", arguments={"gene_id": gene_id})
            data = json.loads(result.content[0].text)
            
            # Step 2: Actuate
            conc = data["concentration_proxy"]
            print(f"[Lab] Actuating robot with concentration: {conc}")
            motion = await session.call_tool("resolve_biotech_spatial_intent", 
                                            arguments={"concentration_input": conc, "plate_scale_mm": scale})
            
            final_coord = json.loads(motion.content[0].text)
            print(f"--- SUCCESS ---")
            print(f"Final Robotic Coordinate: {final_coord}")

if __name__ == "__main__":
    gene = sys.argv[1] if len(sys.argv) > 1 else "BRCA1"
    asyncio.run(run_lab_experiment(gene, 100.0))