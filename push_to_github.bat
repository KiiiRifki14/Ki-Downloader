@echo off
if "%~1"=="" (
    echo Harap sertakan URL Repository GitHub Anda!
    echo Contoh penggunaan: push_to_github.bat https://github.com/KiiiRifki14/Ki-Downloader.git
    exit /b 1
)

echo Mengatur remote URL ke %~1 ...
git remote set-url origin %~1
echo Memulai Push kode ke GitHub ...
git push -u origin main
echo.
echo Selesai! Kode berhasil di-upload ke GitHub.
