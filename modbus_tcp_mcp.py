#!/usr/bin/env python3
"""
MCP Server for Modbus TCP Protocol.

This server provides comprehensive tools to interact with Modbus TCP devices,
including connection management, reading/writing registers and coils, and device diagnostics.
"""

from typing import Optional, List, Dict, Any, Union
from enum import Enum
import json
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP
import asyncio

# Try to import pymodbus, provide helpful error if not available
try:
    from pymodbus.client import AsyncModbusTcpClient
    from pymodbus.exceptions import ModbusException, ConnectionException
    from pymodbus.pdu import ExceptionResponse
except ImportError:
    raise ImportError(
        "pymodbus is required but not installed. "
        "Install it with: pip install pymodbus --break-system-packages"
    )

# Initialize the MCP server
mcp = FastMCP("modbus_tcp_mcp")

# Constants
DEFAULT_TIMEOUT = 10.0  # Default timeout for Modbus operations in seconds
CHARACTER_LIMIT = 25000  # Maximum response size in characters

# Global connection pool for managing multiple Modbus connections
_connection_pool: Dict[str, AsyncModbusTcpClient] = {}


# Enums
class ResponseFormat(str, Enum):
    """Output format for tool responses."""
    MARKDOWN = "markdown"
    JSON = "json"


class RegisterType(str, Enum):
    """Modbus register types."""
    HOLDING = "holding"  # Function code 3 (read) / 16 (write)
    INPUT = "input"      # Function code 4 (read only)
    COIL = "coil"        # Function code 1 (read) / 5 or 15 (write)
    DISCRETE = "discrete"  # Function code 2 (read only)


class DataType(str, Enum):
    """Data types for register value interpretation."""
    UINT16 = "uint16"    # Unsigned 16-bit integer
    INT16 = "int16"      # Signed 16-bit integer
    UINT32 = "uint32"    # Unsigned 32-bit integer (2 registers)
    INT32 = "int32"      # Signed 32-bit integer (2 registers)
    FLOAT32 = "float32"  # 32-bit float (2 registers)
    BOOL = "bool"        # Boolean (for coils/discrete inputs)


# Pydantic Models for Input Validation
class ConnectInput(BaseModel):
    """Input model for connecting to a Modbus TCP device."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    host: str = Field(
        ...,
        description="IP address or hostname of the Modbus TCP device (e.g., '192.168.1.100', 'plc.local')",
        min_length=1,
        max_length=255
    )
    port: int = Field(
        default=502,
        description="TCP port number (default: 502, standard Modbus TCP port)",
        ge=1,
        le=65535
    )
    timeout: float = Field(
        default=DEFAULT_TIMEOUT,
        description="Connection timeout in seconds",
        gt=0,
        le=60
    )
    unit_id: int = Field(
        default=1,
        description="Modbus slave/unit ID (default: 1, range: 0-255)",
        ge=0,
        le=255
    )


class ReadRegistersInput(BaseModel):
    """Input model for reading Modbus registers."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    host: str = Field(
        ...,
        description="IP address or hostname of the Modbus TCP device",
        min_length=1,
        max_length=255
    )
    register_type: RegisterType = Field(
        ...,
        description="Type of register to read: 'holding' (R/W, FC3), 'input' (RO, FC4), 'coil' (R/W bit, FC1), 'discrete' (RO bit, FC2)"
    )
    start_address: int = Field(
        ...,
        description="Starting register/coil address (0-based addressing, range: 0-65535)",
        ge=0,
        le=65535
    )
    count: int = Field(
        ...,
        description="Number of registers/coils to read (range: 1-125 for registers, 1-2000 for coils)",
        ge=1,
        le=2000
    )
    data_type: DataType = Field(
        default=DataType.UINT16,
        description="Data type for value interpretation: 'uint16', 'int16', 'uint32', 'int32', 'float32', 'bool'"
    )
    port: int = Field(default=502, ge=1, le=65535)
    unit_id: int = Field(default=1, ge=0, le=255)
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable"
    )

    @field_validator('count')
    @classmethod
    def validate_count(cls, v: int, info) -> int:
        register_type = info.data.get('register_type')
        if register_type in [RegisterType.HOLDING, RegisterType.INPUT] and v > 125:
            raise ValueError("Count must be <= 125 for holding/input registers")
        return v


