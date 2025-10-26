# 🧠 Clipmage – Intelligent OCR Text Capture Tool

Clipmage is a lightweight and modern **OCR (Optical Character Recognition)** utility built in **Python**, designed to capture and extract text directly from your screen with just a keyboard shortcut.  
It provides a beautiful, animated interface with visual feedback, toast notifications, and smooth usability — perfect for productivity and automation tasks.

---

## 🚀 Features

- **📸 Smart Region Capture:**  
  Select any area on your screen using a drag-and-drop overlay. Clipmage automatically detects and copies all readable text to your clipboard.

- **💬 Dynamic Toast Notifications:**  
  Elegant pop-up messages appear for every action (success, warning, or error), featuring smooth fade and glow animations.

- **🎨 Modern Design:**  
  Refined dark theme with accent colors, rounded elements, and soft glow effects that enhance readability and comfort.

- **⌨️ Keyboard Shortcuts:**
  | Shortcut | Action |
  |-----------|--------|
  | `Ctrl + Alt + S` | Capture screen region and extract text |
  | `Ctrl + Alt + P` | Pause or resume OCR |
  | `Ctrl + Alt + H` | Show help and shortcuts |
  | `Ctrl + Alt + I` | Display system and OCR engine info |
  | `Ctrl + Alt + W` | Exit the application |

- **🧩 Accessibility & Adaptability:**  
  Works across different screen sizes and resolutions. Fully compatible with high-DPI displays.

- **⚡ Lightweight & Portable:**  
  Clipmage runs silently in the background and supports both **system-installed** and **portable** versions of Tesseract OCR.

- **🛠️ Robust Error Handling:**  
  Detects and notifies the user about any issues, such as missing OCR engines or small capture regions, without crashing.

---

## 🧰 Requirements

- **Python 3.8+**
- **Tesseract OCR** (system or portable version)
- **Libraries:**
  ```bash
  pip install pyautogui pyperclip pytesseract keyboard
