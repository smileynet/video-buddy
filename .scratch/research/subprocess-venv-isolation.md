# Subprocess Venv Isolation — Research Findings

## Summary

Running Python tools in isolated virtualenvs via subprocess is a well-established pattern used by pipx, uv, tox, nox, and the `isolated-environment` library. The core technique is to invoke the target venv's Python interpreter directly (e.g., `/path/to/venv/bin/python script.py`) without needing to "activate" the environment, combined with JSON over stdin/stdout for structured IPC. Modern tooling (uv 2024+) has largely superseded manual venv management with `uv run --isolated` and `uvx` for ephemeral tool execution.

## Details

### Pattern 1: Direct Interpreter Invocation (Fundamental)

The canonical pattern for subprocess venv isolation: call the venv's Python binary directly.

```python
import subprocess
import json
from pathlib import Path

VENV_PYTHON = Path("/path/to/tool-venv/bin/python")

result = subprocess.run(
    [str(VENV_PYTHON), "-m", "tool_module", "--json"],
    capture_output=True,
    text=True,
    timeout=300,
    check=True,
)
output = json.loads(result.stdout)
```

**Key insight**: You never need to "activate" a virtualenv for subprocess execution. Activation only sets environment variables (`PATH`, `VIRTUAL_ENV`) for interactive shell use. Calling the venv's `python` binary directly is sufficient — it automatically uses the venv's site-packages.

