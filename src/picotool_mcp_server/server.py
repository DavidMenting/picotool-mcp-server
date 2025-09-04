"""Main MCP server implementation for picotool."""

import asyncio
import logging
from typing import Any, Sequence

from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from .picotool import PicotoolWrapper

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("picotool-mcp-server")

# Initialize the MCP server
app = Server("picotool-mcp-server")

# Initialize picotool wrapper
picotool = PicotoolWrapper()


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="picotool_info",
            description="Get information about connected Pico devices or binary files",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "File path to analyze, or empty string for connected devices",
                        "default": ""
                    },
                    "basic": {
                        "type": "boolean", 
                        "description": "Include basic information",
                        "default": True
                    },
                    "metadata": {
                        "type": "boolean",
                        "description": "Include all metadata blocks", 
                        "default": False
                    },
                    "pins": {
                        "type": "boolean",
                        "description": "Include pin information",
                        "default": False
                    },
                    "device": {
                        "type": "boolean",
                        "description": "Include device information",
                        "default": False
                    },
                    "debug": {
                        "type": "boolean",
                        "description": "Include device debug information",
                        "default": False
                    },
                    "build": {
                        "type": "boolean",
                        "description": "Include build attributes",
                        "default": False
                    },
                    "all": {
                        "type": "boolean",
                        "description": "Include all information",
                        "default": False
                    }
                },
                "additionalProperties": False
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> Sequence[types.TextContent]:
    """Handle tool calls."""
    if arguments is None:
        arguments = {}
    
    if name == "picotool_info":
        try:
            target = arguments.get("target", "")
            basic = arguments.get("basic", True)
            metadata = arguments.get("metadata", False)
            pins = arguments.get("pins", False)
            device = arguments.get("device", False)
            debug = arguments.get("debug", False)
            build = arguments.get("build", False)
            all_info = arguments.get("all", False)
            
            logger.info(f"Running picotool info with target='{target}', options={arguments}")
            
            result = await picotool.info(
                target=target,
                basic=basic,
                metadata=metadata,
                pins=pins,
                device=device,
                debug=debug,
                build=build,
                all=all_info
            )
            
            return [types.TextContent(type="text", text=result)]
            
        except Exception as e:
            error_msg = f"Error running picotool info: {str(e)}"
            logger.error(error_msg)
            return [types.TextContent(type="text", text=error_msg)]
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())