# Picotool MCP Server

An MCP (Model Context Protocol) server that provides Claude Code with capabilities to interact with Raspberry Pi Pico devices (RP2040/RP2350) through the `picotool` command-line tool.

![MCP](https://img.shields.io/badge/MCP-Compatible-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- 🔍 **Device Information**: Query connected Pico devices for detailed hardware and firmware info
- 📁 **Binary Analysis**: Analyze UF2, ELF, and BIN files without flashing to device
- 🧩 **Pin Mapping**: Extract pin assignment information from firmware
- 🔄 **Device Reboot**: Reboot devices between application and BOOTSEL modes programmatically
- 🎯 **Device Selection**: Filter devices by USB bus, address, VID/PID, or serial number
- 🔧 **Version Checking**: Get picotool version information for troubleshooting
- 🏛️ **Multi-Architecture**: Support for ARM and RISC-V cores on RP2350 devices
- ⚡ **Fast Integration**: Built with `uv` for lightning-fast dependency management
- 🛡️ **Robust Error Handling**: Graceful handling of disconnected devices and file errors
- 📊 **Comprehensive Data**: Access to device info, build metadata, memory layout, and more

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** 
- **[uv](https://docs.astral.sh/uv/)** for dependency management
- **[picotool](https://github.com/raspberrypi/picotool)** installed and available in PATH

### Installation

```bash
# Clone the repository
git clone https://github.com/DavidMenting/picotool-mcp-server.git
cd picotool-mcp-server

# Install dependencies with uv
uv sync
```

### Claude Desktop Integration

Add this configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "picotool": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/picotool-mcp-server",
        "run",
        "python",
        "-m",
        "picotool_mcp_server"
      ]
    }
  }
}
```

> **Note**: Replace `/absolute/path/to/picotool-mcp-server` with the actual path to this repository.

### Standalone Usage

You can also run the server directly:

```bash
uv run python -m picotool_mcp_server
```

## 🛠️ Available Tools

### `picotool_info`

Get comprehensive information about connected Pico devices or analyze binary files. **Can automatically force running devices into BOOTSEL mode** - no physical button press required!

#### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `target` | string | File path to analyze, or empty for connected devices | `""` |
| `basic` | boolean | Include basic information | `true` |
| `metadata` | boolean | Include all metadata blocks | `false` |
| `pins` | boolean | Include pin information | `false` |
| `device` | boolean | Include device information | `false` |
| `debug` | boolean | Include device debug information | `false` |
| `build` | boolean | Include build attributes | `false` |
| `all` | boolean | Include all information | `false` |
| `force` | boolean | **Auto-reboot running device to BOOTSEL mode** (no physical button needed) | `false` |
| `force_no_reboot` | boolean | Force device reset but don't reboot back to application mode | `false` |
| `bus` | string | Filter devices by USB bus number | - |
| `address` | string | Filter devices by USB device address | - |
| `vid` | string | Filter by vendor ID | - |
| `pid` | string | Filter by product ID | - |
| `serial` | string | Filter by serial number | - |

#### Examples

**Auto-detect running device and get info (most common use case):**
```json
{
  "force": true,
  "all": true
}
```

**Get basic info from device already in BOOTSEL mode:**
```json
{
  "basic": true
}
```

**Get comprehensive device information:**
```json
{
  "all": true
}
```

**Analyze a firmware file:**
```json
{
  "target": "/path/to/firmware.uf2",
  "pins": true,
  "build": true
}
```

**Force a running device to provide info (useful for development):**
```json
{
  "force": true,
  "all": true
}
```

**Query a specific device by serial number:**
```json
{
  "serial": "20C110CE49017709",
  "device": true,
  "pins": true
}
```

#### Sample Output

```
Partition 1
 Program Information
  name:          my-project
  version:       1.0.0
  description:   My Pico Project
  features:      USB stdin / stdout
  target chip:   RP2350
  image type:    ARM Secure

 Fixed Pin Information
  0:             UART0 TX
  1:             UART0 RX
  2:             I2C0 SDA
  3:             I2C0 SCL

 Device Information
  type:          RP2350
  revision:      A2
  flash size:    16384K
  current cpu:   ARM
