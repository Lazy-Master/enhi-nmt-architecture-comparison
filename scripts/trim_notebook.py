"""Trim the notebook's orientation material.

Keep only: title block, §1 Introduction, §2 What is used (tools), and the notebook
structure table. Remove the "expected outcome" / "how to run" / "expected runtime"
material, plus the two follow-on markdown cells that fall outside those three parts.
"""
import json
from pathlib import Path

NB = Path(r"C:\Users\anish\Downloads\EnHi_NMT_Report_and_PPT\notebook\EnHi_NMT_Executed_Notebook.ipynb")
nb = json.loads(NB.read_text(encoding="utf-8"))
cells = nb["cells"]

lines = "".join(cells[0]["source"]).splitlines()

# sanity-check the anchors
assert lines[0].startswith("# English"), lines[0]
assert "## 1 · Introduction" in lines[11], lines[11]
assert "## 2 · What is used" in lines[31], lines[31]
assert "## 3 · Expected outcome" in lines[45], lines[45]
assert "## 5 · Notebook structure" in lines[80], lines[80]

head = lines[0:45]          # title block + Introduction + What is used  (lines 1-45)
structure = lines[80:95]    # ## 5 · Notebook structure + stage table     (lines 81-95)

body = head + ["---", ""] + structure

# renumber §5 -> §3, since 3 and 4 are gone
body = [
    l.replace("## 5 · Notebook structure", "## 3 · Notebook structure")
    for l in body
]

# factual correction: the runs were on Kaggle, not Colab
body = [
    l.replace("**Environment** · Google Colab (GPU runtime), PyTorch",
              "**Environment** · Kaggle Notebooks (GPU T4 $\\times$2), PyTorch")
     .replace("| Environment | Google Colab, GPU runtime |",
              "| Environment | Kaggle Notebooks, GPU T4 $\\times$2 |")
    for l in body
]

cells[0]["source"] = [l + "\n" for l in body[:-1]] + [body[-1]]

# drop the two follow-on markdown cells (Design decisions; Repository layout + presets)
assert cells[1]["cell_type"] == "markdown" and "Design decisions" in "".join(cells[1]["source"])
assert cells[2]["cell_type"] == "markdown" and "Repository / output layout" in "".join(cells[2]["source"])
del cells[1:3]

NB.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")

print(f"cells now      : {len(cells)}")
print(f"cell 0 lines   : {len(body)}")
print("remaining headings in cell 0:")
for l in body:
    if l.startswith("#"):
        print("   ", l)
