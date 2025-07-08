# LTspice MCP Server - README

This guide explains how to set up, run, and use the `ltspice_mcp.py` MCP server for automating LTspice simulations via chatbox/IDE integration (e.g., Cursor, Claude) or direct tool calls.

---

## 1. Environment Setup

### **A. Python Environment**
For consistency and ease of use, we strongly recommend using a `conda` environment.

#### **Create and Activate a Conda Environment:**
1.  **Create the environment** (you only need to do this once):
    ```sh
    conda create -n pyspice_conda python=3.10
    ```
2.  **Activate the environment** (do this every time you open a new terminal for this project):
    ```sh
    conda activate pyspice_conda
    ```

### **B. Install Required Packages**
With your `pyspice_conda` environment active, install the necessary dependencies:
```sh
pip install matplotlib numpy PyLTSpice fastmcp
```

### **C. LTspice & Wine (for Mac/Linux users)**
- **LTspice** must be installed.
- Update the `LTSPICE_PATH` in `ltspice_mcp.py` to match your system.
  - **Example for Mac:**
    ```python
    LTSPICE_PATH = "wine /Users/youruser/.wine/drive_c/Users/youruser/AppData/Local/Programs/ADI/LTspice/LTspice.exe"
    ```

---

## 2. Running the MCP Server

1.  **Navigate to the folder:**
    ```sh
    cd /Users/maanasgoel/Documents/Cursor/PySpice/PyLTSpice/test
    ```
2.  **Activate your conda environment:**
    ```sh
    conda activate pyspice_conda
    ```
3.  **Run the server from your terminal:**
    ```sh
    python ltspice_mcp.py
    ```
    Leave this terminal running. **You do not need to run this command if you are using Cursor's MCP integration, as Cursor will run it for you.**

---

## 3. Registering the MCP Server in Your Chatbox/IDE

### **A. In Cursor**
Go to Settings → MCP Servers (or use the command palette). You can add the server via the UI or by editing your `.cursor/mcp.json` file directly.

### **B. Editing `mcp.json` Directly (Recommended)**
Open your `.cursor/mcp.json` file and add a new entry under `"mcpServers"`.
**Do not delete your existing servers—just add a new one.**

**Important:** The `"command"` must be the **full, absolute path** to the Python executable inside your conda environment.

1.  **Find the path:** While your `pyspice_conda` environment is active, run `which python`.
2.  **Use that path** in the `command` field as shown below.

**Example `mcp.json` entry:**
```json
{
  "mcpServers": {
    "filesystem": {
      // ... existing filesystem server ...
    },
    "ltspice": {
      "command": "/Users/maanasgoel/miniconda3/envs/pyspice_conda/bin/python", // <-- Use the full path from `which python`
      "args": [
        "/Users/maanasgoel/Documents/Cursor/PySpice/PyLTSpice/test/ltspice_mcp.py"
      ],
      "cwd": "/Users/maanasgoel/Documents/Cursor/PySpice/PyLTSpice/test",
      "transport": "stdio"
    }
  }
}
```
After saving, **fully quit and restart Cursor**. Your LTspice MCP server should now appear with a **green dot** and the correct number of tools enabled.

---

## 4. Available MCP Tools & Functions

### **1. set_netlist**
- **Purpose:** Set (overwrite) the SPICE netlist file.
- **Arguments:**
  - `netlist_string` (str, required): The SPICE netlist as a string.
  - `netlist_path` (str, optional): File path to save the netlist (default: `rc_circuit.net`).
- **Returns:** Status and message.

### **2. validate_netlist**
- **Purpose:** Basic validation of the netlist (checks for `.end` and at least one voltage source).
- **Arguments:**
  - `netlist_path` (str, optional): Path to the netlist file.
- **Returns:** Status and validation message.

### **3. run_simulation**
- **Purpose:** Run LTspice simulation on the specified netlist.
- **Arguments:**
  - `netlist_path` (str, optional): Path to the netlist file.
  - `output_dir` (str, optional): Directory to store simulation output.
- **Returns:** Status, .raw file path, simulation time, and message.

### **4. list_traces**
- **Purpose:** List available traces in the .raw file.
- **Arguments:**
  - `output_dir` (str, optional): Directory containing the .raw file.
- **Returns:** Status and list of trace names.

### **5. get_raw_data**
- **Purpose:** Get all simulation results as JSON/dict.
- **Arguments:**
  - `output_dir` (str, optional): Directory containing the .raw file.
- **Returns:** Status, traces, and trace names.

### **6. get_plot**
- **Purpose:** Get a plot of any traces as a base64 PNG image (optionally save to file).
- **Arguments:**
  - `traces` (list, optional): List of trace names to plot (default: ["V(out)", "V(in)"] if available).
  - `output_dir` (str, optional): Directory containing the .raw file.
  - `save_to_file` (bool, optional): If True, save the plot as a PNG in output_dir.
  - `plot_filename` (str, optional): Name of the plot file to save.
