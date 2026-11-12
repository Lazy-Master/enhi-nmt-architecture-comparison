# En→Hi NMT — Report & Presentation Plan

Created 24 Oct 2026, after the final Kaggle run (v5) completed successfully.

## What's in here

| File | What it is |
|---|---|
| `report/EnHi_NMT_Report.pdf` | **The report.** 34 pages, A4. Front matter in English; chapters, tables and captions in Chinese; Hindi model output in original Devanagari. |
| `report/main.tex` | The LaTeX source behind the report. |
| `notebook/EnHi_NMT_Executed_Notebook.pdf` | **The notebook as a PDF** — 52 pages, A4, all 28 executed cells and 5 figures. |
| `notebook/EnHi_NMT_Executed_Notebook.ipynb` | **The notebook as .ipynb** — 110 cells with every output intact. Orientation trimmed (see below). |
| `notebook/EnHi_NMT_Executed_Notebook.ORIGINAL.ipynb` | The untrimmed download, kept in case you want the removed sections back. |
| `ppt/EnHi_NMT_Stage1_Review/EnHi_NMT_Stage1_Review.pptx` | **The review deck** — 16 slides, English, academic blue/white. |
| `00_MASTER_PLAN.md` | Template shrinking, page budget, PPT outline, writing order, traps. |
| `01_CANONICAL_NUMBERS.md` | Every number the documents may use, with provenance. |
| `02_REPORT_DRAFT_ZH.md` | The Chinese body text as plain Markdown, for copy-paste while translating. |
| `report/` (other) | `vpcoe.cls`, `fancyhdr.sty`, `vpcoe_logo.JPG` — the college template. |

## Notebook: what was removed

The opening orientation material was trimmed to keep only the introduction, the tools
used and the notebook structure:

| Removed | Kept |
|---|---|
| §3 Expected outcome | Title block |
| §4 How to run this notebook | §1 Introduction |
| "What this notebook does" step table | §2 What is used (tools) |
| "Expected runtime" | §3 Notebook structure |
| *Design decisions* markdown cell | |
| *Repository layout / Configuration presets* cell | |

Also corrected `Environment` from "Google Colab" to **Kaggle Notebooks (GPU T4 × 2)** —
that is where the runs actually happened. All 28 executed outputs and 5 figures survive.

## Deck structure (16 slides, English)

Cover · The question · Objectives O1–O5 · Data · Tokenisation (8.85 % → 0.001 %) ·
Three architectures · One recipe · Results · Beam search · Accuracy vs length ·
Attention alignment · Error analysis · **Transformer instability** · What architecture
buys · Limitations · Conclusion.

Slide 13 is the pivot: the Transformer collapsed, the deck diagnoses why (Noam peak vs
batch size), shows the fix, and quantifies it. That is the strongest content in the study
and it is deliberately not buried.

## Status

- **Results: final.** Kaggle run `v5 transformer lr0.55`, `Ran in 1 hour and 17 minutes`.
- **Report:** 34 pages, A4, compiles clean with 0 missing glyphs.
- **Notebook:** .ipynb (110 cells) + .pdf (52 pages), both verified.
- **Deck:** 16 slides, all passing the layout checker.
- **Front matter:** Anish Charudatta Date · Roll No. EN25552003 ·
  Guide Prof. Sushma S. Nandgaonkar.
- **7 figures** in the report are still placeholders; 5 PNGs exist from the run.

## How to rebuild

**Report** (must be `xelatex` — pdfLaTeX cannot typeset Chinese or Devanagari):
```
cd report
xelatex main.tex
xelatex main.tex     # second pass for the TOC
```

**Notebook PDF:**
```
python nb2html.py notebook/EnHi_NMT_Executed_Notebook.ipynb notebook/_render.html
chrome --headless --print-to-pdf=notebook/EnHi_NMT_Executed_Notebook.pdf \
       file:///<abs path>/notebook/_render.html
```

**Deck:** edit `slides/NN.slide` then re-run `gen_slides.py` and re-insert, or edit the
`.pptx` directly.

## Two fixes applied to the college template

1. **Paper size.** The class sets `\textwidth` by hand and silently ignores `a4paper`,
   so the stock template produces **US Letter**. Added `geometry` with A4.
2. **Devanagari.** The class has no Devanagari font. Added
   `\newfontfamily\devfont[Script=Devanagari]{Nirmala UI}`.

## The headline numbers

| model | params | chrF++ (greedy) | BLEU (greedy) | chrF++ (beam) |
|---|---|---|---|---|
| Seq2Seq + Bahdanau | 94.80 M | **18.56** | 2.665 | 17.93 |
| Vanilla Seq2Seq | 43.15 M | 14.80 | 1.334 | 13.65 |
| Transformer | 62.23 M | 7.91 | 0.427 | 9.09 |

Tokenisation: `<unk>` on test **8.85 % → 0.001 %** (word-level → SentencePiece subword).

## Suggested next step

Follow the writing order in §A6 of the master plan. It is deliberately sequenced so the
mechanical sections come first and the Introduction is written last, once the numbers
are fixed and the framing can match them.
