import asyncio
import json
import logging
import sys

# Set up logging to a file to not interfere with stdio
logging.basicConfig(filename="mcp_test.log", filemode="w", level=logging.INFO)

try:
    from mcp.server import stdio_server
    from mcp.types import Tool, CallToolRequest, CallToolResult, TextContent
except ImportError:
    logging.error("MCP library not found. Please ensure it's installed in the pyspice_conda environment.")
    sys.exit(1)

async def hello_handler(req: CallToolRequest) -> CallToolResult:
    """A very simple handler that returns a success message."""
    logging.info(f"Hello handler called with arguments: {req.arguments}")
    name = req.arguments.get("name", "World")
    response = {"message": f"Hello, {name}!"}
    return CallToolResult(contents=[TextContent(text=json.dumps(response))])

# Define a single, simple tool.
HELLO_TOOL = [
    Tool(
        name="hello",
        description="A simple tool that returns a greeting.",
        input_schema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The name to greet."}
            },
        },
        handler=hello_handler,
    )
]

async def main():
    logging.info("Starting minimal MCP server...")
    await stdio_server(name="mcp-test-server", version="1.0.0", tools=HELLO_TOOL)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.critical(f"Minimal server crashed: {e}", exc_info=True) 