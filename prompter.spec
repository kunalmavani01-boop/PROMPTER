# PyInstaller spec for bundling PROMPTER as a desktop app on Windows and macOS.

import sys
from pathlib import Path


project_root = Path.cwd()
datas = [
    (str(project_root / "static"), "static"),
    (str(project_root / "docs"), "docs"),
    (str(project_root / "examples"), "examples"),
]

hiddenimports = [
    "uvicorn.logging",
    "uvicorn.loops.auto",
    "uvicorn.protocols.http.auto",
    "pydantic_core._pydantic_core",
]

a = Analysis(
    ["desktop.py"],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    [],
    name="PROMPTER",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

if sys.platform == "darwin":
    app = BUNDLE(
        exe,
        a.binaries,
        a.datas,
        name="PROMPTER.app",
        icon=None,
        bundle_identifier="com.kunalmavani.prompter",
    )
else:
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=False,
        name="PROMPTER",
    )
