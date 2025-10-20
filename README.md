# Modbus TCP MCP Server

A comprehensive Model Context Protocol (MCP) server for interacting with Modbus TCP devices. This server enables LLMs to connect to, read from, and write to industrial Modbus TCP devices.

## Features

- **Connection Management**: Establish and maintain connections to Modbus TCP devices
- **Read Operations**: Read holding registers, input registers, coils, and discrete inputs
- **Write Operations**: Write single or multiple registers/coils
- **Data Type Support**: Support for uint16, int16, uint32, int32, float32, and bool
- **Device Information**: Query device identification (if supported)
- **Diagnostics**: Run comprehensive diagnostic tests
- **Connection Pooling**: Efficient connection reuse
- **Error Handling**: Clear, actionable error messages

## Installation

### Requirements

- Python 3.8 or higher
- MCP Python SDK
- pymodbus library

### Install Dependencies

```bash
pip install mcp pymodbus --break-system-packages
```

Or if you're using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install mcp pymodbus
```

## Usage

### Running the Server

```bash
python modbus_tcp_mcp.py
```

The server runs as a stdio-based MCP server and waits for requests from MCP clients.

### Configuring with Claude Desktop

Add this to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "modbus_tcp": {
      "command": "python",
      "args": ["/path/to/modbus_tcp_mcp.py"]
    }
  }
}
```

## Available Tools

### 1. modbus_connect
Connect to a Modbus TCP device.

**Parameters**:
- `host` (str): IP address or hostname (e.g., "192.168.1.100")
- `port` (int, optional): TCP port (default: 502)
- `timeout` (float, optional): Connection timeout in seconds (default: 10.0)
- `unit_id` (int, optional): Modbus slave/unit ID (default: 1)

**Example**:
```
Connect to PLC at 192.168.1.50
```

### 2. modbus_read_registers
Read values from Modbus registers or coils.

**Parameters**:
- `host` (str): Device IP address
- `register_type` (str): "holding", "input", "coil", or "discrete"
- `start_address` (int): Starting register address (0-based)
- `count` (int): Number of registers to read
- `data_type` (str, optional): "uint16", "int16", "uint32", "int32", "float32", "bool" (default: "uint16")
- `port` (int, optional): TCP port (default: 502)
- `unit_id` (int, optional): Slave ID (default: 1)
- `response_format` (str, optional): "markdown" or "json" (default: "markdown")

**Example**:
```
Read holding registers 100-105 from PLC at 192.168.1.50 as float32
```

### 3. modbus_write_register
Write a value to a single Modbus register or coil.

**Parameters**:
- `host` (str): Device IP address
- `address` (int): Register address to write
- `value` (int/float/bool): Value to write
- `register_type` (str, optional): "holding" or "coil" (default: "holding")
- `data_type` (str, optional): Data type for encoding (default: "uint16")
- `port` (int, optional): TCP port (default: 502)
- `unit_id` (int, optional): Slave ID (default: 1)
- `response_format` (str, optional): "markdown" or "json" (default: "markdown")

**Example**:
```
Write 1500 to holding register 100 on PLC at 192.168.1.50
```

### 4. modbus_write_multiple_registers
Write values to multiple consecutive registers or coils.

**Parameters**:
- `host` (str): Device IP address
- `start_address` (int): Starting register address
- `values` (list): List of values to write
- `register_type` (str, optional): "holding" or "coil" (default: "holding")
- `data_type` (str, optional): Data type for encoding (default: "uint16")
- `port` (int, optional): TCP port (default: 502)
- `unit_id` (int, optional): Slave ID (default: 1)
- `response_format` (str, optional): Output format (default: "markdown")

**Example**:
```
Write values [100, 200, 300] to holding registers 40-42 on device 192.168.1.50
```

### 5. modbus_device_info
Query device identification information.

**Parameters**:
- `host` (str): Device IP address
- `port` (int, optional): TCP port (default: 502)
- `unit_id` (int, optional): Slave ID (default: 1)
- `response_format` (str, optional): Output format (default: "markdown")

**Example**:
```
Get device information from PLC at 192.168.1.50
```

### 6. modbus_diagnostics
Run diagnostic tests on the device.

**Parameters**:
- `host` (str): Device IP address
- `port` (int, optional): TCP port (default: 502)
- `unit_id` (int, optional): Slave ID (default: 1)
- `test_read` (bool, optional): Perform test read (default: True)
- `response_format` (str, optional): Output format (default: "markdown")

**Example**:
```
Run diagnostics on Modbus device at 192.168.1.50
```

### 7. modbus_disconnect
Close connection to a device.

**Parameters**:
- `host` (str): Device IP address
- `port` (int, optional): TCP port (default: 502)

