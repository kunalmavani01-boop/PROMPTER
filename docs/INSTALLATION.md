# Installation

## Requirements

- Python 3.10+

## Developer install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Desktop source launch

```bash
python desktop.py
```

## Packaged desktop builds

- Windows build script: `scripts/build_windows.ps1`
- macOS build script: `scripts/build_macos.sh`
- Shared spec: `prompter.spec`
