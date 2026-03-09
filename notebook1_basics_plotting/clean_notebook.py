import nbformat
import sys
from pathlib import Path

def clean_notebook_metadata(path: str):
    """
    Remove problematic metadata that breaks GitHub rendering,
    while keeping all cell outputs intact.
    """
    path = Path(path)
    if not path.exists():
        print(f"File not found: {path}")
        return

    # Read notebook
    nb = nbformat.read(str(path), as_version=4)

    # Keys in top-level metadata that trigger GitHub widget errors
    for key in ["widgets", "varInspector", "latex_envs"]:
        if key in nb['metadata']:
            nb['metadata'].pop(key, None)
            print(f"Removed top-level metadata: {key}")

    # Optional: Remove widgets metadata from individual cells if present
    for i, cell in enumerate(nb['cells']):
        if 'metadata' in cell and 'widgets' in cell['metadata']:
            cell['metadata'].pop('widgets', None)
            print(f"Removed widgets metadata from cell {i}")

    # Write the cleaned notebook back
    nbformat.write(nb, str(path))
    print(f"Notebook cleaned and saved: {path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_notebook.py <notebook.ipynb>")
        sys.exit(1)

    notebook_path = sys.argv[1]
    clean_notebook_metadata(notebook_path)