- **Returns:** Status, image_base64, and/or plot file path.

### **7. clear_output**
- **Purpose:** Delete all .raw files in the output directory.
- **Arguments:**
  - `output_dir` (str, optional): Directory to clear .raw files from.
- **Returns:** Status and message.

---

## 5. Example Usage Scenarios

See the 10 example tool calls in the main README or previous message. Here are a few:

- **Set a netlist:**
  > Set the following netlist as my circuit:
  > ```
  > * RC Circuit
  > V1 in 0 DC 5
  > R1 in out 1k
  > C1 out 0 1u
  > .tran 0 0.01 0 0.0001
  > .end
  > ```
- **Validate netlist:**
  > Is my current netlist valid?
- **Run simulation:**
  > Run the simulation on the current netlist.
- **List traces:**
  > What traces are available in the simulation output?
- **Get plot:**
  > Show me a plot of V(out) and V(in).

(See the main README or ask your chatbox for more examples.)

---

## 6. Troubleshooting & FAQ

- **Q: I get a Wine/LTspice error.**
  - A: Make sure Wine and LTspice are installed and the `LTSPICE_PATH` is correct.
- **Q: No .raw file found after simulation.**
  - A: Check your netlist for errors (use `validate_netlist`).
- **Q: My chatbox can't find the MCP server.**
  - A: Make sure the server is running and the path is correct in your chatbox settings.
- **Q: My `ltspice` MCP server shows '0 tools enabled' or has a red dot in Cursor.**
  - **A:** This is the most common issue. It means Cursor is not using your activated Python environment (e.g., `conda` or `venv`). You must provide the **full, absolute path** to the Python executable in your `.cursor/mcp.json` file.

    1. **Find the Python path:** Activate your environment in a terminal (`conda activate pyspice`) and run `which python`.
    2. **Update `mcp.json`:** Use that full path in the `command` field.

    ```json
    "ltspice": {
      "command": "/Users/maanasgoel/miniconda3/envs/pyspice/bin/python", // <-- Use the full path from `which python`
      "args": [
        "/Users/maanasgoel/Documents/Cursor/PySpice/PyLTSpice/test/ltspice_mcp.py"
      ],
      "cwd": "/Users/maanasgoel/Documents/Cursor/PySpice/PyLTSpice/test"
    }
    ```
    3. **Restart Cursor:** Fully quit and restart Cursor for the changes to take effect.
- **Q: How do I see available tools?**
  - A: Ask your chatbox "What tools are available?" or check this README.

---

## 7. Platform-Specific Notes

- **Mac/Linux:**
  - LTspice runs via Wine. Install Wine and LTspice, and update the path in the script.
- **Windows:**
  - You can use the native LTspice executable. Update the path accordingly.

---

## 8. Contact & Support

For further help, contact your project maintainer or ask in your chatbox/IDE.

---

## 9. Author

Author: Maanas Goel  
Email: maanasgoel@gmail.com  
GitHub: https://github.com/maanas-goel

---

Happy simulating!

## 10. Using a Local Chatbox to Create and Simulate a Netlist

You can use a local chatbox (like Cursor, Claude, or any MCP-enabled chatbox) to write your circuit description in plain English. The chatbox can then help you convert your description into a valid SPICE netlist, and automatically send it to the MCP server using the `set_netlist` tool.

### **Step-by-Step Workflow:**

1. **Write your circuit in plain English in the chatbox.**
   - Example: "I want a simple RC circuit with a 5V DC source, a 1k resistor, and a 1uF capacitor."
2. **Ask the chatbox to generate a SPICE netlist for your description.**
   - Example prompt: "Convert this description to a SPICE netlist."
3. **The chatbox generates the netlist and uses the `set_netlist` tool to send it to the MCP server.**
4. **You can then ask the chatbox to run the simulation, plot results, or analyze data using the other MCP tools.**

### **Example Chatbox Conversation:**

**You:**
> I want a simple RC circuit with a 5V DC source, a 1k resistor, and a 1uF capacitor. Simulate its transient response.

**Chatbox:**
> Here is the SPICE netlist for your circuit:
> ```
> * RC Circuit
> V1 in 0 DC 5
> R1 in out 1k
> C1 out 0 1u
> .tran 0 0.01 0 0.0001
> .end
> ```
> I will now set this netlist and run the simulation.

*(The chatbox calls `set_netlist` with the generated netlist, then calls `run_simulation`, and can show you the plot with `get_plot`.)*

### **Summary:**
- You describe your circuit in plain English.
- The chatbox converts it to a SPICE netlist.
- The chatbox sends the netlist to the MCP server and runs the simulation for you.
- You can view results, plots, and data—all from your chatbox! 