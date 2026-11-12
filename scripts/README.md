# Helper scripts

Utilities used while producing the documents, retained for provenance.

- `fill_tables.py` — patches numeric tables into a LaTeX `main.tex`.
- `trim_notebook.py` — removes the notebook's opening orientation cells to produce
  `EnHi_NMT_Executed_Notebook.ipynb` from the untrimmed Kaggle download.

**Note:** both scripts contain hard-coded absolute paths into the original working
folder (the author's `Downloads/EnHi_NMT_Report_and_PPT/`). They are not intended
to run as-is from this repository; edit the path constants first. The `.ORIGINAL.ipynb`
in `../notebooks/` is the untrimmed input if you want to re-run the trim.
