# Container Deployment

## Podman on macOS

This project uses Podman for containerized Ollama deployment on macOS.

## Port Configuration

| Port  | Model     | Description          |
|-------|-----------|----------------------|
| 55077 | granite4  | IBM Granite model    |
| 66044 | qwen-coder| Qwen Coder model    |

## Deployment Steps

1. Install Podman Desktop for macOS
2. Pull Ollama container image
3. Configure port mappings:
   ```bash
   podman run -d -p 55077:11434 --name ollama-granite4 ollama/ollama
   podman run -d -p 66044:11434 --name ollama-qwen-coder ollama/ollama
   ```
4. Pull models:
   ```bash
   podman exec ollama-granite4 ollama pull granite4
   podman exec ollama-qwen-coder ollama pull qwen-coder
   ```

## Verification

Check service status:
```bash
curl http://localhost:55077/api/tags
curl http://localhost:66044/api/tags
```
