# Browser Harness - Windows 适配版

> 基于 [browser-use/browser-harness](https://github.com/browser-use/browser-harness) 的 Windows 平台适配版本

## 🎯 项目简介

Browser Harness 是一个强大的浏览器自动化工具，通过 Chrome DevTools Protocol (CDP) 实现对浏览器的精确控制。本项目在原版基础上增加了完整的 Windows 平台支持。

### 核心特性

- ✅ **跨平台支持**: Windows、Linux、macOS 全平台兼容
- ✅ **CDP 协议**: 直接使用 Chrome DevTools Protocol，无需 Selenium
- ✅ **轻量高效**: 纯 Python 实现，无重型依赖
- ✅ **功能完整**: 页面导航、截图、JavaScript 执行、标签管理等

---

## 🔧 Windows 适配说明

### 主要改动

原版 Browser Harness 使用 Unix Domain Socket 进行进程间通信，Windows 不支持。本适配版实现了跨平台兼容层：

1. **新增文件**: `socket_compat.py` - 跨平台 Socket 兼容层
2. **修改文件**: `helpers.py`, `admin.py`, `daemon.py` - 使用兼容层
3. **关键修复**: 使用稳定的 MD5 hash 替代 Python 随机 hash，确保端口一致性

### 技术细节

| 平台 | 通信方式 | 路径/端口 |
|------|----------|-----------|
| Unix/Linux/macOS | Unix Domain Socket | `/tmp/bu-{name}.sock` |
| Windows | TCP Socket | `127.0.0.1:19222+offset` |

---

## 📦 安装

### 前置要求

- Python 3.8+
- Chrome 或 Edge 浏览器
- Windows 10/11 或 Unix-like 系统

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/YOUR-USERNAME/browser-harness-windows.git
cd browser-harness-windows

# 安装依赖
pip install -r requirements.txt
```

---

## 🚀 快速开始

### 1. 启动 Chrome (远程调试模式)

**Windows:**
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%TEMP%\chrome-debug"
```

### 2. 获取 WebSocket URL

```bash
curl http://127.0.0.1:9222/json/version
```

### 3. 启动 Browser Harness Daemon

```bash
export BU_CDP_WS="ws://127.0.0.1:9222/devtools/browser/YOUR-BROWSER-ID"
python daemon.py
```

### 4. 使用示例

```python
from helpers import goto_url, page_info, capture_screenshot

# 导航到网页
goto_url('https://www.example.com')

# 获取页面信息
info = page_info()
print(f"Title: {info['title']}")

# 截图
capture_screenshot('screenshot.png')
```

---

## 📚 API 文档

### 页面导航
- `goto_url(url)` - 导航到指定 URL
- `wait_for_load(timeout)` - 等待页面加载

### 页面信息
- `page_info()` - 获取页面信息 (标题、URL、尺寸等)

### 截图
- `capture_screenshot(path, full=False)` - 截图

### JavaScript
- `js(expression)` - 执行 JavaScript

### 用户交互
- `click_at_xy(x, y)` - 点击坐标
- `type_text(text)` - 输入文本
- `press_key(key)` - 按键
- `scroll(x, y, dy)` - 滚动

### 标签管理
- `list_tabs()` - 列出所有标签
- `current_tab()` - 获取当前标签
- `switch_tab(target_id)` - 切换标签
- `new_tab(url)` - 新建标签

---

## 🧪 测试结果

### 功能测试

| 功能 | Windows | 说明 |
|------|---------|------|
| Socket 通信 | ✅ | TCP Socket (127.0.0.1:19292) |
| Chrome 连接 | ✅ | CDP WebSocket 连接成功 |
| 页面导航 | ✅ | goto_url() 正常工作 |
| 页面信息 | ✅ | page_info() 正常工作 |
| 截图 | ✅ | capture_screenshot() 正常工作 |
| JavaScript | ✅ | js() 正常执行 |
| 标签管理 | ✅ | 所有标签操作正常 |

---

## 🔍 故障排除

### 连接被拒绝 (ConnectionRefusedError)

**解决**: 确保 daemon 正在运行
```bash
python daemon.py
```

### DevToolsActivePort not found

**解决**: 使用正确的参数启动 Chrome
```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="%TEMP%\chrome-debug"
```

---

## 📄 许可证

本项目基于原 [browser-harness](https://github.com/browser-use/browser-harness) 项目。

Windows 适配部分由 [@duanhaoran](https://github.com/duanhaoran) 贡献。

---

**最后更新**: 2026-04-25  
**版本**: 1.0.0-windows
