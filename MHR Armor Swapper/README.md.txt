# Monster Hunter Rise Armor Swapper

A modern utility tool for converting Monster Hunter Rise armor mods into different armor IDs automatically.

Designed for:
- Monster Hunter Rise
- Sunbreak
- Fluffy Mod Manager

---

## Features

- Automatic armor ID detection
- Searchable armor database
- One-click armor conversion
- Automatic ZIP repack
- Modern dark UI
- Standalone EXE
- Supports most armor mods

---

## Preview

Add screenshots here.

---

## Usage

1. Open the application
2. Select your armor mod ZIP
3. Search target armor
4. Select target armor
5. Click Convert

The converted ZIP is ready for Fluffy Mod Manager.

---

## Requirements

- Windows 10 / 11
- Monster Hunter Rise
- Fluffy Mod Manager

---

## Supported Mods

Most armor replacement mods using:
- natives/
- prefab/
- reframework/

---

## Download

Download the latest release from:

- Nexus Mods
- GitHub Releases
- Caimogu

---

## Build

```bat
python -m nuitka ^
  --standalone ^
  --onefile ^
  --assume-yes-for-downloads ^
  --windows-console-mode=disable ^
  --enable-plugin=tk-inter ^
  --include-package-data=customtkinter ^
  --include-data-files=armor_database.txt=armor_database.txt ^
  --windows-icon-from-ico=icon.ico ^
  --plugin-enable=upx ^
  --upx-binary="D:\upx\upx.exe" ^
  --nofollow-import-to=tkinter.test ^
  --lto=yes ^
  --remove-output ^
  mhr_armor_swapper_v4.py
````

---

## Credits

Armor database:

* Monster Hunter Rise Modding Community

Tool by:

* Anedeshi

---

## License

MIT License

```

