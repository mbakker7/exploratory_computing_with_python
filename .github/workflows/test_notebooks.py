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
notebooks = []
for path in BASE_DIR.iterdir():
    if path.is_dir():
        for nb in path.rglob("*_sol.ipynb"):
            notebooks.append(nb.resolve())
#%%
# test function
@pytest.mark.parametrize("path", notebooks, ids=lambda p: str(p))
def test_notebook_runs(path: Path) -> None:
    print(f"Testing notebook: {path.name}")
    if "bugs" in str(path):
        with pytest.raises(Exception):
            pm.execute_notebook(
                input_path=str(path),
                output_path=None,
                log_output=True,
                kernel_name="python3",
                cwd=str(path.parent),
            )
    else:
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
#     if "bugs" in str(path):
#         continue
#     test_notebook_runs(path=path)
