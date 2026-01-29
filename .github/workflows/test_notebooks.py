#%%
# depenencies
from pathlib import Path
import papermill as pm
import pytest

#%%
# paths
CWD = Path(__file__).parent.resolve()
BASE_DIR = CWD.parent.parent

#%%
# Collect all notebooks you want to test
notebooks_to_ignore = ["bugs", "wm", "s3", "s4"]
notebooks = []
for path in BASE_DIR.iterdir():
    if path.is_dir():
        if any(ignored in path.name for ignored in notebooks_to_ignore):
            continue
        if ".github" in str(path):
            continue
        for nb in path.rglob("*_sol.ipynb"):
            notebooks.append(nb.resolve())
#%%
# test function
@pytest.mark.parametrize("path", notebooks, ids=lambda p: str(p))
def test_notebook_runs(path: Path) -> None:
    print(f"Testing notebook: {path.name}")
    pm.execute_notebook(
        input_path=str(path),
        output_path=None,
        log_output=True,
        kernel_name="python3",
        cwd=str(path.parent),
    )

#%%
# local test
# for path in sorted(notebooks):
#     test_notebook_runs(path=path)
