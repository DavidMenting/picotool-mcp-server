# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that provides Claude Code with capabilities to interact with Raspberry Pi Pico devices (RP2040/RP2350) through the `picotool` command-line tool. The server acts as a bridge between Claude Code and picotool, enabling firmware development workflows, device management, and debugging operations.

## Architecture

The MCP server will expose picotool's functionality through structured MCP tools, allowing Claude Code to:

- Query device information (`picotool info`)
- Load firmware onto devices (`picotool load`)
- Save firmware from devices (`picotool save`)
- Configure device settings (`picotool config`)
- Manage OTP memory on RP2350 devices (`picotool otp`)
- Handle UF2 file operations (`picotool uf2`)
- Work with partition tables on RP2350 (`picotool partition`)
- Perform cryptographic operations (`picotool seal`, `picotool encrypt`)

## Key Dependencies

- **picotool**: The underlying CLI tool for RP2040/RP2350 device interaction
- **MCP SDK**: For implementing the Model Context Protocol server

## picotool Integration

The MCP server will wrap these key picotool commands:

### Device Information
- `picotool info` - Get device/binary information
- `picotool version` - Check picotool version

### Firmware Operations  
- `picotool load <file>` - Flash firmware to device
- `picotool save <file>` - Backup firmware from device
- `picotool verify <file>` - Verify device contents match file
- `picotool erase` - Erase device flash

### Device Management
- `picotool config` - Read/write device configuration
- `picotool reboot` - Reboot device

### RP2350 Specific Features
- `picotool otp` - OTP memory operations
- `picotool partition` - Partition table management
- `picotool seal` - Binary signing and sealing
- `picotool encrypt` - Binary encryption

### File Operations
- `picotool uf2 convert` - Convert ELF/BIN to UF2
- `picotool uf2 info` - UF2 file information

## Error Handling

The MCP server should handle common picotool error scenarios:
- No device connected
- Device not in BOOTSEL mode
- File format issues
- Permission problems
- OTP write protection

## Security Considerations

- OTP operations are destructive and irreversible
- Secure boot operations require careful key management
- Device selection should be explicit to avoid accidental operations