Source: [StackOverflow — Running subprocess within different virtualenv](https://stackoverflow.com/questions/8052926/running-subprocess-within-different-virtualenv-with-python)

### Pattern 2: JSON IPC via stdin/stdout

For structured communication between parent and child:

```python
import subprocess
import json

def run_isolated_tool(venv_python: Path, input_data: dict, timeout: int = 60) -> dict:
    """Run a tool in an isolated venv with JSON IPC."""
    payload = json.dumps(input_data)
    
    result = subprocess.run(
        [str(venv_python), "-m", "worker"],
        input=payload,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )
    
    # Parse JSON from stdout; stderr is for logs/diagnostics
    return json.loads(result.stdout)
```

Worker script pattern (in the isolated venv):

```python
import sys
import json

def main():
    input_data = json.loads(sys.stdin.read())
    # ... do work ...
    result = {"status": "ok", "data": processed}
    json.dump(result, sys.stdout)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
```

**Convention**: stdout is exclusively for structured output (JSON). All logging/diagnostics go to stderr. This keeps the IPC channel clean.

### Pattern 3: Error Handling (Comprehensive)

```python
import subprocess
import json
from pathlib import Path

class ToolError(Exception):
    def __init__(self, message, returncode=None, stderr=None):
        super().__init__(message)
        self.returncode = returncode
        self.stderr = stderr

def run_tool(venv_python: Path, args: list[str], input_data=None, timeout=300):
    """Run isolated tool with full error handling."""
    cmd = [str(venv_python)] + args
    
    try:
        result = subprocess.run(
            cmd,
            input=json.dumps(input_data) if input_data else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True,
        )
    except FileNotFoundError:
        raise ToolError(
            f"Venv Python not found at {venv_python}. "
            f"Run setup to create the tool environment."
        )
    except subprocess.TimeoutExpired as e:
        raise ToolError(
            f"Tool timed out after {timeout}s",
            stderr=e.stderr,
        )
    except subprocess.CalledProcessError as e:
        raise ToolError(
            f"Tool failed with exit code {e.returncode}",
            returncode=e.returncode,
            stderr=e.stderr,
        )
    
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise ToolError(
            f"Tool produced invalid JSON output: {result.stdout[:200]}",
            stderr=result.stderr,
        )
```

### Pattern 4: Timeout Management

Best practices for timeouts:

- **Always set a timeout** — a hung subprocess blocks your entire application
- `subprocess.run(timeout=N)` kills the child and raises `TimeoutExpired` after N seconds
- For process trees (shell=True or processes that spawn children), use `os.killpg` on Unix:

```python
import os
import signal
import subprocess

proc = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    start_new_session=True,  # Creates new process group
)
try:
    stdout, stderr = proc.communicate(timeout=timeout)
except subprocess.TimeoutExpired:
    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    proc.wait()
    raise
```

- Layer timeouts: short timeout for health checks (5s), medium for normal operations (60-300s), long for heavy processing (transcription, model inference: 1800s+)

Source: [Python docs — subprocess timeout](https://docs.python.org/3/library/subprocess.html), [StackOverflow — TimeoutExpired](https://stackoverflow.com/questions/28131659/understanding-subprocess-timeoutexpired)

### Pattern 5: Health Checks / Venv Validation

Before running expensive operations, verify the isolated environment is functional:

```python
def check_venv_health(venv_python: Path) -> bool:
    """Verify the isolated venv is usable."""
    try:
        result = subprocess.run(
            [str(venv_python), "-c", "import sys; print(sys.executable)"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def check_tool_available(venv_python: Path, module: str) -> bool:
    """Check if a specific tool/module is importable in the venv."""
    result = subprocess.run(
        [str(venv_python), "-c", f"import {module}; print({module}.__version__)"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.returncode == 0
```

### Pattern 6: uv-Based Isolation (Modern Approach, 2024+)

`uv` provides first-class support for isolated tool execution without managing venvs manually:

```python
# Run a tool in a temporary isolated environment (no persistent venv needed)
subprocess.run(
    ["uvx", "ruff", "check", "."],
    capture_output=True,
    text=True,
    timeout=60,
    check=True,
)

# Run with specific dependencies in isolation
subprocess.run(
    ["uv", "run", "--isolated", "--with", "whisper==1.0", "python", "transcribe.py"],
    capture_output=True,
    text=True,
    timeout=1800,
    check=True,
)
```

`uv tool run` (aliased as `uvx`) creates a temporary isolated venv, installs deps, runs the tool, and caches the environment. This is the modern equivalent of pipx for ephemeral execution.

Source: [uv docs — Tools](https://docs.astral.sh/uv/concepts/tools/), [uv docs — Running commands](https://docs.astral.sh/uv/concepts/projects/run/)

### Pattern 7: isolated-environment Library (AI/ML Use Case)

The `isolated-environment` library (now succeeded by `uv-iso-env`) demonstrates the production pattern for AI tools with conflicting deps:

```python
from pathlib import Path
from isolated_environment import isolated_environment_run

venv_path = Path("./whisper-venv")
requirements = ["openai-whisper", "torch==2.1.2+cu121 --extra-index-url ..."]

cp = isolated_environment_run(
    env_path=venv_path,
    requirements=requirements,
    cmd_list=["whisper", "--help"],
)
```

Key design: moves dependency installation from install-time to runtime, allowing conditional deps (e.g., CUDA vs CPU torch) based on system detection.

Source: [github.com/zackees/isolated-environment](https://github.com/zackees/isolated-environment)

### Pattern 8: Environment Variable Isolation

For full isolation, control the subprocess environment:

```python
import os
import subprocess

def make_clean_env(venv_path: Path) -> dict:
    """Create a minimal environment for the subprocess."""
    env = os.environ.copy()
    # Override PATH to put venv first
    env["PATH"] = f"{venv_path / 'bin'}:{env.get('PATH', '')}"
    env["VIRTUAL_ENV"] = str(venv_path)
    # Remove any parent venv markers
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    return env

result = subprocess.run(
    [str(venv_path / "bin" / "python"), "-m", "tool"],
    env=make_clean_env(venv_path),
    capture_output=True,
    text=True,
    timeout=300,
    check=True,
)
```

### Production Examples

1. **pipx** — Installs and runs Python CLI applications in isolated environments. Each app gets its own venv; executables are symlinked to PATH.
2. **tox / nox** — Create isolated venvs per test session, run commands within them via subprocess.
3. **pypa/build** — Uses `venv` module to create an isolated build environment, then runs build backends in subprocess (`pypa/build@38099ad`).
4. **uv tool run / uvx** — Creates temporary isolated venvs cached in `~/.cache/uv/`, with automatic dep resolution and execution.

## Sources

| Source | URL | Relevance |
|--------|-----|-----------|
| StackOverflow: Running subprocess in different virtualenv | https://stackoverflow.com/questions/8052926/ | Core pattern (direct interpreter path) |
| Python docs: subprocess module | https://docs.python.org/3/library/subprocess.html | Timeout, error handling, Popen |
| Real Python: subprocess guide | https://realpython.com/python-subprocess/ | Comprehensive patterns, exception handling |
| uv docs: Tools | https://docs.astral.sh/uv/concepts/tools/ | Modern isolated execution via uvx |
| uv docs: Running commands | https://docs.astral.sh/uv/concepts/projects/run/ | `--isolated` flag for ephemeral envs |
| zackees/isolated-environment | https://github.com/zackees/isolated-environment | AI dep isolation library (succeeded by uv-iso-env) |
| pypa/pipx | https://github.com/pypa/pipx | Production isolated app runner |
| pypa/build commit 38099ad | https://github.com/pypa/build/commit/38099ad | Venv creation in subprocess for build isolation |
| Blaxel: Python Sandbox for LLM | https://blaxel.ai/blog/python-sandbox-llm-untrusted-code-isolation | Security boundary patterns |

## Open Questions

1. **Graceful degradation**: When the isolated venv is corrupted or missing, should the parent auto-recreate it or fail fast? (pipx recreates; tox recreates; uv caches and recreates transparently)
2. **Startup overhead**: For frequently-called tools, is subprocess spawn overhead acceptable or should a long-running worker process (with JSON-RPC over stdio) be preferred?
3. **Signal propagation**: How to cleanly forward SIGTERM/SIGINT to child processes in process groups on Linux vs. Darwin?
4. **Resource limits**: Should `ulimit`-style constraints (memory, CPU time) be applied to isolated subprocesses to prevent runaway tools from starving the parent?
5. **Lock contention**: When multiple parent processes share the same isolated venv, pip install races can corrupt the environment. uv solves this with lockfile-based atomic installs — is this sufficient for concurrent access?