**Example**:
```
Disconnect from PLC at 192.168.1.50
```

## Register Types

### Holding Registers (Function Code 3/6/16)
- **Access**: Read/Write
- **Size**: 16-bit (2 bytes)
- **Use**: General-purpose data storage, configuration, setpoints

### Input Registers (Function Code 4)
- **Access**: Read-only
- **Size**: 16-bit (2 bytes)
- **Use**: Sensor readings, analog inputs, status data

### Coils (Function Code 1/5/15)
- **Access**: Read/Write
- **Size**: 1-bit (boolean)
- **Use**: Digital outputs, control signals, binary flags

### Discrete Inputs (Function Code 2)
- **Access**: Read-only
- **Size**: 1-bit (boolean)
- **Use**: Digital inputs, switches, binary sensors

## Data Types

| Type | Size | Range | Description |
|------|------|-------|-------------|
| `uint16` | 1 register | 0 to 65535 | Unsigned 16-bit integer |
| `int16` | 1 register | -32768 to 32767 | Signed 16-bit integer |
| `uint32` | 2 registers | 0 to 4294967295 | Unsigned 32-bit integer |
| `int32` | 2 registers | -2147483648 to 2147483647 | Signed 32-bit integer |
| `float32` | 2 registers | ±3.4e±38 | IEEE 754 floating-point |
| `bool` | 1 register/coil | True/False | Boolean value |

## Addressing

This server uses **0-based addressing** (protocol addressing):
- Register 0 = Address 0
- Register 1 = Address 1
- etc.

If your device documentation uses 1-based addressing or offset addressing (e.g., 40001-49999 for holding registers), subtract the offset:
- Holding register 40001 → Address 0
- Input register 30001 → Address 0
- Coil 00001 → Address 0

## Examples

### Example 1: Read Temperature Sensor
```
Read input register 100 from device 192.168.1.50 as float32
```

### Example 2: Control Relay
```
Write True to coil 5 on device 192.168.1.50
```

### Example 3: Read Multiple Values
```
Read holding registers 0-9 from PLC at 192.168.1.100
```

### Example 4: Write Configuration
```
Write values [1000, 2000, 3000, 4000, 5000] to holding registers 200-204 on device 192.168.1.50
```

### Example 5: Device Diagnostics
```
Run diagnostics on device 192.168.1.50 to check connectivity and response time
```

## Error Handling

The server provides clear, actionable error messages:

- **Connection Failed**: Check IP address, port, and network connectivity
- **Invalid Register Address**: Verify address is within device range
- **Modbus Exception**: Device-specific error, check device documentation
- **Timeout**: Device not responding, check device status
- **Read-only Register**: Cannot write to input/discrete registers

## Best Practices

1. **Test Connectivity First**: Use `modbus_connect` before other operations
2. **Use Appropriate Data Types**: Match data types to your device's configuration
3. **Handle Large Reads**: Read registers in chunks if needed (max 125 for registers)
4. **Close Connections**: Use `modbus_disconnect` when done to free resources
5. **Run Diagnostics**: Use `modbus_diagnostics` to troubleshoot issues

## Troubleshooting

### Connection Timeout
- Verify the device IP address and port
- Check network connectivity (ping the device)
- Ensure Modbus TCP service is running on the device
- Check firewall rules

### Invalid Address
- Verify the address range supported by your device
- Check if using 0-based or 1-based addressing
- Consult device documentation for valid register ranges

### Permission Denied
- Some registers may be read-only
- Check device security settings
- Verify user permissions on the device

### Data Type Mismatch
- Ensure data type matches device configuration
- 32-bit values require 2 consecutive registers
- Use appropriate byte order (big-endian by default)

## Technical Details

- **Protocol**: Modbus TCP (IEEE standard)
- **Default Port**: 502
- **Transport**: TCP/IP
- **Function Codes Supported**:
  - FC1: Read Coils
  - FC2: Read Discrete Inputs
  - FC3: Read Holding Registers
  - FC4: Read Input Registers
  - FC5: Write Single Coil
  - FC6: Write Single Register
  - FC15: Write Multiple Coils
  - FC16: Write Multiple Registers
  - FC43: Read Device Identification (if supported)

## License

This MCP server is provided as-is for use with industrial Modbus TCP devices.

## Support

For issues or questions:
1. Check device documentation for supported features
2. Verify network connectivity and device configuration
3. Use `modbus_diagnostics` tool for troubleshooting
4. Review error messages for specific guidance

## Safety Warning

⚠️ **CAUTION**: This tool can write to industrial equipment. Always:
- Test on non-critical systems first
- Understand the implications of register writes
- Use proper safety procedures
- Consult device documentation
- Follow industrial safety standards
