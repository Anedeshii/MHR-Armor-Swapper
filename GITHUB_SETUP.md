# GitHub Setup Instructions

Selamat! Repository sudah siap untuk di-push ke GitHub. Ikuti langkah berikut:

## Step 1: Buat GitHub Repository

1. Buka https://github.com/new
2. Isi form:
   - **Repository name**: `MHR-Armor-Swapper`
   - **Description**: `A modern utility for converting Monster Hunter Rise armor mods`
   - **Visibility**: Public (atau Private jika preference)
   - **Initialize without README** (karena sudah punya)
3. Klik "Create repository"

## Step 2: Setup Remote dan Push

Jalankan command berikut di terminal:

```powershell
# Masuk ke folder project
cd "d:\Downloads\Rise Mod\New folder"

# Tambah remote (ganti USERNAME dengan GitHub username Anda)
git remote add origin https://github.com/USERNAME/MHR-Armor-Swapper.git

# Ganti branch default ke main
git branch -M main

# Push ke GitHub
git push -u origin main
```

## Step 3: Konfigurasi GitHub (Optional tapi Recommended)

Di halaman repository GitHub Anda:

1. **Settings > General**
   - Description: `A modern utility for converting Monster Hunter Rise armor mods`
   - Add topics: `monster-hunter, mods, armor, python, gui`

2. **Settings > Pages**
   - Bisa enable GitHub Pages untuk hosting dokumentasi (optional)

3. **Settings > Actions**
   - Verifikasi workflows sudah enabled
   - Nanti kalo push tag, automatic build exe!

## Step 4: Buat Release

Untuk buat first release dengan automatic build:

```powershell
# Ganti ke folder project
cd "d:\Downloads\Rise Mod\New folder"

# Buat tag (v1.0.0 or sesuai versi Anda)
git tag -a v1.0.0 -m "Version 1.0.0 - Initial Release"

# Push tag
git push origin v1.0.0
```

Ini akan trigger GitHub Actions workflow untuk automatic build executable!

## Structure yang sudah di-setup:

✅ **.gitignore** - Exclude Python cache, venv, build files
✅ **LICENSE** - MIT License (bisa diganti ke GPL jika prefer)
✅ **requirements.txt** - Dependencies (customtkinter, pillow)
✅ **README.md** - Comprehensive documentation dengan features, usage, troubleshooting
✅ **CONTRIBUTING.md** - Panduan untuk contributors
✅ **.gitattributes** - Konsistent line endings
✅ **.github/workflows/release.yml** - Auto-build executable saat tag baru
✅ **.github/workflows/lint.yml** - Code quality checks

## Selesai! 🎉

Repository Anda sekarang proper dan siap untuk:
- Otomatis build executable
- Code quality checks
- Professional releases
- Easy collaboration
