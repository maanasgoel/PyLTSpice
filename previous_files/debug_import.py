import sys
print("--- Attempting to import FastMCP ---")
try:
    from fastmcp import FastMCP
    print("--- Successfully imported FastMCP ---")
    print(f"FastMCP location: {FastMCP.__file__}")
except ImportError as e:
    print(f"--- FAILED to import FastMCP ---")
    print(f"Error: {e}")
    print("\nPython Path:")
    import pprint
    pprint.pprint(sys.path) 