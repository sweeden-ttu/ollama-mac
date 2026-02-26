# ollama-mac

Ollama LLM deployment on macOS with Apple Silicon/Metal GPU acceleration

## Features

- Metal GPU acceleration
- macOS native
- Homebrew support

## Ollama port mapping (canonical)

Same mapping across all Ollama projects. Workflows that use **@granite**, **@deepseek**, **@qwen-coder**, or **@codellama** call Ollama on the port for that model and environment.

| Environment        | granite | deepseek | qwen-coder | codellama |
|--------------------|---------|----------|------------|-----------|
| Debug (VPN)        | 55077   | 55088    | 66044      | 66033     |
| Testing +1 (macOS) | 55177   | 55188    | 66144      | 66133     |
| Testing +2 (Rocky) | 55277   | 55288    | 66244      | 66233     |
| Release +3        | 55377   | 55388    | 66344      | 66333     |

See **docs/AGENTS.md** for details.

## Related Projects

- toolchain-module
- ollama-hpcc
- ollama-rocky
- ollama-podman

## Installation

```bash
pip install -e src/python/
```

## License

MIT