class WriteRegisterInput(BaseModel):
    """Input model for writing to a single Modbus register."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    host: str = Field(..., min_length=1, max_length=255)
    address: int = Field(
        ...,
        description="Register/coil address to write to (0-based, range: 0-65535)",
        ge=0,
        le=65535
    )
    value: Union[int, float, bool] = Field(
        ...,
        description="Value to write. For registers: 0-65535 (uint16) or use data_type for other formats. For coils: True/False"
    )
    register_type: RegisterType = Field(
        default=RegisterType.HOLDING,
        description="Type of register: 'holding' (FC6/16) or 'coil' (FC5/15). Input/discrete are read-only."
    )
    data_type: DataType = Field(
        default=DataType.UINT16,
        description="Data type for value encoding: 'uint16', 'int16', 'uint32', 'int32', 'float32', 'bool'"
    )
    port: int = Field(default=502, ge=1, le=65535)
    unit_id: int = Field(default=1, ge=0, le=255)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class WriteMultipleRegistersInput(BaseModel):
    """Input model for writing to multiple Modbus registers."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    host: str = Field(..., min_length=1, max_length=255)
    start_address: int = Field(
        ...,
        description="Starting register/coil address (0-based)",
        ge=0,
        le=65535
    )
    values: List[Union[int, float, bool]] = Field(
        ...,
        description="List of values to write. Length must match count. For registers: 0-65535 each. For coils: True/False",
        min_length=1,
        max_length=123
    )
    register_type: RegisterType = Field(
        default=RegisterType.HOLDING,
        description="Type of register: 'holding' (FC16) or 'coil' (FC15)"
    )
    data_type: DataType = Field(
        default=DataType.UINT16,
        description="Data type for value encoding"
    )
    port: int = Field(default=502, ge=1, le=65535)
    unit_id: int = Field(default=1, ge=0, le=255)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class DeviceInfoInput(BaseModel):
    """Input model for querying device information."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    host: str = Field(..., min_length=1, max_length=255)
    port: int = Field(default=502, ge=1, le=65535)
    unit_id: int = Field(default=1, ge=0, le=255)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class DiagnosticsInput(BaseModel):
    """Input model for running diagnostics."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    host: str = Field(..., min_length=1, max_length=255)
    port: int = Field(default=502, ge=1, le=65535)
    unit_id: int = Field(default=1, ge=0, le=255)
    test_read: bool = Field(
        default=True,
        description="Test reading a register (address 0)"
    )
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


# Shared utility functions
def _get_connection_key(host: str, port: int) -> str:
    """Generate a unique key for connection pooling."""
    return f"{host}:{port}"


async def _get_or_create_client(host: str, port: int, timeout: float = DEFAULT_TIMEOUT) -> AsyncModbusTcpClient:
    """Get existing client from pool or create a new one."""
    key = _get_connection_key(host, port)
    
    if key in _connection_pool:
        client = _connection_pool[key]
        if client.connected:
            return client
        else:
            # Remove disconnected client
            del _connection_pool[key]
    
    # Create new client
    client = AsyncModbusTcpClient(
        host=host,
        port=port,
        timeout=timeout
    )
    
    try:
        await client.connect()
        if not client.connected:
            raise ConnectionException(f"Failed to connect to {host}:{port}")
        _connection_pool[key] = client
        return client
    except Exception as e:
        raise ConnectionException(f"Connection failed: {str(e)}")


def _handle_modbus_error(e: Exception, operation: str) -> str:
    """Consistent error formatting across all tools."""
    if isinstance(e, ConnectionException):
        return f"Error: Connection failed during {operation}. Please check host/port and network connectivity. Details: {str(e)}"
    elif isinstance(e, ModbusException):
        return f"Error: Modbus protocol error during {operation}. Details: {str(e)}"
    elif isinstance(e, TimeoutError):
        return f"Error: Operation timed out during {operation}. Device may be slow or unreachable."
    return f"Error: Unexpected error during {operation}: {type(e).__name__} - {str(e)}"


def _decode_register_value(registers: List[int], data_type: DataType) -> Union[int, float, bool]:
    """Decode register values based on data type."""
    import struct
    
    if data_type == DataType.UINT16:
        return registers[0]
    elif data_type == DataType.INT16:
        val = registers[0]
        return val if val < 32768 else val - 65536
    elif data_type == DataType.UINT32:
        return (registers[0] << 16) | registers[1]
    elif data_type == DataType.INT32:
        val = (registers[0] << 16) | registers[1]
        return val if val < 2147483648 else val - 4294967296
    elif data_type == DataType.FLOAT32:
        bytes_val = struct.pack('>HH', registers[0], registers[1])
        return struct.unpack('>f', bytes_val)[0]
    elif data_type == DataType.BOOL:
        return bool(registers[0])
    else:
        return registers[0]


