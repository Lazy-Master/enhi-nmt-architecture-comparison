# Results

Machine-readable copies of the tables in the final report and presentation.

**Provenance.** Every value here is transcribed from
`../docs/01_CANONICAL_NUMBERS.md` (the project's declared single source of truth),
which was itself derived from the final Kaggle run `v5 transformer lr0.55`
(24 Oct 2026, 1 h 17 min, 502-line log). The same values appear in the executed
notebook outputs in `../notebooks/EnHi_NMT_Executed_Notebook.ipynb`.

These CSVs are **derived artifacts for convenience**, not raw run outputs. The raw
`metrics.csv` / `results.json` / checkpoints produced under
`/kaggle/working/EnHi_NMT_Study/results/` were not part of the supplied folder.

| File | Contents |
|---|---|
| `metrics.csv` | Main test-set comparison (greedy + beam) |
| `training_summary.csv` | Params, best epoch/loss, training time, stopping |
| `chrf_by_length.csv` | chrF++ by source-sentence length |
| `output_length.csv` | Output-length behaviour, incl. Transformer 2.06× over-generation |
| `beam_search_delta.csv` | Greedy → beam k=5 deltas |
| `transformer_lr_ablation.csv` | Noam-scale v4 vs v5 stability study |
| `tokenisation.csv` | Word-level vs SentencePiece `<unk>` rates |
| `data_splits.csv` | Raw → cleaned → used pair counts |

Figures are in `../report/latex/figures/` (7 PNGs); they are the ones embedded in
the report and are referenced by `main.tex`.

**Known minor inconsistencies** between the run log and the canonical numbers file
(retained here deliberately, see `docs/ORIGINAL_PROJECT_NOTES.md` context):

- Transformer train time: canonical `59.0 min`, notebook log `57.0 min`,
  notebook summary table `56.3 min`.
- Transformer final train loss: canonical `6.7155` (best epoch 7), notebook summary
  `7.2415` (last epoch 11). Both are correct for their respective definitions.

Neither affects any headline metric.
