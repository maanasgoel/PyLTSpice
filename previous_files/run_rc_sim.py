import sys
import os

# Only needed if you didn't pip install PyLTSpice, but using source code directly:
sys.path.append("/Users/maanasgoel/Documents/Cursor/PySpice/PyLTSpice")

from PyLTSpice import SimRunner, SpiceEditor, RawRead

import matplotlib.pyplot as plt
import numpy as np

# Path to your Wine LTspice executable (include 'wine' at the start!)
ltspice_path = "wine /Users/maanasgoel/.wine/drive_c/Users/maanasgoel/AppData/Local/Programs/ADI/LTspice/LTspice.exe"

# 1. Load the netlist
netlist = SpiceEditor("PyLTSpice/test/rc_circuit.net")

# 2. Run the simulation
runner = SimRunner(output_folder='./output', simulator=ltspice_path)
runner.run_now(netlist)

# 3. Find the .raw file in the output folder
raw_files = [f for f in os.listdir('./output') if f.endswith('.raw')]
if not raw_files:
    print("Simulation failed: No .raw file found. Check LTspice path and Wine setup.")
    exit(1)
raw_path = os.path.join('./output', raw_files[0])

# 4. Read and plot the results
raw = RawRead(raw_path)
print("Available traces:", raw.get_trace_names())
t = raw.get_trace("time").data
vout = raw.get_trace("V(out)").data
vin = raw.get_trace("V(in)").data

# Debug: Print time range and first 10 values
print("Time min:", t.min(), "Time max:", t.max())
print("First 10 time values:", t[:10])

# Sort the data by time before plotting
sort_idx = np.argsort(t)
t_sorted = t[sort_idx]
vout_sorted = vout[sort_idx]

# Only plot t >= 0
mask = t_sorted >= 0
plt.plot(t_sorted[mask], vout_sorted[mask], label="V(out)")
plt.plot(t_sorted[mask], vin[sort_idx][mask], label="V(in)")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("RC Circuit Output")
plt.legend()
plt.grid(True)
plt.show() 