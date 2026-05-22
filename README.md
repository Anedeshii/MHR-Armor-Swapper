# MHR Armor Swapper

> A modern, standalone utility for converting Monster Hunter Rise armor mods into different armor IDs automatically.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)

## 🎯 Overview

MHR Armor Swapper is a powerful tool designed specifically for **Monster Hunter Rise** and **Sunbreak** modders. It enables seamless conversion of armor mods to use different armor IDs, making it trivial to swap which armor slot your mod replaces.

**Perfect for:**
- Armor modders who want to offer multiple armor slot options
- Players who prefer their favorite armor on a specific slot
- Bulk armor mod conversions
- Use with **Fluffy Mod Manager**

## ✨ Key Features

- 🔍 **Automatic Armor ID Detection** - Scans ZIP files to identify current armor
- 🎯 **Searchable Armor Database** - 250+ Monster Hunter Rise armors with instant search
- ⚡ **One-Click Conversion** - Select source → target armor → convert
- 📦 **Automatic ZIP Repack** - Converted files ready for Fluffy Mod Manager
- 🌙 **Modern Dark UI** - Built with CustomTkinter for beautiful, responsive interface
- 💾 **Standalone EXE** - No dependencies needed (bundled executable available)
- ✅ **Wide Mod Support** - Compatible with most armor replacement mods

## 📋 Requirements

| Requirement | Minimum |
|---|---|
| OS | Windows 10 / 11 |
| Python | 3.9+ (if running from source) |
| Game | Monster Hunter Rise / Sunbreak |
| Mod Manager | Fluffy Mod Manager |

## 🚀 Quick Start

### Option 1: Using Executable (Recommended)
1. Download the latest `.exe` from [Releases](https://github.com/yourusername/MHR-Armor-Swapper/releases)
2. Run `MHR Armor Swapper.exe`
3. No installation required!

### Option 2: Running from Source
```bash
# Clone repository
git clone https://github.com/yourusername/MHR-Armor-Swapper.git
cd MHR-Armor-Swapper

# Install dependencies
pip install -r requirements.txt

# Run application
python mhr_armor_swapper_v4.py
```

## 📖 Usage

1. **Open Application** - Launch the executable or Python script
2. **Select Armor Mod** - Click "Select ZIP" and choose your armor mod file
3. **Detect Source Armor** - Application auto-detects current armor ID
4. **Search Target Armor** - Find desired armor using search bar (name or ID)
5. **Select Target** - Click on target armor from database
6. **Convert** - Click "Convert" button
7. **Save** - New ZIP is automatically saved to `output/` folder

**That's it!** Your converted mod is ready for Fluffy Mod Manager.

## 📊 Supported Armors

Current armor database includes:
- **Base Game**: Kamura, Hunter, Leather, Chainmail, Alloy, and more
- **Iceborne Armors**: All Master Rank armor sets
- **Sunbreak Armors**: Village and Hub armor sets
- **Special Armor**: Event and collaboration armor pieces

Total: **250+ unique armor IDs**

See [armor_database.py](armor_database.py) for complete list.

## 🛠️ Technical Details

### Project Structure
```
.
├── mhr_armor_swapper_v4.py    # Main application
├── armor_database.py           # 250+ armor ID mappings
├── armor_database.txt          # Human-readable armor list
├── icon.ico                    # Application icon
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
└── README.md                   # This file
```

### Built With
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Modern Python UI
- **[Pillow](https://pillow.readthedocs.io/)** - Image processing
- **Python 3.9+** - Core language

### Build Info
- Built using **Nuitka** for optimized performance
- Single-file executable (~30MB)
- No external dependencies required

## 📝 How It Works

1. **ZIP Analysis** - Examines mod structure to find armor ID
2. **Pattern Matching** - Matches ID against armor database
3. **File Replacement** - Swaps armor ID references throughout mod
4. **ZIP Repack** - Creates new ZIP with converted armor
5. **Output** - Saves to `output/` folder ready for use

## 🐛 Troubleshooting

### "Invalid ZIP file"
- Ensure ZIP is a valid armor mod for Fluffy Mod Manager
- Extract and check structure matches expected format

### "Armor not detected"
- Some non-standard mods may not be compatible
- Try manual armor ID selection if available

### "Cannot open ZIP"
- Close any open file managers or archive tools
- Ensure sufficient disk space for temporary files
- Check file permissions

## 🤝 Contributing

Found a bug or have a feature request? 

- [Report Issues](https://github.com/yourusername/MHR-Armor-Swapper/issues)
- [Submit Pull Requests](https://github.com/yourusername/MHR-Armor-Swapper/pulls)

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

## ⚖️ Disclaimer

This tool is for personal use with Monster Hunter Rise. Respect mod authors' terms and Monster Hunter intellectual property.

## 🙏 Acknowledgments

- **Capcom** - Monster Hunter Rise, Sunbreak
- **Fluffy Mod Manager** - Best mod manager for MHR
- **CustomTkinter** - Beautiful UI framework
- **Modding Community** - Inspiration and support

## 📞 Support

- 📧 Open an issue on GitHub
- 💬 Join the modding Discord communities
- 🌐 Check [Monster Hunter Wiki](https://monsterhunter.fandom.com/)

---

**Version:** 4.0  
**Last Updated:** May 2024  
**Status:** Active Development ✅

Made with ❤️ for Monster Hunter fans