```

### `picotool_reboot`

Reboot connected Pico devices to application mode or BOOTSEL mode for development workflows.

#### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `all_devices` | boolean | Reboot all connected devices | `false` |
| `usb_mass_storage` | boolean | Reboot to USB mass storage mode (BOOTSEL) | `false` |
| `partition` | string | Reboot to a specific partition | - |
| `cpu` | string | Specify which CPU to boot (ARM/RISC-V for RP2350) | - |
| `force` | boolean | Force device not in BOOTSEL mode to reset | `false` |
| `force_no_reboot` | boolean | Force device reset but don't reboot back | `false` |
| `bus` | string | Filter devices by USB bus number | - |
| `address` | string | Filter devices by USB device address | - |
| `vid` | string | Filter by vendor ID | - |
| `pid` | string | Filter by product ID | - |
| `serial` | string | Filter by serial number | - |

#### Examples

**Reboot to BOOTSEL mode (for firmware flashing):**
```json
{
  "usb_mass_storage": true,
  "force": true
}
```

**Reboot back to application mode:**
```json
{}
```

**Reboot all connected devices:**
```json
{
  "all_devices": true
}
```

**Reboot to specific partition (RP2350):**
```json
{
  "partition": "1",
  "force": true
}
```

**Reboot with specific CPU (RP2350):**
```json
{
  "cpu": "RISC-V",
  "usb_mass_storage": true
}
```

### `picotool_version`

Get picotool version information for troubleshooting and diagnostics.

#### Parameters

This tool takes no parameters - it simply returns the installed picotool version.

#### Example

```json
{}
```

#### Sample Output

```
picotool v2.0.0 (d4c9a39)
```

## 📋 Supported Devices

- **RP2040**: Original Raspberry Pi Pico, Pico W, and compatible boards
- **RP2350**: Raspberry Pi Pico 2 and compatible RP2350-based boards

## 🔧 Development

### Setup Development Environment

```bash
# Install development dependencies
uv sync --dev

# Install pre-commit hooks (optional)
pre-commit install
```

### Code Quality

```bash
# Format code
uv run black .

# Lint code  
uv run ruff check .

# Type checking
uv run mypy src/
```

### Testing

```bash
# Run tests (when implemented)
uv run pytest

# Test the server manually
uv run python -c "
import asyncio
from src.picotool_mcp_server.picotool import PicotoolWrapper

async def test():
    picotool = PicotoolWrapper()
    version = await picotool.version()
    print(f'Picotool version: {version}')

asyncio.run(test())
"
```

## 🐛 Troubleshooting

### Common Issues

**Server fails to start:**
- Ensure `picotool` is installed and in your PATH
- Verify Python 3.10+ is being used
- Check that `uv` is installed

**No devices found:**
- Connect your Pico device in BOOTSEL mode (hold BOOTSEL while plugging in)
- Verify device appears in system (check USB device list)
- Try `picotool info` directly to confirm device detection

**Permission errors:**
- On Linux, you may need to add udev rules for the Pico device
- Ensure your user has permission to access USB devices

### Debug Logging

The server logs important events. Check Claude Desktop's MCP server logs:

**macOS**: `~/Library/Logs/Claude/mcp-server-picotool.log`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`uv run black . && uv run ruff check .`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- **[picotool](https://github.com/raspberrypi/picotool)**: The official Raspberry Pi Pico command-line tool
- **[MCP](https://modelcontextprotocol.io/)**: Model Context Protocol specification
- **[Claude Code](https://claude.ai/code)**: AI-powered code editor with MCP support

---

*Built with ❤️ for the Raspberry Pi Pico community*