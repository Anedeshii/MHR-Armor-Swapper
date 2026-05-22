@echo off

python -m nuitka ^
  --standalone ^
  --onefile ^
  --assume-yes-for-downloads ^
  --windows-console-mode=disable ^
  --enable-plugin=tk-inter ^
  --include-package-data=customtkinter ^
  --windows-icon-from-ico=icon.ico ^
  --plugin-enable=upx ^
  --upx-binary="D:\upx\upx.exe" ^
  --nofollow-import-to=tkinter.test ^
  --lto=yes ^
  --remove-output ^
  mhr_armor_swapper_v4.py