# Release Guide

## Desktop targets

PROMPTER is prepared for:

- Windows desktop packaging via PyInstaller into `PROMPTER.exe`
- macOS desktop packaging via PyInstaller into `PROMPTER.app`

## Local build

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_windows.ps1
```

### macOS

```bash
chmod +x scripts/build_macos.sh
./scripts/build_macos.sh
```

## CI build

GitHub Actions runs `.github/workflows/desktop-build.yml` on `main` pushes and manual dispatches. It publishes desktop artifacts for both supported operating systems.

Desktop packaging dependencies live in `requirements-desktop.txt` so the main runtime install remains lightweight.

## Data storage

PROMPTER stores persistent user data in the platform app-data directory:

- Windows: `%APPDATA%\PROMPTER`
- macOS: `~/Library/Application Support/PROMPTER`

You can override this with `PROMPTER_DATA_DIR`.
