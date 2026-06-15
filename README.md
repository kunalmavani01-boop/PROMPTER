# PROMPTER

PROMPTER is a prompt optimization toolkit with a FastAPI backend, browser UI, persistent local storage, and desktop packaging support for Windows and macOS.

## Production-ready upgrades

- Persistent local storage for versions and analytics in the user app-data directory
- Desktop launcher entrypoint for packaged builds
- PyInstaller spec for Windows `.exe` and macOS `.app` packaging
- GitHub Actions workflow for Windows and macOS desktop artifacts
- Build scripts for both platforms
- Health and settings endpoints for runtime inspection

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000`.

## Desktop mode

Run the packaged launcher source locally:

```bash
python desktop.py
```

This starts the local server and opens the PROMPTER UI in the default browser.

## Windows and macOS packaging

- Windows: `scripts/build_windows.ps1`
- macOS: `scripts/build_macos.sh`
- Shared PyInstaller config: `prompter.spec`
- Build-only dependency list: `requirements-desktop.txt`
- CI artifacts: `.github/workflows/desktop-build.yml`

## API

- `GET /health`
- `GET /api/settings`
- `POST /api/enhance`
- `GET /api/templates`
- `GET /api/versions`
- `POST /api/versions`
- `GET /api/versions/{version_id}`
- `GET /api/analytics`

## Project structure

```text
PROMPTER/
|-- .github/workflows/
|-- docs/
|-- examples/
|-- scripts/
|-- static/
|-- tests/
|-- desktop.py
|-- main.py
|-- prompter.spec
|-- requirements.txt
```

See [docs/GETTING_STARTED.md](./docs/GETTING_STARTED.md), [docs/INSTALLATION.md](./docs/INSTALLATION.md), and [docs/RELEASE.md](./docs/RELEASE.md).
