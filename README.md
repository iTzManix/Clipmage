# 🧠 Clipmage – Intelligent OCR Text Capture Tool

Clipmage is a lightweight and modern **OCR (Optical Character Recognition)** utility built in **Python**, designed to capture and extract text directly from your screen with just a keyboard shortcut.  
It provides a beautiful, animated interface with visual feedback, toast notifications, and smooth usability — perfect for productivity and automation tasks.

---

## 🚀 Features

- **📸 Smart Region Capture:**  
  Select any area on your screen using a drag-and-drop overlay. Clipmage automatically detects and reads all text and copies it to your clipboard.

- **💬 Dynamic Toast Notifications:**  
  Elegant pop-up messages appear for every action (success, warning, or error), featuring smooth fade and glow animations.

- **🎨 Modern Design:**  
  Refined dark and light theme with accent colors, rounded elements, and soft glow effects that enhance readability and comfort.

- **⌨️ Keyboard Shortcuts:**
  | Shortcut | Action |
  |-----------|--------|
  | `Ctrl + Alt + S` | Capture screen region and extract text |
  | `P` | Pause or resume OCR |
  | `H` | Show help and shortcuts |
  | `I` | Display system and OCR engine info |
  | `T` | Toggle dark/light theme |
  | `W` | Exit the application |

- **🧩 Accessibility & Adaptability:**  
  Works across different screen sizes and resolutions. Fully compatible with high-DPI displays.

- **⚡ Lightweight & Portable:**  
  Clipmage runs silently in the background and supports both **system-installed** and **portable** versions of Tesseract OCR.

- **🛠️ Robust Error Handling:**  
  Detects and notifies the user about any issues gracefully.

---

## 🧰 Requirements

- **Python 3.10+** (3.13 recommended)
- **Tesseract OCR** (bundled in executable)
- **Windows 10/11**

---

## 📦 Installation

### Option 1: Download Executable (Recommended)

1. Go to [Releases](https://github.com/iTzManix/Clipmage/releases)
2. Download `Clipmage.exe`
3. Run it directly — no installation needed!

### Option 2: Compile from Source

```bash
# Clone repository
git clone https://github.com/iTzManix/Clipmage.git
cd Clipmage

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run
python src/Clipmage.py
```

---

## ⚠️ Windows Defender / Antivirus Notice

Clipmage may trigger a warning from Windows Defender when first run. **This is completely safe to ignore.**

### Why does this happen?

- ✅ **Portable Tesseract OCR** - The bundled OCR engine can be flagged by some antivirus software
- ✅ **Automation libraries** - `pyautogui` and `keyboard` libraries used for shortcuts and screen capture
- ✅ **Executable from internet** - Downloaded files from the internet are scanned by Windows Defender

### How to safely use Clipmage:

#### Method 1: Allow Execution (Fastest)

1. Download and try to run `Clipmage.exe`
2. Windows shows **"Windows protected your PC"** warning
3. Click **"More options"** → **"Run anyway"**
4. Done! Clipmage will now run normally

#### Method 2: Exclude from Windows Defender (Recommended)

1. Open **Windows Defender**
2. Go to **Virus & threat protection**
3. Click **Manage settings**
4. Scroll to **Exclusions** → **Add or remove exclusions**
5. Add the Clipmage folder or executable

#### Method 3: Compile from Source (Most Secure)

For users who want to verify the code themselves:

```bash
git clone https://github.com/iTzManix/Clipmage.git
cd Clipmage
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/Clipmage.py
```

### 🔐 Security & Privacy

- 🔒 **No telemetry** - We don't collect any data
- 🔒 **No account required** - Works completely offline
- 🔒 **No internet connection needed** - Everything runs locally
- 🔒 **Code auditable** - Full source code on GitHub (MIT License)
- 🔒 **Digitally signed** - Executable is cryptographically signed

---

## 🎯 Quick Start

1. **Download** `Clipmage.exe` from Releases
2. **Run** the executable
3. Press **`Ctrl + Alt + S`** to start capturing
4. **Drag** to select the text area
5. **Text is copied** to your clipboard automatically!

---

## 🔧 Configuration

Keyboard shortcuts can be customized by editing `src/Clipmage.py`:

```python
keyboard.add_hotkey('ctrl+alt+s', app.capture_and_extract_text)
keyboard.add_hotkey('p', app.toggle_status)
keyboard.add_hotkey('h', app.show_help)
keyboard.add_hotkey('i', app.show_info)
keyboard.add_hotkey('t', app.toggle_theme)
keyboard.add_hotkey('w', app.quit_app)
```

---

## 📊 System Requirements

| Requirement | Minimum    | Recommended |
| ----------- | ---------- | ----------- |
| OS          | Windows 10 | Windows 11  |
| Python      | 3.8        | 3.13+       |
| RAM         | 128 MB     | 512 MB      |
| Disk        | 150 MB     | 300 MB      |
| Display     | 1024x768   | 1920x1080+  |

---

## 🐛 Troubleshooting

### "Tesseract not found" error

- Restart Clipmage — it will auto-install on first run
- Check `%LOCALAPPDATA%\Clipmage` folder exists
- Run as Administrator if permissions issue

### Region capture not working

- Ensure `Ctrl + Alt + S` shortcut is available (not used by other apps)
- Try running as Administrator
- Disable any screen recording software

### Inaccurate OCR results

- Make sure text is clearly visible
- Increase capture region size
- Try different fonts/styles
- Check system has sufficient RAM

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Found a bug or have a feature idea?

- 🐛 Report bugs: [Issues](https://github.com/iTzManix/Clipmage/issues)
- 💡 Suggest features: [Discussions](https://github.com/iTzManix/Clipmage/discussions)
- 🔧 Submit code: Create a Pull Request

---

## 🎉 Acknowledgments

Built with ❤️ using:

- **Python** - Programming language
- **Tesseract OCR** - Text recognition engine
- **PyAutoGUI** - Screen automation
- **PyTesseract** - Python bindings for Tesseract

---

**Made with 🧠 and ❤️ by [iTzManix](https://github.com/iTzManix)**
