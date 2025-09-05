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
            description="Get information about connected Pico devices or binary files. Can force running devices into BOOTSEL mode automatically.",
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
                    },
                    "force": {
                        "type": "boolean",
                        "description": "Force running device to reboot into BOOTSEL mode automatically (no physical button needed)",
                        "default": False
                    },
                    "force_no_reboot": {
                        "type": "boolean", 
                        "description": "Force device reset but don't reboot back to application mode",
                        "default": False
                    },
                    "bus": {
                        "type": "string",
                        "description": "Filter devices by USB bus number"
                    },
                    "address": {
                        "type": "string", 
                        "description": "Filter devices by USB device address"
                    },
                    "vid": {
                        "type": "string",
                        "description": "Filter by vendor ID"
                    },
                    "pid": {
                        "type": "string",
                        "description": "Filter by product ID" 
                    },
                    "serial": {
                        "type": "string",
                        "description": "Filter by serial number"
                    }
                },
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="picotool_reboot",
            description="Reboot connected Pico devices to application or BOOTSEL mode",
            inputSchema={
                "type": "object",
                "properties": {
                    "all_devices": {
                        "type": "boolean",
                        "description": "Reboot all connected devices",
                        "default": False
                    },
                    "usb_mass_storage": {
                        "type": "boolean",
                        "description": "Reboot to USB mass storage mode (BOOTSEL)",
                        "default": False
                    },
                    "partition": {
                        "type": "string",
                        "description": "Reboot to a specific partition"
                    },
                    "cpu": {
                        "type": "string",
                        "description": "Specify which CPU to boot (ARM/RISC-V for RP2350)",
                        "enum": ["ARM", "RISC-V"]
                    },
                    "force": {
                        "type": "boolean",
                        "description": "Force device not in BOOTSEL mode to reset",
                        "default": False
                    },
                    "force_no_reboot": {
                        "type": "boolean",
                        "description": "Force device reset but don't reboot back",
                        "default": False
                    },
                    "bus": {
                        "type": "string",
                        "description": "Filter devices by USB bus number"
                    },
                    "address": {
                        "type": "string",
                        "description": "Filter devices by USB device address"
                    },
                    "vid": {
                        "type": "string",
                        "description": "Filter by vendor ID"
                    },
                    "pid": {
                        "type": "string",
                        "description": "Filter by product ID"
                    },
                    "serial": {
                        "type": "string",
                        "description": "Filter by serial number"
                    }
                },
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="picotool_version",
            description="Get picotool version information for troubleshooting and diagnostics",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="picotool_partition_info",
            description="Get partition table information from RP2350 devices (RP2040 devices don't have partition tables)",
            inputSchema={
                "type": "object",
                "properties": {
                    "family_id": {
                        "type": "string",
                        "description": "Target family ID to show partition for (e.g. 'rp2350-arm-s', 'rp2350-riscv')"
                    },
                    "force": {
                        "type": "boolean",
                        "description": "Force device not in BOOTSEL mode to reset",
                        "default": False
                    },
                    "force_no_reboot": {
                        "type": "boolean",
                        "description": "Force device reset but don't reboot back",
                        "default": False
                    },
                    "bus": {
                        "type": "string",
                        "description": "Filter devices by USB bus number"
                    },
                    "address": {
                        "type": "string",
                        "description": "Filter devices by USB device address"
                    },
                    "vid": {
                        "type": "string",
                        "description": "Filter by vendor ID"
                    },
                    "pid": {
                        "type": "string",
                        "description": "Filter by product ID"
                    },
                    "serial": {
                        "type": "string",
                        "description": "Filter by serial number"
                    }
                },
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="picotool_erase",
            description="Erase flash memory on connected Pico devices. CAUTION: This operation is destructive and will permanently delete data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "all_flash": {
                        "type": "boolean",
                        "description": "Erase all flash memory on the device",
                        "default": False
                    },
                    "sector": {
                        "type": "string",
                        "description": "Erase specific sector (hex address, e.g. '0x10000000')"
                    },
                    "range_start": {
                        "type": "string",
                        "description": "Start address for range erase (hex, e.g. '0x10000000')"
                    },
                    "range_end": {
                        "type": "string",
                        "description": "End address for range erase (hex, e.g. '0x10100000')"
                    },
                    "force": {
                        "type": "boolean",
                        "description": "Force device not in BOOTSEL mode to reset",
                        "default": False
                    },
                    "force_no_reboot": {
                        "type": "boolean",
                        "description": "Force device reset but don't reboot back",
                        "default": False
                    },
                    "bus": {
                        "type": "string",
                        "description": "Filter devices by USB bus number"
                    },
                    "address": {
                        "type": "string",
                        "description": "Filter devices by USB device address"
                    },
                    "vid": {
                        "type": "string",
                        "description": "Filter by vendor ID"
                    },
                    "pid": {
                        "type": "string",
                        "description": "Filter by product ID"
                    },
                    "serial": {
                        "type": "string",
                        "description": "Filter by serial number"
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
            force = arguments.get("force", False)
            force_no_reboot = arguments.get("force_no_reboot", False)
            bus = arguments.get("bus")
            address = arguments.get("address")
            vid = arguments.get("vid") 
            pid = arguments.get("pid")
            serial = arguments.get("serial")
            
            logger.info(f"Running picotool info with target='{target}', options={arguments}")
            
            result = await picotool.info(
                target=target,
                basic=basic,
                metadata=metadata,
                pins=pins,
                device=device,
                debug=debug,
                build=build,
                all=all_info,
                force=force,
                force_no_reboot=force_no_reboot,
                bus=bus,
                address=address,
                vid=vid,
                pid=pid,
                serial=serial
            )
            
            return [types.TextContent(type="text", text=result)]
            
        except Exception as e:
            error_msg = f"Error running picotool info: {str(e)}"
            logger.error(error_msg)
            return [types.TextContent(type="text", text=error_msg)]
    
    elif name == "picotool_reboot":
        try:
            all_devices = arguments.get("all_devices", False)
            usb_mass_storage = arguments.get("usb_mass_storage", False)
            partition = arguments.get("partition")
            cpu = arguments.get("cpu")
            force = arguments.get("force", False)
            force_no_reboot = arguments.get("force_no_reboot", False)
            bus = arguments.get("bus")
            address = arguments.get("address")
            vid = arguments.get("vid")
            pid = arguments.get("pid")
            serial = arguments.get("serial")
            
            logger.info(f"Running picotool reboot with options={arguments}")
            
            result = await picotool.reboot(
                all_devices=all_devices,
                usb_mass_storage=usb_mass_storage,
                partition=partition,
                cpu=cpu,
                force=force,
                force_no_reboot=force_no_reboot,
                bus=bus,
                address=address,
                vid=vid,
                pid=pid,
                serial=serial
            )
            
            return [types.TextContent(type="text", text=result)]
            
        except Exception as e:
            error_msg = f"Error running picotool reboot: {str(e)}"
            logger.error(error_msg)
            return [types.TextContent(type="text", text=error_msg)]
    
    elif name == "picotool_version":
        try:
            logger.info("Running picotool version")
            
            result = await picotool.version()
            
            return [types.TextContent(type="text", text=result)]
            
        except Exception as e:
            error_msg = f"Error running picotool version: {str(e)}"
            logger.error(error_msg)
            return [types.TextContent(type="text", text=error_msg)]
    
    elif name == "picotool_partition_info":
        try:
            family_id = arguments.get("family_id")
            force = arguments.get("force", False)
            force_no_reboot = arguments.get("force_no_reboot", False)
            bus = arguments.get("bus")
            address = arguments.get("address")
            vid = arguments.get("vid")
            pid = arguments.get("pid")
            serial = arguments.get("serial")
            
            logger.info(f"Running picotool partition info with options={arguments}")
            
            result = await picotool.partition_info(
                family_id=family_id,
                force=force,
                force_no_reboot=force_no_reboot,
                bus=bus,
                address=address,
                vid=vid,
                pid=pid,
                serial=serial
            )
            
            return [types.TextContent(type="text", text=result)]
            
        except Exception as e:
            error_msg = f"Error running picotool partition info: {str(e)}"
            logger.error(error_msg)
            return [types.TextContent(type="text", text=error_msg)]
    
    elif name == "picotool_erase":
        try:
            all_flash = arguments.get("all_flash", False)
            sector = arguments.get("sector")
            range_start = arguments.get("range_start")
            range_end = arguments.get("range_end")
            force = arguments.get("force", False)
            force_no_reboot = arguments.get("force_no_reboot", False)
            bus = arguments.get("bus")
            address = arguments.get("address")
            vid = arguments.get("vid")
            pid = arguments.get("pid")
            serial = arguments.get("serial")
            
            logger.info(f"Running picotool erase with options={arguments}")
            
            result = await picotool.erase(
                all_flash=all_flash,
                sector=sector,
                range_start=range_start,
                range_end=range_end,
                force=force,
                force_no_reboot=force_no_reboot,
                bus=bus,
                address=address,
                vid=vid,
                pid=pid,
                serial=serial
            )
            
            return [types.TextContent(type="text", text=result)]
            
        except Exception as e:
            error_msg = f"Error running picotool erase: {str(e)}"
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