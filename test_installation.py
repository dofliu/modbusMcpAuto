#!/usr/bin/env python3
"""
Modbus TCP MCP Server - 測試和驗證腳本

此腳本幫助驗證 MCP 伺服器的安裝和配置。
"""

import sys
import subprocess

def check_python_version():
    """檢查 Python 版本"""
    print("檢查 Python 版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (需要 3.8+)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (需要 3.8+)")
        return False

def check_dependencies():
    """檢查依賴項是否已安裝"""
    print("\n檢查依賴項...")
    dependencies = {
        "mcp": "MCP Python SDK",
        "pymodbus": "Pymodbus 庫",
        "pydantic": "Pydantic 驗證庫"
    }
    
    all_installed = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name} 已安裝")
        except ImportError:
            print(f"❌ {name} 未安裝")
            print(f"   安裝命令: pip install {module} --break-system-packages")
            all_installed = False
    
    return all_installed

def check_syntax():
    """檢查 Python 檔案語法"""
    print("\n檢查 MCP 伺服器語法...")
    try:
        result = subprocess.run(
            ["python", "-m", "py_compile", "modbus_tcp_mcp.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ modbus_tcp_mcp.py 語法正確")
            return True
        else:
            print("❌ modbus_tcp_mcp.py 語法錯誤")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("⚠️  找不到 modbus_tcp_mcp.py 檔案")
        print("   請確保您在正確的目錄中執行此腳本")
        return False
    except Exception as e:
        print(f"❌ 檢查語法時發生錯誤: {e}")
        return False

def test_imports():
    """測試是否可以導入必要的模組"""
    print("\n測試模組導入...")
    try:
        from mcp.server.fastmcp import FastMCP
        print("✅ 可以導入 FastMCP")
        
        from pymodbus.client import AsyncModbusTcpClient
        print("✅ 可以導入 AsyncModbusTcpClient")
        
        from pydantic import BaseModel, Field
        print("✅ 可以導入 Pydantic")
        
        return True
    except ImportError as e:
        print(f"❌ 導入錯誤: {e}")
        return False

def show_config_instructions():
    """顯示配置說明"""
    print("\n" + "="*60)
    print("配置 Claude Desktop")
    print("="*60)
    
    import os
    import platform
    
    system = platform.system()
    if system == "Darwin":  # macOS
        config_path = "~/Library/Application Support/Claude/claude_desktop_config.json"
    elif system == "Windows":
        config_path = "%APPDATA%\\Claude\\claude_desktop_config.json"
    else:  # Linux
        config_path = "~/.config/Claude/claude_desktop_config.json"
    
    print(f"\n配置檔案位置: {config_path}")
    print("\n添加以下內容到配置檔案:\n")
    
    current_dir = os.getcwd()
    mcp_path = os.path.join(current_dir, "modbus_tcp_mcp.py")
    
    config = f'''{{
  "mcpServers": {{
    "modbus_tcp": {{
      "command": "python",
      "args": ["{mcp_path}"]
    }}
  }}
}}'''
    
    print(config)
    print("\n注意: 如果 Python 不在 PATH 中，請使用完整路徑")
    print(f"      例如: \"/usr/bin/python3\" 或 \"C:\\\\Python39\\\\python.exe\"")

def show_test_queries():
    """顯示測試查詢範例"""
    print("\n" + "="*60)
    print("測試查詢範例")
    print("="*60)
    print("""
配置完成後，在 Claude 中嘗試以下查詢:

1. 測試連接:
   "連接到 Modbus 設備 192.168.1.100"

2. 讀取暫存器:
   "從設備 192.168.1.100 讀取保持暫存器 0-9"

3. 檢查設備資訊:
   "查詢設備 192.168.1.100 的資訊"

4. 執行診斷:
   "對設備 192.168.1.100 執行診斷測試"

⚠️  注意: 請將 IP 地址替換為您實際的 Modbus 設備地址
""")

def main():
    """主函數"""
    print("="*60)
    print("Modbus TCP MCP Server - 安裝驗證")
    print("="*60)
    
    checks = [
        ("Python 版本", check_python_version),
        ("依賴項", check_dependencies),
        ("檔案語法", check_syntax),
        ("模組導入", test_imports),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {name} 檢查失敗: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print("檢查總結")
    print("="*60)
    
    if all(results):
        print("✅ 所有檢查通過！")
        print("\n下一步:")
        print("1. 配置 Claude Desktop (見下方)")
        print("2. 重啟 Claude Desktop")
        print("3. 嘗試測試查詢 (見下方)")
        show_config_instructions()
        show_test_queries()
    else:
        print("❌ 部分檢查失敗")
        print("\n請修復上述問題後重新執行此腳本")
        print("\n常見解決方案:")
        print("- 安裝依賴項: pip install -r requirements.txt --break-system-packages")
        print("- 確保使用 Python 3.8 或更高版本")
        print("- 檢查是否在正確的目錄中")
    
    print("\n" + "="*60)
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())
