#!/usr/bin/env python3
"""
Example usage scenarios for the Modbus TCP MCP Server.

This script demonstrates common use cases and how to interact with
Modbus TCP devices through natural language queries with Claude.
"""

# These are example queries you can use with Claude when the MCP server is running:

EXAMPLE_QUERIES = """
# Connection Examples
1. "Connect to Modbus device at 192.168.1.100"
2. "Connect to PLC at 10.0.0.50 on port 5020"
3. "Test connection to Modbus server at 192.168.1.1 with unit ID 2"

# Reading Examples
4. "Read holding registers 100-110 from device 192.168.1.100"
5. "Get the value from input register 40001 on PLC 192.168.1.50 as float32"
6. "Read coil status at address 0-15 from device 192.168.1.100"
7. "Show me the values in holding registers 0-9 as int16"
8. "Read temperature sensor from input register 200 as float32 on device 192.168.1.100"

# Writing Examples
9. "Write 1500 to holding register 100 on device 192.168.1.100"
10. "Set coil 5 to True on PLC at 192.168.1.50"
11. "Write float value 23.5 to register 200 as float32 on device 192.168.1.100"
12. "Write values [100, 200, 300, 400, 500] to holding registers 10-14 on device 192.168.1.100"
13. "Set coils 0-7 to [True, False, True, False, True, False, True, False] on device 192.168.1.100"

# Device Information
14. "Get device information from PLC at 192.168.1.100"
15. "Query the identity of Modbus device at 192.168.1.50"

# Diagnostics
16. "Run diagnostics on device 192.168.1.100"
17. "Test the connection and response time of PLC at 192.168.1.50"
18. "Check if Modbus device at 192.168.1.100 is responding properly"

# Disconnect
19. "Disconnect from device 192.168.1.100"
20. "Close connection to PLC at 192.168.1.50"

# Complex Scenarios
21. "Connect to PLC at 192.168.1.100, read registers 0-10, then disconnect"
22. "Read temperature from register 100 as float32 on device 192.168.1.50 and compare with setpoint in register 200"
23. "Write configuration values [1000, 2000, 3000] to registers 300-302 and verify by reading them back"
24. "Monitor coils 0-3 on device 192.168.1.100 and show their status"
25. "Read all holding registers from 0-50 on device 192.168.1.100 and format as JSON"
"""

# Common Register Address Conversions
ADDRESS_CONVERSION_GUIDE = """
# Converting from 1-Based or Offset Addressing to 0-Based

Many Modbus device documentation uses offset addressing:

## Holding Registers (40001-49999)
- Document shows: 40001 → Use address: 0
- Document shows: 40100 → Use address: 99
- Document shows: 41000 → Use address: 999

## Input Registers (30001-39999)
- Document shows: 30001 → Use address: 0
- Document shows: 30100 → Use address: 99

## Coils (00001-09999)
- Document shows: 00001 → Use address: 0
- Document shows: 00100 → Use address: 99

## Discrete Inputs (10001-19999)
- Document shows: 10001 → Use address: 0
- Document shows: 10100 → Use address: 99

Formula: Protocol Address = Documented Address - Offset
Where offset is 40001, 30001, 00001, or 10001
"""

# Device Configuration Examples
DEVICE_CONFIGS = """
# Example Device Configurations

## Example 1: Temperature Controller
- IP: 192.168.1.100
- Unit ID: 1
- Registers:
  - 100 (input): Current Temperature (float32)
  - 200 (holding): Temperature Setpoint (float32)
  - 300 (holding): Control Mode (uint16: 0=Off, 1=Heat, 2=Cool)
  - 0 (coil): System Enable

## Example 2: Motor Controller
- IP: 192.168.1.101
- Unit ID: 1
- Registers:
  - 0-3 (input): Current Speed, Torque, Voltage, Current (all float32)
  - 100 (holding): Speed Setpoint (float32)
  - 200 (holding): Acceleration Rate (float32)
  - 0 (coil): Motor Start/Stop
  - 1 (coil): Emergency Stop

## Example 3: PLC with Multiple Zones
- IP: 192.168.1.102
- Unit ID: 1
- Registers:
  - 0-99 (holding): Zone 1 Configuration
  - 100-199 (holding): Zone 2 Configuration
  - 200-299 (holding): Zone 3 Configuration
  - 1000-1099 (input): Zone 1 Status
  - 1100-1199 (input): Zone 2 Status
  - 1200-1299 (input): Zone 3 Status
"""

# Safety Reminders
SAFETY_REMINDERS = """
# Safety Reminders for Industrial Automation

⚠️ IMPORTANT SAFETY CONSIDERATIONS:

1. **Test on Non-Critical Systems First**
   - Always test new configurations on development systems
   - Verify behavior before deploying to production

2. **Understand Register Functions**
   - Know what each register controls
   - Consult device documentation
   - Understand the implications of writes

3. **Use Proper Safety Procedures**
   - Follow lockout/tagout procedures
   - Coordinate with operations team
   - Have emergency stop procedures ready

4. **Verify Data Types**
   - Incorrect data types can cause unexpected behavior
   - Confirm byte order (endianness) with device
   - Test with known values first

5. **Monitor After Changes**
   - Watch device behavior after writes
   - Check logs and alarms
   - Be ready to revert changes

6. **Network Security**
   - Use secure networks for industrial devices
   - Limit access to authorized personnel
   - Monitor for unauthorized access

7. **Backup Configurations**
   - Save current settings before changes
   - Document all modifications
   - Have rollback procedures ready
"""

if __name__ == "__main__":
    print("=" * 80)
    print("Modbus TCP MCP Server - Usage Examples")
    print("=" * 80)
    print("\nThis file contains example queries and configuration guides.")
    print("Use these examples with Claude when the MCP server is running.\n")
    
    print("EXAMPLE QUERIES:")
    print(EXAMPLE_QUERIES)
    
    print("\n" + "=" * 80)
    print("ADDRESS CONVERSION GUIDE:")
    print(ADDRESS_CONVERSION_GUIDE)
    
    print("\n" + "=" * 80)
    print("DEVICE CONFIGURATIONS:")
    print(DEVICE_CONFIGS)
    
    print("\n" + "=" * 80)
    print("SAFETY REMINDERS:")
    print(SAFETY_REMINDERS)
    
    print("\n" + "=" * 80)
    print("\nTo use this MCP server:")
    print("1. Ensure the server is running: python modbus_tcp_mcp.py")
    print("2. Configure it in Claude Desktop's config file")
    print("3. Use natural language queries like the examples above")
    print("=" * 80)
