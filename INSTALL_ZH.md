# Modbus TCP MCP Server - 快速安裝指南

## 步驟 1: 安裝依賴項

```bash
# 使用 pip 安裝（推薦使用 --break-system-packages 避免衝突）
pip install mcp pymodbus --break-system-packages

# 或者建立虛擬環境（推薦用於開發）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 步驟 2: 驗證安裝

```bash
# 檢查 Python 語法
python -m py_compile modbus_tcp_mcp.py

# 測試導入
python -c "import mcp; import pymodbus; print('✅ 所有依賴項已安裝')"
```

## 步驟 3: 配置 Claude Desktop

### macOS
編輯文件: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows
編輯文件: `%APPDATA%\Claude\claude_desktop_config.json`

### Linux
編輯文件: `~/.config/Claude/claude_desktop_config.json`

### 配置內容
```json
{
  "mcpServers": {
    "modbus_tcp": {
      "command": "python",
      "args": ["/完整/路徑/到/modbus_tcp_mcp.py"]
    }
  }
}
```

**重要**: 請將 `/完整/路徑/到/` 替換為您實際的檔案路徑。

## 步驟 4: 重啟 Claude Desktop

關閉並重新開啟 Claude Desktop 應用程式以載入 MCP 伺服器。

## 步驟 5: 測試連接

在 Claude 中嘗試以下查詢（請將 IP 地址替換為您的設備地址）：

```
連接到 Modbus 設備 192.168.1.100
```

## 常見問題

### Q: 找不到 pymodbus
**A**: 執行 `pip install pymodbus --break-system-packages`

### Q: 找不到 mcp
**A**: 執行 `pip install mcp --break-system-packages`

### Q: Claude Desktop 找不到 Python
**A**: 在配置文件中使用 Python 的完整路徑：
```json
{
  "mcpServers": {
    "modbus_tcp": {
      "command": "/usr/bin/python3",  # 或 "C:\\Python39\\python.exe" (Windows)
      "args": ["/完整/路徑/到/modbus_tcp_mcp.py"]
    }
  }
}
```

### Q: 如何找到 Python 路徑？
**A**: 執行以下命令：
```bash
# Linux/macOS
which python3

# Windows (在 cmd 中)
where python
```

### Q: 連接超時
**A**: 
1. 檢查設備 IP 地址是否正確
2. 確認設備在網路上（嘗試 ping）
3. 檢查防火牆設置
4. 確認 Modbus TCP 服務正在設備上運行

## 支援的功能

✅ 連接到 Modbus TCP 設備
✅ 讀取保持暫存器 (Holding Registers)
✅ 讀取輸入暫存器 (Input Registers)
✅ 讀取線圈 (Coils)
✅ 讀取離散輸入 (Discrete Inputs)
✅ 寫入單個暫存器/線圈
✅ 寫入多個暫存器/線圈
✅ 設備診斷
✅ 查詢設備資訊
✅ 多種資料類型（uint16, int16, uint32, int32, float32, bool）
✅ 連接池管理
✅ 清晰的錯誤訊息

## 下一步

查看 `examples.py` 了解更多使用範例，或查看 `README.md` 了解完整文檔。

## 安全提醒

⚠️ 此工具可以寫入工業設備。使用前請：
- 在非關鍵系統上測試
- 了解暫存器寫入的影響
- 遵循適當的安全程序
- 查閱設備文檔
- 遵守工業安全標準
