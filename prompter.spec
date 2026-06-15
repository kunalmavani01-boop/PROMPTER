# PyInstaller spec for bundling PROMPTER as a desktop app on Windows and macOS.

from pathlib import Path


project_root = Path(__file__).resolve().parent
datas = [
    (str(project_root / "static"), "static"),
    (str(project_root / "docs"), "docs"),
    (str(project_root / "examples"), "examples"),
]

hiddenimports = ["uvicorn.logging", "uvicorn.loops.auto", "uvicorn.protocols.http.auto"]

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
    a.binaries,
    a.datas,
    [],
    name="PROMPTER",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
app = BUNDLE(
    exe,
    name="PROMPTER.app",
    icon=None,
    bundle_identifier="com.kunalmavani.prompter",
)
