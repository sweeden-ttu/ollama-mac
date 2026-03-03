# HPCC Ollama Job Submission Pipeline

This document describes how to use the HPCC Ollama aliases for job submission and tunneling.

## Quick Start

### 1. Source the aliases

Add to your `~/.zshrc`:
```bash
source ~/ollama-hpcc/scripts/hpcc-aliases.zsh
```

### 2. Check job status
```bash
hpcc-info
# or
hpcc-jobs
# or
hpcc-latest-info 
```

### 3. Submit a batch job
```bash
granite          # granite4:3b model (default)
deepseek         # deepseek-coder model
codellama        # codellama model
qwen             # qwen model
```

### 4. Wait for job to start running, then run ollama 
```bash
hpcc-tunnel              # Auto-detect running granite4 job
hpcc-tunnel granite4:3b  # Specify model explicitly
hpcc-tunnel deepseek-coder:6.7b
```

### 5. Connect to Ollama
```bash
curl http://localhost:<PORT>/api/tags
```

---

## Commands Reference

### Connection
| Command | Description |
|---------|-------------|
| `hpcc` | SSH to HPCC login node |
| `hpcc-login` | SSH to HPCC login node |

### Job Management
| Command | Description |
|---------|-------------|
| `hpcc-info` | Show job queue and .info files |
| `hpcc-status` | Show Slurm job queue |
| `hpcc-jobs` | Alias for hpcc-status |
| `hpcc-kill JOBID` | Kill a specific job |
| `hpcc-git-pull` | Pull latest ollama-hpcc repo |

### Tunnels
| Command | Description |
|---------|-------------|
| `hpcc-tunnel [MODEL]` | Auto-create tunnel to running Ollama job |
| `hpcc-tunnel-jump` | Legacy tunnel command |

### Batch Jobs
| Command | Description |
|---------|-------------|
| `granite` | Submit granite4:3b batch job |
| `deepseek` | Submit deepseek-coder batch job |
| `codellama` | Submit codellama batch job |
| `qwen` | Submit qwen-coder batch job |

### Interactive Sessions
| Command | Description |
|---------|-------------|
| `granite-interactive` | Start interactive GPU session |
| `deepseek-interactive` | Start interactive GPU session |
| `codellama-interactive` | Start interactive GPU session |
| `qwen-interactive` | Start interactive GPU session |

---

## Environment Variables

When a job runs, the following are set in `.info` files in `~/ollama-logs/`:

```
JOB_ID=<job_id>
MODEL=<model_name>
NODE=<hostname>
PORT=<port>
OLLAMA_HOST=http://127.0.0.1:<port>/
OLLAMA_BASE_URL=http://localhost:<port>/api
STARTED=<timestamp>
```

---

## Debugging

### Check job status
```bash
hpcc-info
hpcc-jobs
```

### View latest job info
```bash
hpcc-latest-log
```

### Kill stuck job
```bash
hpcc-kill <JOB_ID>
```

### Check tunnel
```bash
lsof -i :<PORT>
curl -v http://localhost:<PORT>/api/tags
```

### Kill tunnel
```bash
pkill -f "ssh.*-L.*<PORT>"
```

---

## Troubleshooting

**Job not running?**
- Run `hpcc-info` to check queue status
- Jobs must be RUNNING before creating tunnel

**Tunnel not working?**
- Verify job is running: `hpcc-info`
- Check port: `lsof -i :<PORT>`
- Kill old tunnels: `pkill -f ssh.*-L`

**Wrong model?**
- Pass model explicitly: `hpcc-tunnel deepseek-coder:6.7b`
