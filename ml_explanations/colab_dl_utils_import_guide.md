# Colab Guide: Fixing `from dl_utils.device import get_device`

## Why It Fails In Colab
When you open a notebook from GitHub in Google Colab, the runtime is a fresh VM.
Your local package inside this repo (`packages/dl_utils`) is not installed automatically.

That is why this line fails until setup is done:

```python
from dl_utils.device import get_device
```

## Recommended Project Structure (Keep This)

- `packages/dl_utils/pyproject.toml`
- `packages/dl_utils/dl_utils/__init__.py`
- `packages/dl_utils/dl_utils/device.py`
- `pyproject.toml` (root)

This structure is correct and does not need major changes for Colab.

## Colab-First Workflow
Always run a bootstrap cell at the top of the notebook before any `dl_utils` import.

### Step 1: Clone repo and install local package

```python
import os
import sys
import subprocess
from pathlib import Path

REPO_URL = "https://github.com/dhyan-singh/deep_learning.git"
REPO_DIR = "/content/deep_learning"

# Clone once per runtime
if not Path(REPO_DIR).exists():
    subprocess.check_call(["git", "clone", REPO_URL, REPO_DIR])

# Move into repo root
os.chdir(REPO_DIR)

# Install the local package that contains dl_utils.device
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-e", "packages/dl_utils"])
```

### Step 2: Import and verify

```python
from dl_utils.device import get_device
print(get_device())
```

## Optional: One-Cell Version

```python
import os, sys, subprocess
from pathlib import Path

REPO_URL = "https://github.com/dhyan-singh/deep_learning.git"
REPO_DIR = "/content/deep_learning"

if not Path(REPO_DIR).exists():
    subprocess.check_call(["git", "clone", REPO_URL, REPO_DIR])

os.chdir(REPO_DIR)
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-e", "packages/dl_utils"])

from dl_utils.device import get_device
print(get_device())
```

## If You Use Private Repos
Use one of these approaches before cloning:

1. Mount Google Drive and copy repo manually.
2. Use a GitHub token with `git clone` HTTPS URL.
3. Zip upload the repo to Colab and unzip under `/content`.

## Best Practice For Fewer Name Collisions
`dl_utils` is a unique package name and avoids generic naming collisions.

Then imports become:

```python
from dl_utils.device import get_device
```

## Quick Checklist Per New Colab Runtime

1. Clone repo.
2. `cd` into repo root.
3. `pip install -e packages/dl_utils`.
4. Run imports.

If runtime restarts, repeat the checklist.
