# English → Hindi Neural Machine Translation

**A comparative study of three sequence-to-sequence architectures**

Deep Learning mini-project · M.Tech II (AI & DS) · VPKBIET, Baramati

| | |
|---|---|
| Author | Anish Charudatta Date (Roll No. EN25552003) |
| Guide | Prof. Sushma S. Nandgaonkar |
| Corpus | IIT Bombay English–Hindi parallel corpus (`cfilt/iitb-english-hindi`) |
| Platform | Kaggle Notebooks, GPU T4 × 2, PyTorch, AMP |
| Final run | 1 h 17 min end-to-end, seed 42 |

---

## What this project does

Three neural machine translation architectures are trained on **exactly the same**
data, tokeniser, optimiser recipe and decoding procedure, so the only variable is
the architecture itself:

1. **Vanilla LSTM Seq2Seq** — 43.15 M parameters, one fixed context vector.
2. **Seq2Seq + Bahdanau attention** — 94.80 M parameters.
3. **Transformer** — 62.23 M parameters, 4+4 layers, 8 heads, Noam schedule.

A controlled comparison of this kind is uncommon: published studies usually change
the model *and* the preprocessing, which confounds the comparison.

## Headline results

Test set, greedy decoding on 2,505 sentences; beam search (k = 5) on the first 1,000.
Metrics via `sacrebleu` (BLEU `intl`, chrF++, TER).

| Model | Params (M) | BLEU greedy | chrF++ greedy | TER greedy | chrF++ beam |
|---|---:|---:|---:|---:|---:|
| **Seq2Seq + Bahdanau** | 94.80 | **2.665** | **18.560** | **98.656** | **17.929** |
| Vanilla Seq2Seq | 43.15 | 1.334 | 14.796 | 100.814 | 13.649 |
| Transformer | 62.23 | 0.427 | 7.911 | 213.607 | 9.094 |

Three findings worth reading the report for:

- **Subword tokenisation is the first win.** Hindi `<unk>` on test falls from
  **8.85 % → 0.001 %** moving from word-level to SentencePiece Unigram (32 k pieces).
- **Attention buys +3.76 chrF++** over the fixed-vector model, at 2.2× the parameters
  and 2.4× the training time.
- **The Transformer was unstable, and the reason is reportable.** The Vaswani Noam
  peak assumes ~25 k tokens per batch; here a batch is only ~4 k tokens, so the
  default peak diverges. Halving the Noam scale (1.0 → 0.55) removed the repetition
  collapse and lifted chrF++ from 3.494 → 7.911.

> One seed, no error bars. The ranking is **not** claimed as statistically significant,
> and the Transformer is **not** claimed as competitive (10.65 chrF++ behind).

## Repository layout

```
README.md                     this file
requirements.txt              Python dependencies
docs/                         master plan, canonical numbers, Chinese draft, original notes
notebooks/                    executed .ipynb (110 cells, 5 figures) + PDF + untrimmed original
report/                       final 38-page PDF + compilable LaTeX source and 7 figures
presentation/                 final 13-slide PowerPoint deck
results/                      machine-readable result tables (CSV) + provenance
scripts/                      helper scripts used while producing the documents
```

## Reproducing

1. Open `notebooks/EnHi_NMT_Executed_Notebook.ipynb` on Kaggle with **Internet ON**
   and **GPU T4 × 2**; use *Save & Run All (Commit)* so the run continues server-side.
2. `pip install -r requirements.txt` happens in notebook §0.1.
3. The `balanced` preset uses 99,561 training pairs, 3,000 validation, 2,505 test.
   Total wall clock ≈ 1 h 17 min.
4. All outputs are written under `/kaggle/working/EnHi_NMT_Study/`.

The report is built with **XeLaTeX** (pdfLaTeX cannot typeset Devanagari):

```bash
cd report/latex
xelatex main.tex
xelatex main.tex   # second pass for the table of contents
```

## Data and limitations

- Raw splits: 1,652,981 train / 520 validation / 2,507 test sentence pairs.
  Cleaning (NFKC, dedup, Devanagari validation, length-ratio filter) keeps 83.3 %
  of train. The 100 k training subset is a compute-budget decision.
- The 3,000-sentence validation set is only **520 official** sentences plus 2,480
  held out from train. Stated in the report's Limitations.
- No pretrained weights, one random seed, beam search on 1,000 sentences only.
- Scores are not comparable to published IITB BLEU figures (different subset/split).

See `docs/01_CANONICAL_NUMBERS.md` — the single source of truth for every number in
the report, the deck, and `results/`.

## Documents

| Deliverable | File |
|---|---|
| Final report (38 pp, English) | `report/EnHi_NMT_Report_EN_updated.pdf` |
| Report source | `report/latex/main.tex` |
| Presentation (13 slides) | `presentation/EnHi_NMT_Presentation_v3.pptx` |
| Executed notebook | `notebooks/EnHi_NMT_Executed_Notebook.ipynb` |
| Notebook as PDF (54 pp) | `notebooks/EnHi_NMT_Notebook.pdf` |

`docs/ORIGINAL_PROJECT_NOTES.md` is the project's earlier planning README, kept for
provenance. It describes a 34-page Chinese-body report and a 16-slide Stage-I deck —
**both superseded** by the English report and the v3 deck above.
