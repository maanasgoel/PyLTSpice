from mcp.server.fastmcp import FastMCP
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from PyLTSpice import SimRunner, SpiceEditor, RawRead

mcp = FastMCP("PyLTSpice MCP Server")

NETLIST_PATH = "rc_circuit.net"
OUTPUT_DIR = "output"
LTSPICE_PATH = "wine /Users/maanasgoel/.wine/drive_c/Users/maanasgoel/AppData/Local/Programs/ADI/LTspice/LTspice.exe"

@mcp.tool
def set_netlist(netlist_text: str) -> dict:
    with open(NETLIST_PATH, "w") as f:
        f.write(netlist_text)
    return {"status": "success", "message": "Netlist updated."}

@mcp.tool
def run_simulation() -> dict:
    netlist = SpiceEditor(NETLIST_PATH)
    runner = SimRunner(output_folder=OUTPUT_DIR, simulator=LTSPICE_PATH)
    runner.run_now(netlist)
    raw_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.raw')]
    if not raw_files:
        return {"status": "error", "message": "Simulation failed: No .raw file found."}
    return {"status": "success", "raw_file": os.path.join(OUTPUT_DIR, raw_files[0])}

@mcp.tool
def get_plot() -> dict:
    raw_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.raw')]
    if not raw_files:
        return {"status": "error", "message": "No .raw file found."}
    raw_path = os.path.join(OUTPUT_DIR, raw_files[0])
    raw = RawRead(raw_path)
    t = raw.get_trace("time").data
    vout = raw.get_trace("V(out)").data
    vin = raw.get_trace("V(in)").data
    sort_idx = np.argsort(t)
    t_sorted = t[sort_idx]
    vout_sorted = vout[sort_idx]
    vin_sorted = vin[sort_idx]
    mask = t_sorted >= 0
    plt.figure()
    plt.plot(t_sorted[mask], vout_sorted[mask], label="V(out)")
    plt.plot(t_sorted[mask], vin_sorted[mask], label="V(in)")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("RC Circuit Output")
    plt.legend()
    plt.grid(True)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    return {"status": "success", "image_base64": img_b64}

if __name__ == "__main__":
    mcp.run(transport="stdio")
