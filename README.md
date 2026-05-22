# 🎮 MHR Armor Swapper

> Transform your Monster Hunter Rise armor mods with a single click

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
![Windows](https://img.shields.io/badge/platform-Windows-brightgreen)

## ✨ Overview

**MHR Armor Swapper** is a lightweight, user-friendly utility designed for Monster Hunter Rise modders. Convert any armor mod to use a different armor ID in seconds—perfect for customizing which armor slot your favorite mod replaces.

### Perfect for:
- Armor modders offering multiple slot variants
- Players wanting their preferred armor in a specific slot
- Batch converting armor mods
- Fluffy Mod Manager integration

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🔍 **Auto-Detection** | Automatically identifies armor ID in ZIP files |
| 🎯 **Smart Search** | 250+ armor database with instant name/ID lookup |
| ⚡ **One-Click Convert** | Select source → target → done |
| 📦 **Auto-Pack** | Converted ZIP ready for Fluffy Mod Manager |
| 🌙 **Modern UI** | Beautiful dark theme with CustomTkinter |
| 💾 **Standalone** | No dependencies needed (EXE included) |
| ✅ **Wide Support** | Works with most armor replacement mods |

## 📥 Installation

### Option 1: Download EXE (Recommended)
1. Go to [Releases](https://github.com/Anedeshii/MHR-Armor-Swapper/releases)
2. Download `MHR Armor Swapper.exe`
3. Run it - no installation needed!

### Option 2: Run from Source
```bash
# Clone
git clone https://github.com/Anedeshii/MHR-Armor-Swapper.git
cd MHR-Armor-Swapper

# Install dependencies
pip install -r requirements.txt

# Run
python mhr_armor_swapper_v4.py
```

## 📖 How to Use

1. **Launch** the application
2. **Select** your armor mod ZIP file
3. **Search** for target armor (name or ID)
4. **Click Convert** - automatically repacks the ZIP
5. **Done!** New file ready for Fluffy Mod Manager

## 📋 Requirements

| Requirement | Version |
|---|---|
| **OS** | Windows 10 / 11 |
| **Python** (source only) | 3.9+ |
| **Game** | Monster Hunter Rise / Sunbreak |
| **Mod Manager** | Fluffy Mod Manager |

## 🛠️ Technical Stack

- **Language**: Python 3.9+
- **UI Framework**: CustomTkinter
- **Image Processing**: Pillow
- **Build Tool**: Nuitka (for EXE)

## 📁 Project Structure

```
.
├── mhr_armor_swapper_v4.py    # Main application
├── armor_database.txt          # 250+ armor mappings
├── MHR Armor Swapper.exe       # Standalone executable
├── requirements.txt            # Dependencies
├── README.md                   # This file
└── LICENSE                     # MIT License
```

## 🐛 Troubleshooting

### "Invalid ZIP file"
- Ensure the ZIP is a valid Fluffy Mod Manager mod
- Check mod structure is intact

### "Armor not detected"
- Some custom mods may use non-standard structures
- Try manual armor ID selection if available

### "Cannot open ZIP"
- Close any archive tools/file managers
- Check you have write permissions
- Ensure enough disk space

## 🤝 Contributing

Found a bug? Have an idea?
- [Report Issue](https://github.com/Anedeshii/MHR-Armor-Swapper/issues)
- [Pull Request](https://github.com/Anedeshii/MHR-Armor-Swapper/pulls)

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

## 🙏 Credits

- **Capcom** - Monster Hunter Rise, Sunbreak
- **Fluffy Mod Manager** - Best MHR mod manager
- **CustomTkinter** - Beautiful UI framework
- **Modding Community** - Inspiration & support

## 📞 Support

- 💬 Open an issue on GitHub
- 🌐 Check [Monster Hunter Wiki](https://monsterhunter.fandom.com/)

---

**Made with ❤️ for Monster Hunter modders**

v4.0 • Last Updated: May 2024
