import os
import sys
import subprocess
import datetime
import logging

# --- Basic Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# This is the netlist for the RC circuit.
# The PULSE source is critical for a correct transient analysis.
NETLIST_TEXT = """
* Simple RC Circuit Demo
V1 Vin 0 PULSE(0 5 0 1ns 1ns 5ms 10ms)
R1 Vin Vout 1k
C1 Vout 0 1uF
.tran 5m
.end
"""

# --- Environment Configuration ---
# These paths MUST be correct for your system.
LTSPICE_EXECUTABLE_PATH = "/Users/maanasgoel/.wine/drive_c/users/maanasgoel/AppData/Local/Programs/ADI/LTspice/LTCspice.exe"
WINE_COMMAND = "wine"
BASE_OUTPUT_DIR = os.path.abspath("output")

def main():
    """
    Main function to run the LTspice simulation.
    """
    # 1. Setup Session Directory
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = os.path.join(BASE_OUTPUT_DIR, f"rc_circuit_{timestamp}")
        os.makedirs(session_dir, exist_ok=True)
        logging.info(f"Created output session directory: {session_dir}")
    except Exception as e:
        logging.error(f"Fatal: Could not create session directory. Error: {e}")
        sys.exit(1)

    # 2. Write the Netlist File
    netlist_path = os.path.join(session_dir, "circuit.net")
    try:
        with open(netlist_path, "w") as f:
            f.write(NETLIST_TEXT)
        logging.info(f"Netlist written to {netlist_path}")
    except Exception as e:
        logging.error(f"Fatal: Could not write netlist file. Error: {e}")
        sys.exit(1)

    # 3. Run the Simulation
    raw_file_path = os.path.join(session_dir, "circuit.raw")
    log_file_path = os.path.join(session_dir, "circuit.log")
    try:
        cmd = [WINE_COMMAND, LTSPICE_EXECUTABLE_PATH, "-b", os.path.abspath(netlist_path)]
        logging.info(f"Executing simulation command: {' '.join(cmd)}")
        
        process = subprocess.run(
            cmd,
            cwd=session_dir,  # Critical: Run from the session directory
            capture_output=True,
            text=True,
            check=False
        )

        if process.returncode != 0 or not os.path.exists(raw_file_path):
            log_content = ""
            if os.path.exists(log_file_path):
                with open(log_file_path, 'r') as f:
                    log_content = f.read()
            logging.error(f"--- SIMULATION FAILED ---")
            logging.error(f"Return Code: {process.returncode}")
            logging.error(f"STDOUT: {process.stdout}")
            logging.error(f"STDERR: {process.stderr}")
            logging.error(f"Log File Content:\n{log_content}")
            sys.exit(1)

        logging.info(f"Simulation successful. Raw data at: {raw_file_path}")

    except Exception as e:
        logging.error(f"Fatal: An exception occurred during simulation. Error: {e}")
        sys.exit(1)
        
    # 4. Plot the results using spicelib (if available)
    try:
        from spicelib.raw.raw_read import RawRead
        import matplotlib.pyplot as plt

        raw_reader = RawRead(raw_file_path)
        time_trace = raw_reader.get_trace('time')
        vin_trace = raw_reader.get_trace('V(vin)')
        vout_trace = raw_reader.get_trace('V(vout)')

        x = time_trace.get_wave()
        y_vin = vin_trace.get_wave()
        y_vout = vout_trace.get_wave()
        
        plt.figure(figsize=(12, 7))
        plt.plot(x, y_vin, label="V(in)")
        plt.plot(x, y_vout, label="V(out)")
        plt.title("RC Circuit Transient Analysis")
        plt.xlabel("Time (s)")
        plt.ylabel("Voltage (V)")
        plt.grid(True)
        plt.legend()
        
        plot_path = os.path.join(session_dir, "rc_plot.png")
        plt.savefig(plot_path)
        logging.info(f"Plot saved to: {plot_path}")

    except ImportError:
        logging.warning("Skipping plot generation: 'spicelib' or 'matplotlib' not found.")
    except Exception as e:
        logging.error(f"Could not generate plot. Error: {e}")


    print("\n--- ✅ SIMULATION COMPLETE ---")
    print(f"All output files have been saved in:")
    print(f"{session_dir}")
    print("---------------------------------")


if __name__ == "__main__":
    # Check for wine command
    if subprocess.run(['which', WINE_COMMAND], capture_output=True).returncode != 0:
        logging.error(f"'{WINE_COMMAND}' command not found. Wine must be installed and in your PATH.")
        sys.exit(1)
    # Check for LTspice executable
    if not os.path.exists(LTSPICE_EXECUTABLE_PATH):
        logging.error(f"LTspice executable not found at: {LTSPICE_EXECUTABLE_PATH}")
        sys.exit(1)
        
    main() 