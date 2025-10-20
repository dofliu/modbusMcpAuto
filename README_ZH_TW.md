# Modbus TCP MCP 伺服器

一個全面的模型上下文協議 (MCP) 伺服器，用於與 Modbus TCP 設備互動。此伺服器使大型語言模型 (LLM) 能夠連接、讀取和寫入工業 Modbus TCP 設備。

## 功能

- **連接管理**：建立並維護與 Modbus TCP 設備的連接
- **讀取操作**：讀取保持暫存器、輸入暫存器、線圈和離散輸入
- **寫入操作**：寫入單個或多個暫存器/線圈
- **資料類型支援**：支援 uint16、int16、uint32、int32、float32 和 bool
- **設備資訊**：查詢設備識別（如果支援）
- **診斷**：運行全面的診斷測試
- **連接池**：高效的連接重用
- **錯誤處理**：清晰、可操作的錯誤訊息

## 安裝

### 步驟 1: 安裝依賴項

```bash
# 使用 pip 安裝（推薦使用 --break-system-packages 避免衝突）
pip install mcp pymodbus --break-system-packages

# 或者建立虛擬環境（推薦用於開發）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 步驟 2: 驗證安裝

```bash
# 檢查 Python 語法
python -m py_compile modbus_tcp_mcp.py

# 測試導入
python -c "import mcp; import pymodbus; print('✅ 所有依賴項已安裝')"
```

## 使用

### 運行伺服器

```bash
python modbus_tcp_mcp.py
```

伺服器作為基於 stdio 的 MCP 伺服器運行，並等待來自 MCP 客戶端的請求。

### 配置 Claude Desktop

將此內容添加到您的 Claude Desktop 配置文件中：

**macOS**：`~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**：`%APPDATA%/Claude/claude_desktop_config.json`

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

## 可用工具

### 1. modbus_connect
連接到 Modbus TCP 設備。

**參數**：
- `host` (str)：IP 地址或主機名（例如：「192.168.1.100」）
- `port` (int, 可選)：TCP 端口（預設值：502）
- `timeout` (float, 可選)：連接超時時間（秒）（預設值：10.0）
- `unit_id` (int, 可選)：Modbus 從站/單元 ID（預設值：1）

**範例**：
```
Connect to PLC at 192.168.1.50
```

### 2. modbus_read_registers
從 Modbus 暫存器或線圈讀取值。

**參數**：
- `host` (str)：設備 IP 地址
- `register_type` (str)：「holding」、「input」、「coil」或「discrete」
- `start_address` (int)：起始暫存器地址（基於 0）
- `count` (int)：要讀取的暫存器數量
- `data_type` (str, 可選)：「uint16」、「int16」、「uint32」、「int32」、「float32」、「bool」（預設值：「uint16」）
- `port` (int, 可選)：TCP 端口（預設值：502）
- `unit_id` (int, 可選)：從站 ID（預設值：1）
- `response_format` (str, 可選)：「markdown」或「json」（預設值：「markdown」）

**範例**：
```
Read holding registers 100-105 from PLC at 192.168.1.50 as float32
```

### 3. modbus_write_register
將值寫入單個 Modbus 暫存器或線圈。

**參數**：
- `host` (str)：設備 IP 地址
- `address` (int)：要寫入的暫存器地址
- `value` (int/float/bool)：要寫入的值
- `register_type` (str, 可選)：「holding」或「coil」（預設值：「holding」）
- `data_type` (str, 可選)：用於編碼的資料類型（預設值：「uint16」）
- `port` (int, 可選)：TCP 端口（預設值：502）
- `unit_id` (int, 可選)：從站 ID（預設值：1）
- `response_format` (str, 可選)：「markdown」或「json」（預設值：「markdown」）

**範例**：
```
Write 1500 to holding register 100 on PLC at 192.168.1.50
```

### 4. modbus_write_multiple_registers
將值寫入多個連續的暫存器或線圈。

