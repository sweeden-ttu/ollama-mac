# Cursor IDE Configuration

This document contains settings and recommendations for using Cursor IDE with this project.

## Extensions

- Python extension
- YAML extension
- GitLens
- Docker

## Settings

Use the Python interpreter from your Miniconda environment (e.g. LangSmith). In settings:

```json
{
  "python.defaultInterpreterPath": "${env:HOME}/miniconda3/envs/LangSmith/bin/python",
  "files.associations": {
    "*.md": "markdown"
  }
}
```

Or select the conda env from the status bar (Python version) after running `conda activate LangSmith`.

## Keybindings

- `Cmd+Shift+P`: Command Palette
- `Cmd+Shift+F`: Search in files
- `Cmd+P`: Quick file open
