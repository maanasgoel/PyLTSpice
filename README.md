# AI-Powered LTSpice Automation

This project provides a suite of tools that allow an AI assistant, like the one in Cursor, to programmatically control the LTSpice electronic circuit simulator. You can describe a circuit in plain English, have the AI generate a netlist, run a simulation, and plot the results, creating a seamless, conversational workflow for circuit analysis.

This project is designed for engineers, students, and hobbyists who want to speed up their simulation workflow and leverage the power of Large Language Models for circuit design.

![Demo](https://path-to-your/demo.gif)  <!-- Replace with a link to your demo video/gif -->

---

## Features In-Depth

-   **Conversational Circuit Design**: Describe any circuit with standard components (resistors, capacitors, inductors, voltage/current sources) and their connections. The AI assistant can generate valid SPICE netlists for transient (`.tran`), AC (`.ac`), and DC operating point (`.op`) analyses.

-   **Step-by-Step Simulation**: A guided, interactive workflow that mimics how an engineer uses LTSpice: create, inspect, run, and plot. The AI will wait for your confirmation at each step.

-   **Automated Session Management**: Each simulation is saved in a unique, timestamped `simulation_output` directory, keeping all your artifacts (netlist, logs, raw data, plots) neatly organized.

-   **Headless Simulation**: Run LTSpice simulations in the background without opening the GUI, perfect for quick calculations or automated test scripts.

-   **Generates Plot Files**: Ask for plots of any node voltage (`V(node_name)`) or component current (`I(R1)`). The AI generates a `.png` image file and saves it in the session directory.

-   **Comprehensive Data Access**: All simulation data is saved in standard `.raw` format, allowing you to use any SPICE-compatible analysis tool of your choice.

-   **Built-in Debugging**: If a simulation fails, you can ask the AI to read the log file and help you understand what went wrong.

---

## Example Workflow: Simulating an RLC Circuit

Here is an example of the interactive workflow in action.

**You:**
> I want to simulate a custom RLC circuit. First, please generate the SPICE netlist with the following components:
> * A voltage source V1 from node `in` to `0`. It should be a 10V pulse that starts at 1ms, has a 1us rise/fall time, a 1ms pulse width, and a 5ms period.
> * A 50Ω resistor R1 from node `in` to `out`.
> * A 1mH inductor L1 from node `out` to `mid`.
> * A 10uF capacitor C1 from node `mid` to `0`.
>
> The simulation should be a transient analysis for 5ms. Please show me the generated netlist before doing anything else.

**AI:**
> Of course. Here is the netlist for the RLC circuit you described:
> ```spice
> * RLC Circuit
> V1 in 0 PULSE(0 10 1m 1u 1u 1m 5m)
> R1 in out 50
> L1 out mid 1mH
> C1 mid 0 10uF
> .tran 5m
> .end
> ```
> I have created a new simulation session for this netlist. Please let me know if this looks correct, and I will proceed with running the simulation.

**You:**
> Looks good, please run the simulation.

**AI:**
> ✅ Simulation successful! All the output files have been saved in the session folder `simulation_output/20250703_150000/`. What would you like to do next? For example, I can list the available signals for plotting.

**You:**
> Yes, what can I plot?

**AI:**
> The following signals are available from the simulation: `V(in)`, `V(out)`, `V(mid)`, `I(V1)`, `I(R1)`, `I(L1)`, `I(C1)`.

**You:**
> Please plot V(out) for me.

**AI:**
> 📈 Plot generated successfully!
> - **File:** `plot_V(out).png`
> - **Location:** `simulation_output/20250703_150000/`
>
> You can open this image file to view the plot of V(out). What would you like to do next?

**You:**
> Great. Can you plot some other signals too?

**AI:**
> Absolutely! Which signals would you like to see? For example, I can plot:
> - `V(in)` - the input pulse signal  
> - `V(mid)` - voltage across the capacitor
> - `I(L1)` - current through the inductor
> - Or any combination of these signals on the same plot
>
> Just let me know which ones interest you!

---

## Setup and Installation

Follow these steps carefully to configure your environment.

### 1. Prerequisites

-   **LTSpice**: You must have LTSpice installed.
    -   [Download for Windows/macOS](https://www.analog.com/en/design-center/design-tools-and-calculators/ltspice-simulator.html)
-   **Wine (for macOS/Linux users)**: Since LTSpice is a Windows application, you need a compatibility layer like Wine or a commercial version like [CrossOver](https://www.codeweavers.com/crossover/) to run it.
    -   Install Wine using [Homebrew](https://brew.sh/): `brew install wine-stable`
-   **Cursor (or another MCP-compatible editor)**: This project is designed to work with an AI editor that supports MCP.
    -   [Download Cursor](https://cursor.sh/)
-   **Python & Conda**: A Python environment manager like Conda is highly recommended.
    -   [Download Miniconda](https://docs.conda.io/en/latest/miniconda.html)

### 2. Project Setup

**Step 1: Clone the Repository & Navigate into It**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

**Step 2: Create Conda Environment & Install Dependencies**
From the project's root directory (`your-repo-name`), run the following commands:

```bash
# Create a new conda environment named 'pyspice_env' with Python 3.11
conda create --name pyspice_env python=3.11 -y

# Activate the new environment
conda activate pyspice_env

# Upgrade pip to the latest version
pip install --upgrade pip

# Install all required packages from requirements.txt
pip install -r requirements.txt
```

**Important Notes for fastMCP:**
- Ensure you have Python 3.11 or higher.
- The `requirements.txt` file pins `fastmcp` to a stable version range to avoid compatibility issues.

**Step 3: Configure the LTSpice Executable Path**
Open `ltspice_mcp.py` and find the `LTSPICE_EXECUTABLE_PATH` variable. **You must update this** to point to the location of `LTspice.exe` inside your Wine C: drive.

A typical path on macOS with Wine is:
```python
# ltspice_mcp.py
LTSPICE_EXECUTABLE_PATH = "/Users/your_username/.wine/drive_c/Users/your_username/AppData/Local/Programs/ADI/LTspice/LTspice.exe"
```

**Step 4: Configure the Cursor MCP Server**
This is the most critical step to connect the AI to your tools.

1.  In Cursor, go to `File > Settings > Extensions > "Model Context Protocol (MCP)"`.
2.  Find the `Mcp: Json Path` setting and click "Edit in settings.json".
3.  Replace the contents of your `mcp.json` file with the following. **Make sure to replace `your_full_path_to` with the correct absolute paths on your machine.**

    ```json
    {
      "mcpServers": {
        "ltspice_mcp": {
          "command": "/your_full_path_to/miniconda3/envs/pyspice_env/bin/python",
          "args": [
            "/your_full_path_to/your-repo-name/ltspice_mcp.py"
          ],
          "workingDirectory": "/your_full_path_to/your-repo-name/"
        }
      }
    }
    ```
    *   **`command`**: The absolute path to the Python executable *inside your new Conda environment*.
    *   **`args`**: The absolute path to the `ltspice_mcp.py` script.
    *   **`workingDirectory`**: The absolute path to the project's root directory.

**Step 5: Restart Cursor**
After saving `mcp.json`, you **must restart Cursor** for the changes to take effect.

---

## Understanding the Output Files

Each simulation creates a timestamped folder inside `simulation_output/` (e.g., `20250703_143000/`) containing:

-   `circuit.net`: The plain text SPICE netlist that defines your circuit.
-   `circuit.log`: A log file from LTSpice containing details about the simulation run, solver settings, and any errors. Use the `read_simulation_log` tool to view this.
-   `circuit.raw`: The most important file—a binary file containing all the voltage and current data for every time step of your simulation.
-   `circuit.op.raw`: A small file containing the DC Operating Point (`.op`) data, which shows the initial state of the circuit before the transient analysis begins.
-   `plot_*.png`: The plot images generated by the AI.
-   `view.plt`: A temporary plot settings file created by the `view_results_in_ltspice` tool to reliably open the waveform viewer.
---

## Troubleshooting

### FastMCP Related Issues

-   **ImportError: No module named 'fastmcp'**: 
    - Ensure you're using the correct Python environment: `conda activate pyspice_env`
    - Reinstall fastmcp: `pip install --upgrade "fastmcp>=2.7.0,<3.0.0"`
    - Check Python version: `python --version` (should be 3.11+)

-   **FastMCP Version Compatibility Issues**:
    - The requirements.txt pins fastmcp to versions 2.7.0-2.99.99 for stability
    - If you encounter errors with specific fastmcp versions, try: `pip install fastmcp==2.9.2`

-   **MCP Server Shows '0 tools enabled' or Red Dot in Cursor**:
    - This usually indicates a Python environment issue
    - Verify the correct Python path in your mcp.json using: `which python` (with conda environment activated)
    - Ensure all dependencies are installed: `pip list | grep -E "(fastmcp|mcp|matplotlib|PyLTSpice)"`
    - Check for any import errors by running the server directly: `python ltspice_mcp.py`

### General Issues

-   **Tool Not Found Error**: If the AI says it can't find a tool (e.g., `read_simulation_log`), it almost always means you need to **restart Cursor** after editing `ltspice_mcp.py` or `mcp.json`.
-   **Files Disappearing from Output Folder**: If you notice files vanishing after you open and close them, this is likely an issue with your local editor or file system, not the script. The Python scripts in this project only have permission to create and write files, not delete them. Check for any aggressive file-watching or "auto-clean" features in your editor or third-party utilities.
-   **Simulation Fails**: If a simulation fails, ask the AI to read the log file: `"Please read the log file for the last simulation and tell me what went wrong."` This is the best way to debug.

### Environment Verification

To verify your setup is working correctly, run these commands in your activated conda environment:

```bash
# Check Python version
python --version

# Check if fastmcp is installed correctly
python -c "import fastmcp; print(f'FastMCP version: {fastmcp.__version__}')"

# Check if other dependencies are available
python -c "import matplotlib, spicelib; print('All dependencies imported successfully')"

# Test the MCP server directly
python ltspice_mcp.py --help
```

---

## Contact
- **Author:** Maanas Goel
- **Email:** maanasgoel5@gmail.com