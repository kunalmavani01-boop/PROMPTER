New-Item -ItemType Directory -Force -Path dist | Out-Null
python -m pip install -r requirements.txt
python -m pip install -r requirements-desktop.txt
pyinstaller --noconfirm prompter.spec
