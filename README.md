# scionsix-core

Prototype Android agent console (Kivy) — "ORI SCION Sovereign Node".

- `main.py`: Kivy app with a command input that executes shell commands locally and streams output.
- `logic/orchestrator.py`: orchestration logic.
- `ori`: Termux Python agent script (APEX 600 orchestration system).
- `ori-service`, `segment2.sh`, `deploy`: Termux service/plumbing scripts.
- `buildozer.spec`: Android APK build config (CI builds `bin/*.apk` on push via `.github/workflows/build.yml`).

Status: prototype from February 2026, not under active development.
