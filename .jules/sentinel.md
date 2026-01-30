## 2026-01-30 - Hardcoded Secrets in Logic Scripts
**Vulnerability:** Found `password = "hackme"` hardcoded directly in Liquidsoap scripting logic (`radio.liq`).
**Learning:** Hardcoding secrets in scripts (even for dev) makes it impossible to deploy securely without code changes. Defaults should live in environment/config layers, not script logic.
**Prevention:** Use `environment.get()` or equivalent in scripts and enforce defaults via container orchestration (Docker Compose) or environment files.
