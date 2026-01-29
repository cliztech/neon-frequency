# Dev Toolchain

## Language servers
- **TypeScript/React:** Use the TypeScript language server (`tsserver`) through your editor, backed by the repo TypeScript versions in `studio/` and `visuals/web-client/`. Recommended for React + Vite projects.
- **Python:** Use a Python language server such as Pyright or Python LSP Server (pylsp). The repo does not pin an LSP, so select the one your editor supports best.
- **SQL:** Use a SQL language server (e.g., `sqls` or `sql-language-server`) for database queries and Supabase-related SQL.

## CLI tools
### Audio processing
- **ffmpeg/ffprobe:** Standard for audio transforms, resampling, and encoding inspection.
- **sox:** Handy for quick waveform edits and audio conversions.

### Metadata tools
- **mediainfo:** High-level metadata inspection for audio and video files.
- **exiftool:** Deep metadata edits for asset tags and embedded metadata.

> These CLI tools are not bundled with the repo; install them via your OS package manager when needed.

## Lint, format, and test tooling
- **TypeScript linting:** ESLint scripts live in `studio/` and `visuals/web-client/`.
  - `studio`: `npm run lint`
  - `visuals/web-client`: `npm run lint`
- **TypeScript type-check/build:** Both front-end apps run `tsc` before Vite builds.
  - `npm run build`
- **Python tests:** `core/tests/` uses `unittest`.
  - `python -m unittest discover -s core/tests`

## CI expectations
- There is no CI configuration in the repo. Expectation is to run lint/type-check/build for the front-end apps and Python unit tests locally before shipping changes.

## Local dev environment setup
1. **Node.js + npm**
   - Install an LTS version of Node.js (to match Vite/TypeScript tooling).
   - Install dependencies:
     - `cd studio && npm install`
     - `cd visuals/web-client && npm install`
2. **Python 3.10+**
   - Create a virtual environment and install root dependencies:
     - `python -m venv .venv`
     - `source .venv/bin/activate`
     - `pip install -r requirements.txt`
3. **Optional CLI tools**
   - Install `ffmpeg`, `sox`, `mediainfo`, and `exiftool` via your OS package manager if you work with audio assets.