def _encode_register_value(value: Union[int, float, bool], data_type: DataType) -> List[int]:
    """Encode value to register format based on data type."""
    import struct
    
    if data_type == DataType.UINT16:
        return [int(value) & 0xFFFF]
    elif data_type == DataType.INT16:
        val = int(value)
        return [val & 0xFFFF]
    elif data_type == DataType.UINT32:
        val = int(value)
        return [(val >> 16) & 0xFFFF, val & 0xFFFF]
    elif data_type == DataType.INT32:
        val = int(value)
        return [(val >> 16) & 0xFFFF, val & 0xFFFF]
    elif data_type == DataType.FLOAT32:
        bytes_val = struct.pack('>f', float(value))
        return list(struct.unpack('>HH', bytes_val))
    elif data_type == DataType.BOOL:
        return [1 if value else 0]
    else:
        return [int(value) & 0xFFFF]


# Tool definitions
@mcp.tool(
    name="modbus_connect",
    annotations={
        "title": "Connect to Modbus TCP Device",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def modbus_connect(params: ConnectInput) -> str:
    """
    Establish a connection to a Modbus TCP device.
    """
    try:
        client = await _get_or_create_client(params.host, params.port, params.timeout)
        
        try:
            # --- MODIFIED ---: Added keyword arguments for address, count, and slave
            result = await client.read_holding_registers(address=0, count=1, slave=params.unit_id)
            if isinstance(result, ExceptionResponse):
                connection_status = "Connected (device returned exception - normal for some devices)"
            elif result.isError():
                connection_status = "Connected (test read failed)"
            else:
                connection_status = "Connected and responding"
        except Exception:
            connection_status = "Connected (unable to test read)"
        
        return f"""# Modbus TCP Connection Successful

**Device**: {params.host}:{params.port}
**Unit ID**: {params.unit_id}
**Status**: {connection_status}
**Timeout**: {params.timeout}s

Connection is active and ready for read/write operations."""

    except Exception as e:
        return _handle_modbus_error(e, "connection")


@mcp.tool(
    name="modbus_read_registers",
    annotations={
        "title": "Read Modbus Registers/Coils",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def modbus_read_registers(params: ReadRegistersInput) -> str:
    """
    Read values from Modbus registers or coils.
    """
    try:
        client = await _get_or_create_client(params.host, params.port)
        
        # --- MODIFIED ---: Ensured all calls use keyword arguments (address, count, slave)
        if params.register_type == RegisterType.HOLDING:
            result = await client.read_holding_registers(address=params.start_address, count=params.count, slave=params.unit_id)
        elif params.register_type == RegisterType.INPUT:
            result = await client.read_input_registers(address=params.start_address, count=params.count, slave=params.unit_id)
        elif params.register_type == RegisterType.COIL:
            result = await client.read_coils(address=params.start_address, count=params.count, slave=params.unit_id)
        elif params.register_type == RegisterType.DISCRETE:
            result = await client.read_discrete_inputs(address=params.start_address, count=params.count, slave=params.unit_id)
        else:
            return f"Error: Invalid register type '{params.register_type}'"
        
        if isinstance(result, ExceptionResponse):
            return f"Error: Modbus exception {result.exception_code} - {result}"
        if result.isError():
            return f"Error: Modbus read failed - {result}"
        
        raw_values = result.bits[:params.count] if hasattr(result, 'bits') else result.registers
        
        values_list = []
        i = 0
        addr_offset = 0
        while i < len(raw_values):
            address = params.start_address + addr_offset
            
            if params.register_type in [RegisterType.COIL, RegisterType.DISCRETE]:
                decoded_val = bool(raw_values[i])
                raw_val = raw_values[i]
                i += 1
                addr_offset += 1
            else:
                regs_needed = 2 if params.data_type in [DataType.UINT32, DataType.INT32, DataType.FLOAT32] else 1
                if i + regs_needed > len(raw_values):
                    break
                
                registers_for_decode = raw_values[i:i+regs_needed]
                decoded_val = _decode_register_value(registers_for_decode, params.data_type)
                raw_val = registers_for_decode[0] if regs_needed == 1 else registers_for_decode
                i += regs_needed
                addr_offset += regs_needed

            values_list.append({"address": address, "raw_value": raw_val, "decoded_value": decoded_val})

        if params.response_format == ResponseFormat.MARKDOWN:
            lines = [f"# Modbus Read Results", f"\n**Device**: {params.host}:{params.port}",
                     f"**Register Type**: {params.register_type.value}", f"**Start Address**: {params.start_address}",
                     f"**Count**: {params.count}", f"**Data Type**: {params.data_type.value}\n\n## Values\n"]
            for val in values_list:
                lines.append(f"### Address {val['address']}\n- **Raw Value**: {val['raw_value']}\n- **Decoded Value ({params.data_type.value})**: {val['decoded_value']}\n")
            return "\n".join(lines)
        else:
            return json.dumps({
                "device": f"{params.host}:{params.port}", "register_type": params.register_type.value,
                "start_address": params.start_address, "count": params.count,
                "data_type": params.data_type.value, "values": values_list
            }, indent=2)
    
    except Exception as e:
        return _handle_modbus_error(e, "read operation")


@mcp.tool(
    name="modbus_write_register",
    annotations={
        "title": "Write to Single Modbus Register/Coil",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def modbus_write_register(params: WriteRegisterInput) -> str:
    """
    Write a value to a single Modbus register or coil.
    """
    try:
        if params.register_type in [RegisterType.INPUT, RegisterType.DISCRETE]:
            return f"Error: Cannot write to read-only register type '{params.register_type.value}'."
        
        client = await _get_or_create_client(params.host, params.port)
        
        # --- MODIFIED ---: Ensured all calls use keyword arguments (address, value, values, slave)
        if params.register_type == RegisterType.COIL:
            value_to_write = bool(params.value)
            result = await client.write_coil(address=params.address, value=value_to_write, slave=params.unit_id)
        else:
            encoded_values = _encode_register_value(params.value, params.data_type)
            if len(encoded_values) == 1:
                result = await client.write_register(address=params.address, value=encoded_values[0], slave=params.unit_id)
            else:
                result = await client.write_registers(address=params.address, values=encoded_values, slave=params.unit_id)
        
        if isinstance(result, ExceptionResponse):
            return f"Error: Modbus exception {result.exception_code} - {result}"
        if result.isError():
            return f"Error: Modbus write failed - {result}"
        
        if params.response_format == ResponseFormat.MARKDOWN:
            return f"""# Modbus Write Successful

**Device**: {params.host}:{params.port}
**Register Type**: {params.register_type.value}
**Address**: {params.address}
**Value Written**: {params.value}
**Data Type**: {params.data_type.value}"""
        else:
            return json.dumps({
                "success": True, "device": f"{params.host}:{params.port}",
                "register_type": params.register_type.value, "address": params.address,
                "value_written": params.value, "data_type": params.data_type.value
            }, indent=2)
    
    except Exception as e:
        return _handle_modbus_error(e, "write operation")


@mcp.tool(
    name="modbus_write_multiple_registers",
    annotations={
        "title": "Write to Multiple Modbus Registers/Coils",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def modbus_write_multiple_registers(params: WriteMultipleRegistersInput) -> str:
    """
    Write values to multiple consecutive Modbus registers or coils.
    """
    try:
        if params.register_type in [RegisterType.INPUT, RegisterType.DISCRETE]:
            return f"Error: Cannot write to read-only register type '{params.register_type.value}'."
        
        client = await _get_or_create_client(params.host, params.port)
        
        # --- MODIFIED ---: Ensured all calls use keyword arguments (address, values, slave)
        if params.register_type == RegisterType.COIL:
            values_to_write = [bool(v) for v in params.values]
            result = await client.write_coils(address=params.start_address, values=values_to_write, slave=params.unit_id)
        else:
            encoded_values = [v for value in params.values for v in _encode_register_value(value, params.data_type)]
            result = await client.write_registers(address=params.start_address, values=encoded_values, slave=params.unit_id)
        
        if isinstance(result, ExceptionResponse):
            return f"Error: Modbus exception {result.exception_code} - {result}"
        if result.isError():
            return f"Error: Modbus write failed - {result}"
        
        if params.response_format == ResponseFormat.MARKDOWN:
            return f"""# Modbus Multiple Write Successful

**Device**: {params.host}:{params.port}
**Register Type**: {params.register_type.value}
**Start Address**: {params.start_address}
**Count**: {len(params.values)}
**Data Type**: {params.data_type.value}
**Values Written**: {params.values}"""
        else:
            return json.dumps({
                "success": True, "device": f"{params.host}:{params.port}",
                "register_type": params.register_type.value, "start_address": params.start_address,
                "count": len(params.values), "values_written": params.values,
                "data_type": params.data_type.value
            }, indent=2)
    
    except Exception as e:
        return _handle_modbus_error(e, "multiple write operation")


@mcp.tool(
    name="modbus_device_info",
    annotations={
        "title": "Get Modbus Device Information",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def modbus_device_info(params: DeviceInfoInput) -> str:
    """
    Query Modbus device information and identification.
    """
    try:
        client = await _get_or_create_client(params.host, params.port)
        
        try:
            # This function in older versions typically only takes slave/unit
            result = await client.read_device_information(slave=params.unit_id)
            
            if isinstance(result, ExceptionResponse):
                return f"Device does not support identification (Modbus FC43). Exception: {result}"
            if result.isError():
                return "Device may not support Read Device Identification (FC43)."
            
            info = {k: v.decode() if isinstance(v, bytes) else v for k, v in result.information.items()}
            
            if params.response_format == ResponseFormat.MARKDOWN:
                lines = [f"# Modbus Device Information", f"\n**Device**: {params.host}:{params.port}",
                         f"**Unit ID**: {params.unit_id}\n"]
                lines.extend([f"**{k.replace('_', ' ').title()}**: {v}" for k, v in info.items()] or ["No device identification information available."])
                return "\n".join(lines)
            else:
                return json.dumps({
                    "device": f"{params.host}:{params.port}", "unit_id": params.unit_id,
                    "information": info or "Not available"
                }, indent=2)
                
        except Exception as e:
            return f"Device information unavailable. Device may not support FC43. Details: {str(e)}"
    
    except Exception as e:
        return _handle_modbus_error(e, "device information query")


@mcp.tool(
    name="modbus_diagnostics",
    annotations={
        "title": "Run Modbus Device Diagnostics",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def modbus_diagnostics(params: DiagnosticsInput) -> str:
    """
    Run diagnostic tests on a Modbus TCP device.
    """
    import time
    results = {"device": f"{params.host}:{params.port}", "unit_id": params.unit_id, "tests": []}
    
    start_time = time.time()
    try:
        client = await _get_or_create_client(params.host, params.port)
        latency = (time.time() - start_time) * 1000
        results["tests"].append({"name": "Connection Test", "status": "PASS", "latency_ms": round(latency, 2), "details": "Connected successfully."})
    except Exception as e:
        results["tests"].append({"name": "Connection Test", "status": "FAIL", "details": f"Connection failed: {e}"})
        if params.response_format == ResponseFormat.MARKDOWN:
            return f"# Modbus Diagnostics - FAILED\n\n**Device**: {params.host}:{params.port}\n\n## Connection Test: FAIL\n{e}\n\n**Troubleshooting**:\n1. Verify IP/port.\n2. Check network connectivity (ping {params.host})."
        else:
            return json.dumps(results, indent=2)

    if params.test_read:
        start_time = time.time()
        try:
            # --- MODIFIED ---: Added keyword arguments for address, count, and slave
            result = await client.read_holding_registers(address=0, count=1, slave=params.unit_id)
            latency = (time.time() - start_time) * 1000
            if isinstance(result, ExceptionResponse):
                results["tests"].append({"name": "Test Read (Address 0)", "status": "PARTIAL", "latency_ms": round(latency, 2), "details": f"Device responded with exception code {result.exception_code}."})
            elif result.isError():
                results["tests"].append({"name": "Test Read (Address 0)", "status": "FAIL", "details": "Read operation failed."})
            else:
                results["tests"].append({"name": "Test Read (Address 0)", "status": "PASS", "latency_ms": round(latency, 2), "details": f"Read successful, value: {result.registers[0]}."})
        except Exception as e:
            results["tests"].append({"name": "Test Read", "status": "FAIL", "details": f"Read test failed: {e}"})

    if params.response_format == ResponseFormat.MARKDOWN:
        lines = [f"# Modbus Diagnostics Results\n\n**Device**: {params.host}:{params.port}\n**Unit ID**: {params.unit_id}\n"]
        for test in results["tests"]:
            emoji = "✅" if test["status"] == "PASS" else "⚠️" if test["status"] == "PARTIAL" else "❌"
            lines.append(f"## {emoji} {test['name']}: {test['status']}")
            if "latency_ms" in test: lines.append(f"**Latency**: {test['latency_ms']}ms")
            lines.append(f"**Details**: {test['details']}\n")
        return "\n".join(lines)
    else:
        return json.dumps(results, indent=2)


@mcp.tool(
    name="modbus_disconnect",
    annotations={
        "title": "Disconnect from Modbus TCP Device",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def modbus_disconnect(host: str, port: int = 502) -> str:
    """
    Close the connection to a Modbus TCP device.
    """
    key = _get_connection_key(host, port)
    if key in _connection_pool:
        client = _connection_pool.pop(key)
        if client.connected:
            client.close()
        return f"Successfully disconnected from {host}:{port}"
    return f"No active connection to {host}:{port} to disconnect."


if __name__ == "__main__":
    mcp.run()