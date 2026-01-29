#%%
# depenencies
from pathlib import Path
import papermill as pm
import pytest
from shutil import rmtree

#%%
# paths
CWD = Path(__file__).parent.resolve()
BASE_DIR = CWD.parent.parent
OUTPUT_DIR = CWD / ".ipynb_checkpoints"
OUTPUT_DIR.mkdir(exist_ok=True)

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
def test_notebook_runs(nb_path: Path) -> None:
    out_path = OUTPUT_DIR / nb_path.name
    print(f"Testing notebook: {nb_path.name}")
    pm.execute_notebook(
        input_path=str(nb_path),
        output_path=str(out_path),
        kernel_name="python3",
        log_output=True,
        cwd=str(nb_path.parent),
    )

#%%
@pytest.mark.parametrize("nb_path", notebooks, ids=lambda p: str(p))
def test_notebook_runs_pytest(nb_path: Path) -> None:
    test_notebook_runs(nb_path=nb_path)

# local test
# for nb_path in sorted(notebooks):
#     test_notebook_runs(nb_path)
#     break
# %%
rmtree(OUTPUT_DIR)
