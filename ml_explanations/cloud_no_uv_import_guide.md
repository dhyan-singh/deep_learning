# Cloud Guide: Import Packages When `uv` Is Not Available

If your cloud environment does not have `uv`, use standard Python package workflows.

## 1) Install Local Project Package With `pip` (Recommended)

From repo root:

```bash
python -m pip install -e packages/dl_utils
```

Then import normally:

```python
from dl_utils.device import get_device
print(get_device())
```

Why this is best:
- `-e` (editable install) keeps imports stable.
- Code changes in `packages/dl_utils` are available immediately.
- Works in local, VM, and notebook environments.

## 2) In Notebook/Colab: Install Into Active Kernel

Run this at the top of the notebook:

```python
import sys
import subprocess

subprocess.check_call([
    sys.executable,
    "-m",
    "pip",
    "install",
    "-e",
    "packages/dl_utils",
])
```

Then run imports:

```python
from dl_utils.device import get_device
```

## 3) If You Cannot Use Editable Installs

Install as a normal package:

```bash
python -m pip install packages/dl_utils
```

This works, but you must reinstall after package code changes.

## 4) Last-Resort Temporary Path Fix (Not Preferred)

Only for quick experiments:

```python
import sys
sys.path.append("/path/to/repo/packages/dl_utils")

from dl_utils.device import get_device
```

Use this only when install commands are blocked.

## 5) Verify You Are Installing Into the Right Python

Kernel mismatch is common in cloud notebooks.

```python
import sys
print(sys.executable)
```

Always install with `sys.executable -m pip` (inside notebook cells) so the package goes to the active kernel.

## 6) Full Cloud Bootstrap Example (No `uv`)

```python
import os
import sys
import subprocess
from pathlib import Path

REPO_URL = "https://github.com/dhyan-singh/deep_learning.git"
REPO_DIR = "/content/deep_learning"

if not Path(REPO_DIR).exists():
    subprocess.check_call(["git", "clone", REPO_URL, REPO_DIR])

os.chdir(REPO_DIR)
subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "packages/dl_utils"])

from dl_utils.device import get_device
print(get_device())
```

## Quick Checklist

1. Ensure repo is cloned and current working directory is repo root.
2. Install local package with `python -m pip install -e packages/dl_utils`.
3. Import with `from dl_utils.device import get_device`.
4. If it fails, verify `sys.executable` and reinstall into that interpreter.
