# Modbus TCP MCP Server - 檔案清單

## 📁 專案檔案

### 核心檔案

#### 1. `modbus_tcp_mcp.py` (41 KB)
MCP 伺服器主程式，包含以下功能：

**工具 (Tools)**:
- `modbus_connect` - 連接到 Modbus TCP 設備
- `modbus_read_registers` - 讀取暫存器/線圈
- `modbus_write_register` - 寫入單個暫存器/線圈
- `modbus_write_multiple_registers` - 寫入多個暫存器/線圈
- `modbus_device_info` - 查詢設備資訊
- `modbus_diagnostics` - 執行診斷測試
- `modbus_disconnect` - 斷開連接

**支援的功能**:
- 連接池管理
- 多種資料類型（uint16, int16, uint32, int32, float32, bool）
- 四種暫存器類型（holding, input, coil, discrete）
- 完整的錯誤處理
- Markdown 和 JSON 輸出格式

#### 2. `requirements.txt` (43 bytes)
Python 依賴項清單：
```
mcp>=1.0.0
pymodbus>=3.0.0
pydantic>=2.0.0
```

### 文檔檔案

#### 3. `README.md` (9.5 KB)
完整的英文文檔，包含：
- 功能概述
- 安裝說明
- 所有工具的詳細文檔
- 暫存器類型說明
- 資料類型表格
- 使用範例
- 故障排除指南
- 安全警告

#### 4. `INSTALL_ZH.md` (2.9 KB)
中文快速安裝指南，包含：
- 逐步安裝說明
- Claude Desktop 配置
- 常見問題解答
- 故障排除技巧

#### 5. `examples.py` (6.0 KB)
使用範例和指南，包含：
- 25+ 個查詢範例
- 地址轉換指南（1-based 到 0-based）
- 設備配置範例
- 安全提醒清單

## 🚀 快速開始

### 1. 安裝依賴
```bash
pip install -r requirements.txt --break-system-packages
```

### 2. 驗證安裝
```bash
python -m py_compile modbus_tcp_mcp.py
```

### 3. 配置 Claude Desktop
編輯配置檔案並添加：
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

### 4. 重啟 Claude Desktop

### 5. 開始使用
```
連接到 Modbus 設備 192.168.1.100
```

## 📋 功能檢查清單

### 讀取功能
- ✅ 讀取保持暫存器 (Holding Registers - FC3)
- ✅ 讀取輸入暫存器 (Input Registers - FC4)
- ✅ 讀取線圈 (Coils - FC1)
- ✅ 讀取離散輸入 (Discrete Inputs - FC2)
- ✅ 支援批量讀取 (1-125 個暫存器, 1-2000 個線圈)

### 寫入功能
- ✅ 寫入單個保持暫存器 (FC6)
- ✅ 寫入單個線圈 (FC5)
- ✅ 寫入多個保持暫存器 (FC16)
- ✅ 寫入多個線圈 (FC15)
- ✅ 防止寫入唯讀暫存器

### 資料類型
- ✅ uint16 (無符號 16 位元整數)
- ✅ int16 (有符號 16 位元整數)
- ✅ uint32 (無符號 32 位元整數)
- ✅ int32 (有符號 32 位元整數)
- ✅ float32 (IEEE 754 浮點數)
- ✅ bool (布林值)

### 進階功能
- ✅ 連接池管理
- ✅ 自動重連
- ✅ 設備識別 (FC43)
- ✅ 診斷測試
- ✅ 延遲測量
- ✅ 錯誤處理
- ✅ 多種輸出格式 (Markdown/JSON)

### 安全性
- ✅ 輸入驗證 (Pydantic)
- ✅ 超時保護
- ✅ 清晰的錯誤訊息
- ✅ 唯讀暫存器保護
- ✅ 地址範圍檢查

## 🔧 技術規格

- **協議**: Modbus TCP (IEEE 標準)
- **傳輸**: TCP/IP
- **預設埠**: 502
- **地址模式**: 0-based (協議地址)
- **最大讀取**: 125 個暫存器 / 2000 個線圈
- **最大寫入**: 123 個暫存器
- **支援的功能碼**: FC1, FC2, FC3, FC4, FC5, FC6, FC15, FC16, FC43
- **字節順序**: Big-endian (可自定義)

## 📊 效能特點

- **連接池**: 重用連接以提高效能
- **非同步操作**: 使用 async/await 提高響應速度
- **批量操作**: 支援批量讀寫以減少網路往返
- **超時管理**: 可配置的超時設定
- **錯誤恢復**: 自動重試和錯誤處理

## ⚠️ 安全注意事項

此工具可以**寫入工業設備**。使用前請：

1. ✅ 在非關鍵系統上測試
2. ✅ 了解暫存器功能
3. ✅ 遵循安全程序
4. ✅ 驗證資料類型
5. ✅ 監控變更後的行為
6. ✅ 使用安全網路
7. ✅ 備份配置

## 📞 支援

如有問題：
1. 查看 `README.md` 完整文檔
2. 查看 `examples.py` 使用範例
3. 查看 `INSTALL_ZH.md` 安裝指南
4. 使用 `modbus_diagnostics` 工具排除故障

## 📝 版本資訊

- **版本**: 1.0.0
- **最後更新**: 2025年10月
- **Python**: 3.8+
- **依賴**: mcp>=1.0.0, pymodbus>=3.0.0, pydantic>=2.0.0

## 📄 授權

此 MCP 伺服器按原樣提供，用於工業 Modbus TCP 設備。

---

**專案結構**:
```
modbus-tcp-mcp/
├── modbus_tcp_mcp.py      # 主程式
├── requirements.txt        # 依賴項
├── README.md              # 英文文檔
├── INSTALL_ZH.md          # 中文安裝指南
├── examples.py            # 使用範例
└── FILE_LIST.md           # 此檔案
```
