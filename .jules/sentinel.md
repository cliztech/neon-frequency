## 2026-01-30 - Hardcoded Secrets in Logic Scripts
**Vulnerability:** Found `password = "******"` hardcoded directly in Liquidsoap scripting logic (`radio.liq`).
**Learning:** Hardcoding secrets in scripts (even for dev) makes it impossible to deploy securely without code changes. Defaults should live in environment/config layers, not script logic.
**Prevention:** Use `sys.getenv()` (Liquidsoap v2+) or equivalent in scripts and enforce defaults via container orchestration (Docker Compose) or environment files.

## 2026-01-30 - Default Secrets in Infrastructure Code
**Vulnerability:** GitGuardian flagged `:-******` defaults in `docker-compose.yml` as exposed secrets.
**Learning:** Even if used as a fallback for development, hardcoding a known weak password in infrastructure code (IaC) triggers security scanners and presents a risk if the environment variable is accidentally omitted in production.
**Prevention:** Do not provide default values for secrets in IaC. Force the deployment environment to explicitly provide them (fail secure).
