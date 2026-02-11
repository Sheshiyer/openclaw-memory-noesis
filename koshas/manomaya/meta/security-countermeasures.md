# 🛡️ Security Countermeasures

## Host Status (Mac Mini)
| Area | Status | Risk |
|------|--------|------|
| Platform | Local Mac | ✅ Low |
| Gateway | Loopback | ✅ Secure |
| Auth | Token | ✅ Secure |

## The 10 Attack Vectors (Audit)
1. **Prompt Injection**: ⚠️ Medium (Use `prompt_guard` skill)
2. **Credential Leakage**: ⚠️ Medium (Use `secret-scanner` skill)
3. **Platform Token Theft**: ✅ Low (FileVault dependent)

## Countermeasures
- **Rotate Gateway Token**: Every 30-90 days.
- **Restrict Exec**: Only run allowlisted commands.
- **Firewall**: Ensure macOS stealth mode is active.

---
_Security is Coherence._
