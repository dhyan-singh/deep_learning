# Fix Report: dl_utils.device import get_device

## Issue
In the notebook, this import failed:

```python
from dl_utils.device import get_device
```

Error:

```text
ModuleNotFoundError: No module named 'dl_utils'
```

## Root Cause
The code inside `packages/dl_utils` was valid, but the active notebook/kernel environment did not have the local `dl_utils` package installed on its Python path.

So Python could not resolve `dl_utils.device` even though the files existed in the workspace.

## What Was Fixed

### Step 1: Confirmed the failing import in the notebook
Notebook file:
- `projects/mtech/cloud_autoscale_vm/project.ipynb`

Checked cell contents:

```python
import torch
from dl_utils.device import get_device
```

Observed runtime error:

```text
ModuleNotFoundError: No module named 'dl_utils'
```

### Step 2: Confirmed kernel interpreter path
Executed:

```python
import sys
print(sys.executable)
```

Interpreter used by notebook:

```text
/Users/dhyan/projects/python/deep_learning/.venv/bin/python
```

This verified where `dl_utils` needed to be installed.

### Step 3: Installed local package into the active notebook environment
Installed editable package:

```bash
uv pip install -e packages/dl_utils
```

Then re-ran the import cell. It succeeded.

### Step 4: Made the fix persistent for future environments
Updated root project config so `uv sync` always installs local `dl-utils`:

File changed: `pyproject.toml`

Before:

```toml
dependencies = [
    "matplotlib>=3.10.8",
    "numpy>=2.4.4",
    "pandas>=3.0.2",
    "seaborn>=0.13.2",
    "torch>=2.11.0",
    "torchaudio>=2.11.0",
    "torchvision>=0.26.0",
]
```

After:

```toml
dependencies = [
    "matplotlib>=3.10.8",
    "numpy>=2.4.4",
    "pandas>=3.0.2",
    "seaborn>=0.13.2",
    "torch>=2.11.0",
    "torchaudio>=2.11.0",
    "torchvision>=0.26.0",
    "dl-utils",
]

[tool.uv.sources]
dl-utils = { path = "packages/dl_utils", editable = true }
```

### Step 5: Synced dependencies and validated import from terminal
Synced:

```bash
uv sync
```

Validated:

```bash
/Users/dhyan/projects/python/deep_learning/.venv/bin/python -c "from dl_utils.device import get_device; print(get_device())"
```

Output was:

```text
mps
```

This confirms the import works and the function resolves a valid device.

## Code Locations Involved
- Root dependency/source mapping: `pyproject.toml`
- Local package metadata: `packages/dl_utils/pyproject.toml`
- Import target module: `packages/dl_utils/dl_utils/device.py`
- Notebook using the import: `projects/mtech/cloud_autoscale_vm/project.ipynb`

## Final State
- `from dl_utils.device import get_device` works in notebook and terminal using project venv.
- Local package installation is now persistent via `uv` config (not just one-off manual install).