**參數**：
- `host` (str)：設備 IP 地址
- `start_address` (int)：起始暫存器地址
- `values` (list)：要寫入的值列表
- `register_type` (str, 可選)：「holding」或「coil」（預設值：「holding」）
- `data_type` (str, 可選)：用於編碼的資料類型（預設值：「uint16」）
- `port` (int, 可選)：TCP 端口（預設值：502）
- `unit_id` (int, 可選)：從站 ID（預設值：1）
- `response_format` (str, 可選)：輸出格式（預設值：「markdown」）

**範例**：
```
Write values [100, 200, 300] to holding registers 40-42 on device 192.168.1.50
```

### 5. modbus_device_info
查詢設備識別資訊。

**參數**：
- `host` (str)：設備 IP 地址
- `port` (int, 可選)：TCP 端口（預設值：502）
- `unit_id` (int, 可選)：從站 ID（預設值：1）
- `response_format` (str, 可選)：輸出格式（預設值：「markdown」）

**範例**：
```
Get device information from PLC at 192.168.1.50
```

### 6. modbus_diagnostics
對設備運行診斷測試。

**參數**：
- `host` (str)：設備 IP 地址
- `port` (int, 可選)：TCP 端口（預設值：502）
- `unit_id` (int, 可選)：從站 ID（預設值：1）
- `test_read` (bool, 可選)：執行測試讀取（預設值：True）
- `response_format` (str, 可選)：輸出格式（預設值：「markdown」）

**範例**：
```
Run diagnostics on Modbus device at 192.168.1.50
```

### 7. modbus_disconnect
關閉與設備的連接。

**參數**：
- `host` (str)：設備 IP 地址
- `port` (int, 可選)：TCP 端口（預設值：502）

**範例**：
```
Disconnect from PLC at 192.168.1.50
```

## 暫存器類型

### 保持暫存器 (Function Code 3/6/16)
- **存取**：讀/寫
- **大小**：16 位元 (2 字節)
- **用途**：通用資料儲存、配置、設定點

### 輸入暫存器 (Function Code 4)
- **存取**：唯讀
- **大小**：16 位元 (2 字節)
- **用途**：感測器讀數、類比輸入、狀態資料

### 線圈 (Function Code 1/5/15)
- **存取**：讀/寫
- **大小**：1 位元 (布林)
- **用途**：數位輸出、控制訊號、二進位標誌

### 離散輸入 (Function Code 2)
- **存取**：唯讀
- **大小**：1 位元 (布林)
- **用途**：數位輸入、開關、二進位感測器

## 資料類型

| 類型 | 大小 | 範圍 | 描述 |
|------|------|-------|-------------|
| `uint16` | 1 暫存器 | 0 到 65535 | 無符號 16 位元整數 |
| `int16` | 1 暫存器 | -32768 到 32767 | 有符號 16 位元整數 |
| `uint32` | 2 暫存器 | 0 到 4294967295 | 無符號 32 位元整數 |
| `int32` | 2 暫存器 | -2147483648 到 2147483647 | 有符號 32 位元整數 |
| `float32` | 2 暫存器 | ±3.4e±38 | IEEE 754 浮點數 |
| `bool` | 1 暫存器/線圈 | True/False | 布林值 |

## 尋址

此伺服器使用 **基於 0 的尋址** (協議尋址)：
- 暫存器 0 = 地址 0
- 暫存器 1 = 地址 1
- 等等。

如果您的設備文檔使用基於 1 的尋址或偏移尋址（例如，保持暫存器為 40001-49999），請減去偏移量：
- 保持暫存器 40001 → 地址 0
- 輸入暫存器 30001 → 地址 0
- 線圈 00001 → 地址 0

## 範例

### 範例 1: 讀取溫度感測器
```
Read input register 100 from device 192.168.1.50 as float32
```

