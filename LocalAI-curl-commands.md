# LocalAI Docker Curl Commands - PowerShell vs Bash

## The Problem

When running curl commands with JSON data in PowerShell, Unix/Bash-style quote escaping (`'\''`) doesn't work and causes syntax errors.

### ❌ **INCORRECT** (Bash syntax in PowerShell):
```powershell
docker exec localai sh -lc 'curl -s http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d '\''{"model":"tinyllama","messages":[{"role":"user","content":"Hello"}],"max_tokens":64}'\'''
```

**Error:**
```
Unexpected token ':"tinyllama"' in expression or statement.
```

---

## ✅ Solutions

### Option 1: PowerShell with Single Quotes (Recommended)

```powershell
docker exec localai sh -lc 'sleep 2; echo "== /v1/models =="; curl -s http://127.0.0.1:8080/v1/models; echo; echo "== chat test =="; curl -s http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"tinyllama\",\"messages\":[{\"role\":\"user\",\"content\":\"Xin chào! Hay trả lời một câu ngắn.\"}],\"max_tokens\":64}"'
```

**Key change:** Inside the `sh -lc '...'` single quotes, use escaped double quotes `\"` for the JSON.

### Option 2: PowerShell Here-String

For complex JSON, use PowerShell's here-string:

```powershell
$json = @'
{"model":"tinyllama","messages":[{"role":"user","content":"Xin chào! Hay trả lời một câu ngắn."}],"max_tokens":64}
'@

docker exec localai curl -s http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d $json
```

### Option 3: Bash/Linux (Original Syntax)

In bash shells (Git Bash, WSL, Linux, macOS), the original syntax works:

```bash
docker exec localai sh -lc 'sleep 2; echo "== /v1/models =="; curl -s http://127.0.0.1:8080/v1/models; echo; echo "== chat test =="; curl -s http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d '\''{"model":"tinyllama","messages":[{"role":"user","content":"Xin chào! Hay trả lời một câu ngắn."}],"max_tokens":64}'\'''
```

---

## Complete Example for PowerShell

### 1. Configure models.yaml

```powershell
docker exec localai sh -lc 'printf "models:\n  - name: tinyllama\n    model: tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf\n    backend: llama\n" > /models/models.yaml'
```

### 2. Restart LocalAI

```powershell
docker restart localai
```

### 3. Test endpoints

```powershell
# List models
docker exec localai sh -lc 'sleep 2; curl -s http://127.0.0.1:8080/v1/models'

# Chat completion test
docker exec localai sh -lc 'curl -s http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"tinyllama\",\"messages\":[{\"role\":\"user\",\"content\":\"Xin chào! Hay trả lời một câu ngắn.\"}],\"max_tokens\":64}"'
```

### 4. Combined command (PowerShell-compatible)

```powershell
docker exec localai sh -lc 'printf "models:\n  - name: tinyllama\n    model: tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf\n    backend: llama\n" > /models/models.yaml' ; docker restart localai ; docker exec localai sh -lc 'sleep 2; echo "== /v1/models =="; curl -s http://127.0.0.1:8080/v1/models; echo; echo "== chat test =="; curl -s http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"tinyllama\",\"messages\":[{\"role\":\"user\",\"content\":\"Xin chào! Hay trả lời một câu ngắn.\"}],\"max_tokens\":64}"'
```

---

## Quick Reference

| Shell | JSON String Syntax | Escape Character |
|-------|-------------------|------------------|
| PowerShell (inside `sh -lc '...'`) | `"{\"key\":\"value\"}"` | `\"` |
| Bash/Git Bash | `'\''{"key":"value"}'\''` | `'\''` |
| PowerShell (native curl) | `'{"key":"value"}'` | None needed |

---

## Troubleshooting

### Error: "Unexpected token in expression"
- You're using Bash quote escaping in PowerShell
- Replace `'\''` with `\"` inside the shell command string

### Error: "Missing argument in parameter list"
- Check that all JSON double quotes are escaped with `\"`
- Ensure the entire shell command is wrapped in single quotes: `'...'`

### Error: "Connection refused"
- Wait a few seconds after `docker restart localai` before testing
- Add `sleep 2` before curl commands: `sh -lc 'sleep 2; curl ...'`
