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

### Option 2: PowerShell Native with ConvertTo-Json (Recommended for Complex JSON)

Use PowerShell objects and `ConvertTo-Json` with `curl.exe`:

```powershell
# Wait for LocalAI to be ready after restart
Start-Sleep -Seconds 5

# Create JSON using PowerShell objects
$body = @{
    model = 'tinyllama'
    messages = @(
        @{
            role = 'user'
            content = 'Xin chào! Hay trả lời một câu ngắn.'
        }
    )
    max_tokens = 64
} | ConvertTo-Json -Depth 5

# Save to temp file and use curl.exe (more reliable than piping)
$body | Out-File -FilePath "$env:TEMP\localai-request.json" -Encoding utf8 -NoNewline
curl.exe -s http://localhost:8080/v1/chat/completions -H "Content-Type: application/json" -d "@$env:TEMP\localai-request.json"
```

**Note:** Piping directly to `curl.exe` with `--data-binary "@-"` can cause hanging issues in PowerShell. Use a temp file instead.

### Option 3: PowerShell Here-String (For Simple Cases)

For simpler JSON, use PowerShell's here-string:

```powershell
$json = @'
{"model":"tinyllama","messages":[{"role":"user","content":"Xin chào! Hay trả lời một câu ngắn."}],"max_tokens":64}
'@

docker exec localai curl -s http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d $json
```

### Option 4: Bash/Linux (Original Syntax)

In bash shells (Git Bash, WSL, Linux, macOS), the original syntax works:

```bash
docker exec localai sh -lc 'sleep 2; echo "== /v1/models =="; curl -s http://127.0.0.1:8080/v1/models; echo; echo "== chat test =="; curl -s http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d '\''{"model":"tinyllama","messages":[{"role":"user","content":"Xin chào! Hay trả lời một câu ngắn."}],"max_tokens":64}'\'''
```

---

## Complete Example for PowerShell

### 1. Configure models.yaml

**⚠️ IMPORTANT:** Don't use `printf` in PowerShell - it corrupts the YAML file. Use one of these methods instead:

**Method A - Create locally and copy (Recommended):**

```powershell
# Create YAML file locally
@"
models:
  - name: tinyllama
    model: tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
    backend: llama
"@ | Out-File -FilePath "models.yaml" -Encoding utf8 -NoNewline

# Copy to container
docker cp models.yaml localai:/models/models.yaml
```

**Method B - Use echo -e:**

```powershell
docker exec localai sh -lc 'echo -e "models:\n  - name: tinyllama\n    model: tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf\n    backend: llama" > /models/models.yaml'
```

### 2. Restart LocalAI and wait

```powershell
docker restart localai
Start-Sleep -Seconds 5
```

### 3. Verify models.yaml is correct

```powershell
docker exec localai cat /models/models.yaml
# Should show proper multi-line YAML, not "models:nlocalai"
```

### 4. Test endpoints

```powershell
# List models
docker exec localai sh -lc 'curl -s http://127.0.0.1:8080/v1/models'

# Chat completion test (using model name from YAML)
docker exec localai sh -lc 'curl -s http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"tinyllama\",\"messages\":[{\"role\":\"user\",\"content\":\"Xin chao! Tra loi mot cau ngan.\"}],\"max_tokens\":64}"'
```

### 5. Complete workflow (PowerShell-compatible)

```powershell
# Create and copy models.yaml
@"
models:
  - name: tinyllama
    model: tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
    backend: llama
"@ | Out-File -FilePath "models.yaml" -Encoding utf8 -NoNewline
docker cp models.yaml localai:/models/models.yaml

# Restart and wait
docker restart localai
Start-Sleep -Seconds 5

# Test
Write-Host "`n== Verify models.yaml ==" -ForegroundColor Cyan
docker exec localai cat /models/models.yaml

Write-Host "`n== List models ==" -ForegroundColor Cyan
docker exec localai curl -s http://127.0.0.1:8080/v1/models | ConvertFrom-Json | ConvertTo-Json

Write-Host "`n== Chat test ==" -ForegroundColor Cyan
docker exec localai sh -lc 'curl -s http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"tinyllama\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello! Reply briefly.\"}],\"max_tokens\":64}"'
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

### Error: "no backends found" or corrupted `models.yaml`

**Problem:** The `models.yaml` file shows as `models:nlocalai` (all on one line) instead of proper YAML formatting.

**Cause:** The `printf "models:\n..."` command isn't properly interpreting `\n` newlines in PowerShell's `docker exec` context.

**Solution 1 - Use `echo -e` instead of `printf`:**

```powershell
docker exec localai sh -lc 'echo -e "models:\n  - name: tinyllama\n    model: tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf\n    backend: llama" > /models/models.yaml'
```

**Solution 2 - Use multiple echo commands:**

```powershell
docker exec localai sh -c 'echo "models:" > /models/models.yaml && echo "  - name: tinyllama" >> /models/models.yaml && echo "    model: tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf" >> /models/models.yaml && echo "    backend: llama" >> /models/models.yaml'
```

**Solution 3 - Create YAML file locally and copy it:**

```powershell
# Create the YAML file locally
@"
models:
  - name: tinyllama
    model: tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
    backend: llama
"@ | Out-File -FilePath "models.yaml" -Encoding utf8 -NoNewline

# Copy to container
docker cp models.yaml localai:/models/models.yaml

# Restart LocalAI
docker restart localai

# Verify it worked
docker exec localai cat /models/models.yaml
```

**Verify the fix:**

```powershell
# Check models.yaml content
docker exec localai cat /models/models.yaml

# Should show proper YAML formatting:
# models:
#   - name: tinyllama
#     model: tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
#     backend: llama
```

### Error: Curl hangs when piping JSON in PowerShell

**Problem:** Running `$body | curl.exe --data-binary "@-"` hangs or doesn't return output.

**Solution:** Save JSON to a temporary file instead of piping:

```powershell
$body = @{
    model = 'tinyllama'
    messages = @(@{role='user'; content='Hello!'})
    max_tokens = 64
} | ConvertTo-Json -Depth 5

$body | Out-File -FilePath "$env:TEMP\localai-request.json" -Encoding utf8 -NoNewline
curl.exe -s http://localhost:8080/v1/chat/completions -H "Content-Type: application/json" -d "@$env:TEMP\localai-request.json"
```