### 範例 2: 控制繼電器
```
Write True to coil 5 on device 192.168.1.50
```

### 範例 3: 讀取多個值
```
Read holding registers 0-9 from PLC at 192.168.1.100
```

### 範例 4: 寫入配置
```
Write values [1000, 2000, 3000, 4000, 5000] to holding registers 200-204 on device 192.168.1.50
```

### 範例 5: 設備診斷
```
Run diagnostics on device 192.168.1.50 to check connectivity and response time
```

## 錯誤處理

伺服器提供清晰、可操作的錯誤訊息：

- **連接失敗**：檢查 IP 地址、端口和網路連接
- **無效暫存器地址**：驗證地址是否在設備範圍內
- **Modbus 異常**：設備特定錯誤，請查閱設備文檔
- **超時**：設備無回應，檢查設備狀態
- **唯讀暫存器**：無法寫入輸入/離散暫存器

## 最佳實踐

1. **首先測試連接**：在其他操作之前使用 `modbus_connect`
2. **使用適當的資料類型**：將資料類型與設備配置匹配
3. **處理大量讀取**：如果需要，分塊讀取暫存器（暫存器最大 125 個）
4. **關閉連接**：完成後使用 `modbus_disconnect` 釋放資源
5. **運行診斷**：使用 `modbus_diagnostics` 排除故障

## 故障排除

### 連接超時
- 驗證設備 IP 地址和端口
- 檢查網路連接（ping 設備）
- 確保設備上正在運行 Modbus TCP 服務
- 檢查防火牆規則

### 無效地址
- 驗證設備支援的地址範圍
- 檢查是否使用基於 0 或基於 1 的尋址
- 查閱設備文檔以獲取有效的暫存器範圍

### 權限被拒
- 某些暫存器可能是唯讀的
- 檢查設備安全設置
- 驗證設備上的用戶權限

### 資料類型不匹配
- 確保資料類型與設備配置匹配
- 32 位元值需要 2 個連續暫存器
- 使用適當的位元組順序（預設為大端序）

### 常見問題 (來自 INSTALL_ZH.md)

**Q: 找不到 pymodbus**
**A**: 執行 `pip install pymodbus --break-system-packages`

**Q: 找不到 mcp**
**A**: 執行 `pip install mcp --break-system-packages`

**Q: Claude Desktop 找不到 Python**
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

**Q: 如何找到 Python 路徑？**
**A**: 執行以下命令：
```bash
# Linux/macOS
which python3

# Windows (在 cmd 中)
where python
```

## 技術細節

- **協議**：Modbus TCP (IEEE 標準)
- **預設端口**：502
- **傳輸**：TCP/IP
- **支援的功能碼**：
  - FC1: 讀取線圈 (Read Coils)
  - FC2: 讀取離散輸入 (Read Discrete Inputs)
  - FC3: 讀取保持暫存器 (Read Holding Registers)
  - FC4: 讀取輸入暫存器 (Read Input Registers)
  - FC5: 寫入單個線圈 (Write Single Coil)
  - FC6: 寫入單個暫存器 (Write Single Register)
  - FC15: 寫入多個線圈 (Write Multiple Coils)
  - FC16: 寫入多個暫存器 (Write Multiple Registers)
  - FC43: 讀取設備識別 (Read Device Identification)（如果支援）

## 許可證

此 MCP 伺服器按原樣提供，用於工業 Modbus TCP 設備。

## 支援

如有問題或疑問：
1. 查閱設備文檔以獲取支援的功能
2. 驗證網路連接和設備配置
3. 使用 `modbus_diagnostics` 工具進行故障排除
4. 查閱錯誤訊息以獲取具體指導

## 安全警告

⚠️ **注意**：此工具可以寫入工業設備。請務必：
- 首先在非關鍵系統上測試
- 了解暫存器寫入的影響
- 遵循適當的安全程序
- 查閱設備文檔
- 遵守工業安全標準