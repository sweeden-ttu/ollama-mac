# LangChain, LangGraph, and LangSmith tests

Tests for the LangChain ecosystem in `ollama-mac`, runnable with the **LangSmith** Miniconda environment.

## Setup (Miniconda)

From this directory (`ollama-mac/src/python`):

```bash
# Create and activate the LangSmith environment
conda env create -f environment-langsmith.yml
conda activate LangSmith
```

Or with an existing env and pip only:

```bash
conda create -n LangSmith python=3.11 -y
conda activate LangSmith
pip install -r requirements-langsmith.txt
```

Install the package in editable mode (optional, for local imports):

```bash
pip install -e .
```

## Run tests

```bash
conda activate LangSmith
# Disable LangSmith tracing if you don't have LANGCHAIN_API_KEY (avoids 403)
export LANGCHAIN_TRACING_V2=false
pytest tests/ -v
```

From repo root:

```bash
conda run -n LangSmith pytest src/python/tests/ -v
```

## Optional: LangSmith tracing

To run the traced-invocation test (sends one trace to LangSmith):

1. Create an API key at [smith.langchain.com](https://smith.langchain.com).
2. Set `LANGCHAIN_API_KEY` in your environment.
3. Run tests; `test_langsmith_traced_invocation` will run when the key is set.
